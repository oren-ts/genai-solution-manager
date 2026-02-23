import numpy as np

# -------------------------------------------------------
# a) Create a numpy array with 100 random numbers (0–50)
# -------------------------------------------------------
array_rand = np.random.randint(0, 50, 100)
print(f"a) Random array:\n{array_rand}\n")

# -------------------------------------------------------
# b) Calculate the average value
# -------------------------------------------------------
array_avg = np.average(array_rand)
print(f"b) Average value: {array_avg:.2f}\n")

# -------------------------------------------------------
# c) Find the maximum and minimum
# -------------------------------------------------------
array_min = np.min(array_rand)
array_max = np.max(array_rand)
print(f"c) Minimum value: {array_min}")
print(f"   Maximum value: {array_max}\n")

# -------------------------------------------------------
# d) Create a new array with only values above the average
# -------------------------------------------------------
boolean_mask = array_rand > array_avg  # True where value > average
array_above_avg = array_rand[boolean_mask]  # Keep only those values
print(f"d) Values above average ({array_avg:.2f}):\n{array_above_avg}\n")

# -------------------------------------------------------
# e) Sort the new array in ascending order
# -------------------------------------------------------
array_asc = np.sort(array_above_avg)
print(f"e) Sorted ascending:\n{array_asc}")
