import numpy as np

# example = [0, 1, 0, 0,
#           1, 1, 0, 0]


def label_sample(sample):
    left = False
    right = False
    if sum(sample["pixels"][0:4]) >= 3 or sum(sample["pixels"][0:2]) >= 1:
        left = True
    if sum(sample["pixels"][4:8]) >= 3 or sum(sample["pixels"][6:8]) >= 1:
        right = True

    if left and right:
        sample["str_label"] = "both"
        sample["int_label"] = 3
    elif left:
        sample["str_label"] = "left"
        sample["int_label"] = 1
    elif right:
        sample["str_label"] = "right"
        sample["int_label"] = 2
    else:
        sample["str_label"] = "neither"
        sample["int_label"] = 0

    return sample


def generate_samples(n):
    all_samples = []
    all_arrays = []
    both_count = 0
    left_count = 0
    right_count = 0
    neither_count = 0

    while len(all_samples) < n:
        print("Sample ", len(all_samples))
        random_sample = {"pixels": np.array(np.random.randint(2, size=8)), "str_label": "tbd", "int_label": 0}
        random_sample = label_sample(random_sample)

        if random_sample["pixels"].tolist() in all_arrays:
            continue
        else:
            if random_sample["int_label"] == 3:
                if both_count <= left_count and both_count <= right_count:
                    both_count += 1
                    all_samples.append(random_sample)
                    all_arrays.append(random_sample["pixels"].tolist())
            elif random_sample["int_label"] == 1:
                if left_count <= both_count and left_count <= right_count:
                    left_count += 1
                    all_samples.append(random_sample)
                    all_arrays.append(random_sample["pixels"].tolist())
            elif random_sample["int_label"] == 2:
                if right_count <= left_count and right_count <= both_count:
                    right_count += 1
                    all_samples.append(random_sample)
                    all_arrays.append(random_sample["pixels"].tolist())
            elif random_sample["int_label"] == 0:
                if neither_count <= left_count and neither_count <= right_count and neither_count <= both_count:
                    neither_count += 1
                    all_samples.append(random_sample)
                    all_arrays.append(random_sample["pixels"].tolist())

    return all_samples

# all_samples = []
# for i in range(1000):
#     random_sample = {"pixels": np.array(np.random.randint(2, size=8)), "str_label": "tbd", "int_label": 0}
#     random_sample = label_sample(random_sample)
#     print(random_sample, "\n")
#     all_samples.append(random_sample)


