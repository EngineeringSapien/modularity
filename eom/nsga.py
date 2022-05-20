from collections import defaultdict
import numpy as np
import random

N = population_size = 25
num_parents = population_size*.4


def main():
    population = initialize_pop(N)

    for i in range(100):
        losses = compute_performance_loss(population)
        connection_costs = compute_connection_count_costs(population)  # eventually, compute_connection_distance_costs
        parents = stochastic_dominant_selection(population, r, num_parents)  # use crowding_distance() to break ties
        offspring = crossover(parents, N)
        offspring = mutate(offspring)
        population = population + offspring
        population = nondomimant_sorting(population)  # use crowding_distance() to sort any overflowing fronts


def main2():
    population = initialize_pop(100)
    for i in range(1):
        orgs = [tuple([obj_1(i), obj_2(i)]) for i in population]
        # parents = stochastic_dominant_selection(population, r, num_parents)
        # offspring = crossover(parents, N)
        # population = population + mutate(offspring)
        fronts = sortNondominated(orgs)


def initialize_pop(pop_size):
    x = random.sample(range(-100, 100), pop_size)
    # y = [{"id": str(i), "genome": j, "obj1": None, "obj2": None} for i,j in zip(range(len(x)), x)]
    return x


def stochastic_dominant_selection(population, r, num_parents):
    parents = []
    while len(parents) < num_parents:
        ps = random.sample(range(len(population)), 2)
        parent1 = population[ps[0]]
        parent2 = population[ps[1]]
        current_parents = [parent1, parent2]

        # if (np.random.uniform(0,1) > r and outperforms(parent1[0], parent2[0])) or dominates(parent1["objs"], parent2["objs"], [-1, 1]):
        #     parents.append(parent1)
        # elif ( np.random.uniform(0,1) > r and outperforms(parent2[0], parent1[0]) ) or dominates(parent2["objs"], parent1["objs"], [-1, 1]):
        #     parents.append(parent2)

        stochastic = np.random.uniform(0, 1) <= r
        if not stochastic:
            if outperforms(parent1[0], parent2[0]):
                parents.append(parent1)
            elif outperforms(parent2[0], parent1[0]):
                parents.append(parent2)
            else:
                parents.append(current_parents[random.randint(0,1)])
                # parents.append([parent1, parent2][less_crowded(parent1, parent2)])
        elif stochastic:
            if dominates(parent1, parent2, [-1, -1]):
                parents.append(parent1)
            elif dominates(parent2, parent1, [-1, -1]):
                parents.append(parent2)
            else:
                parents.append(current_parents[random.randint(0,1)])
                # parents.append([parent1, parent2][less_crowded(parent1, parent2)])

    return parents


def less_crowded(a, b):
    # TODO Write this function
    return 1


def outperforms(a, b, sign=-1):
    if a * sign > b * sign:
        return True
    else:
        return False


def dominates(objs_orgA, objs_orgB, sign=[1, 1]):
    """ Returns True iff organism A dominates organism B along all objectives"""
    indicator = False
    for a, b, sign in zip(objs_orgA, objs_orgB, sign):
        if a * sign > b * sign:
            indicator = True
        # if a is dominated by b in one of the objectives, then return False
        elif a * sign < b * sign:
            return False
    return indicator


def obj_1(x):
    y = -x ** 3
    return y


def obj_2(x):
    y = -(x-2)**2
    return y


def nondomimant_sorting():
    pass


def sortNondominated(individuals, k=None, first_front_only=False):
    """Sort the first *k* *individuals* into different nondomination levels
        using the "Fast Nondominated Sorting Approach" proposed by Deb et al.,
        see [Deb2002]_. This algorithm has a time complexity of :math:`O(MN^2)`,
        where :math:`M` is the number of objectives and :math:`N` the number of
        individuals.
        :param individuals: A list of individuals to select from.
        :param k: The number of individuals to select.
        :param first_front_only: If :obj:`True` sort only the first front and
                                    exit.
        :param sign: indicate the objectives are maximized or minimized
        :returns: A list of Pareto fronts (lists), the first list includes
                    nondominated individuals.
        .. [Deb2002] Deb, Pratab, Agarwal, and Meyarivan, "A fast elitist
            non-dominated sorting genetic algorithm for multi-objective
            optimization: NSGA-II", 2002.
    """
    if k is None:
        k = len(individuals)

    map_fit_ind = defaultdict(list)
    for i, f_value in enumerate(individuals):  # fitness = [(1, 2), (2, 2), (3, 1), (1, 4), (1, 1)...]
        map_fit_ind[f_value].append(i)
    fits = list(map_fit_ind.keys())  # fitness values

    current_front = []
    next_front = []
    dominating_fits = defaultdict(int)  # n (The number of people dominate you)
    dominated_fits = defaultdict(list)  # Sp (The people you dominate)

    # Rank first Pareto front
    # *fits* is a iterable list of chromosomes. Each has multiple objectives.
    for i, fit_i in enumerate(fits):
        for fit_j in fits[i + 1:]:
            # Eventhougn equals or empty list, n & Sp won't be affected
            if dominates(fit_i, fit_j):
                dominating_fits[fit_j] += 1
                dominated_fits[fit_i].append(fit_j)
            elif dominates(fit_j, fit_i):
                dominating_fits[fit_i] += 1
                dominated_fits[fit_j].append(fit_i)
        if dominating_fits[fit_i] == 0:
            current_front.append(fit_i)

    fronts = [[]]  # The first front
    for fit in current_front:
        fronts[-1].extend(map_fit_ind[fit])
    pareto_sorted = len(fronts[-1])

    # Rank the next front until all individuals are sorted or
    # the given number of individual are sorted.
    # If Sn=0 then the set of objectives belongs to the next front
    if not first_front_only:  # first front only
        N = min(len(individuals), k)
        while pareto_sorted < N:
            fronts.append([])
            for fit_p in current_front:
                # Iterate Sn in current fronts
                for fit_d in dominated_fits[fit_p]:
                    dominating_fits[fit_d] -= 1  # Next front -> Sn - 1
                    if dominating_fits[fit_d] == 0:  # Sn=0 -> next front
                        next_front.append(fit_d)
                         # Count and append chromosomes with same objectives
                        pareto_sorted += len(map_fit_ind[fit_d])
                        fronts[-1].extend(map_fit_ind[fit_d])
            current_front = next_front
            next_front = []

    return fronts


def crossover(a,b):
    r=random.random()
    if r>0.5:
        return mutate((a+b)/2)
    else:
        return mutate((a-b)/2)


def mutate(solution):
    mutation_prob = random.random()
    if mutation_prob < 1:
        solution = -100+(100+100)*random.random()
    return solution


def compute_performance_loss():
    pass

def compute_connection_count_costs():
    pass


main2()















