import numpy as np

np.random.seed(0)  # For reproducibility

# a) Generate hypothetical dataset
feature_1 = np.random.normal(20, 5, size=100)
feature_2 = np.random.normal(30, 5, size=100)
data = np.column_stack((feature_1, feature_2))

# b) Calculate mean and standard deviation for each feature
mean_1 = np.mean(data[:, 0])
mean_2 = np.mean(data[:, 1])
std_1 = np.std(data[:, 0])
std_2 = np.std(data[:, 1])

# c) Standardize each feature: subtract mean, divide by std
data[:, 0] = (data[:, 0] - mean_1) / std_1
data[:, 1] = (data[:, 1] - mean_2) / std_2

# d) Print first 5 standardized records
print(f"The first five standardized records:\n{data[:5]}")
