import numpy as np


def heaviside(x):
    return 1 if x >= 0 else 0


class Perceptron:
    def __init__(self, input_length, learning_rate=0.01):
        # initialize small random weights, one per input + one for bias
        self.weights = np.random.randn(input_length) * 0.01
        self.bias = 0
        self.learning_rate = learning_rate

    def predict(self, x):
        # calculate weighted sum of inputs and apply activation function
        net_input = np.dot(x, self.weights) + self.bias
        return heaviside(net_input)

    def train(self, inputs, labels, epochs=10):
        # repeat for multiple epochs so the perceptron can converge
        for epoch in range(epochs):
            for x, label in zip(inputs, labels):
                prediction = self.predict(x)
                error = label - prediction
                # update weights and bias using perceptron learning rule
                self.weights += self.learning_rate * error * x
                self.bias += self.learning_rate * error


# AND dataset
inputs = np.array([[0, 0], [0, 1], [1, 0], [1, 1]])
labels = np.array([0, 0, 0, 1])

# train
perceptron = Perceptron(input_length=2)
perceptron.train(inputs, labels)

# test
for x, label in zip(inputs, labels):
    prediction = perceptron.predict(x)
    print(f"Input: {x}, Expected: {label}, Predicted: {prediction}")
