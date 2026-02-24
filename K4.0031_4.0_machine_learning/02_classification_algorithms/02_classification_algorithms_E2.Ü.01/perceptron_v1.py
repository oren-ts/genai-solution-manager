import numpy as np

# weights = np.random.randn(2) * 0.01 # AND/OR
weights = np.random.randn(1) * 0.01
bias = 0
learning_rate = 0.01


def heaviside(x):
    return 1 if x >= 0 else 0


# inputs = np.array([[0, 0], [0, 1], [1, 0], [1, 1]]) # AND/OR
inputs = np.array([0, 1])  # NOT


# labels = np.array([0, 0, 0, 1]) # AND
# labels = np.array([0, 1, 1, 1]) # OR
labels = np.array([1, 0])  # NOT

# training loop
for epoch in range(10):
    for x, label in zip(inputs, labels):
        net_input = np.dot(x, weights) + bias
        prediction = heaviside(net_input)
        error = label - prediction
        weights += learning_rate * error * x
        bias += learning_rate * error

# testing loop
for x, label in zip(inputs, labels):
    net_input = np.dot(x, weights) + bias
    prediction = heaviside(net_input)
    print(f"Input: {x}, Expected: {label}, Predicted: {prediction}")
