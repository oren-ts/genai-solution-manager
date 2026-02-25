class SimpleAdaline:
    def __init__(self, learning_rate=0.01, num_weights=2):
        self.learning_rate = learning_rate  # step size for weight updates
        self.weights = [0] * (
            num_weights + 1
        )  # initialize all weights to zero, index 0 is bias

    def net_input(self, inputs):
        # multiply each input by its weight, sum them up, then add the bias
        return sum(w * x for w, x in zip(self.weights[1:], inputs)) + self.weights[0]

    def activation(self, net_input):
        # identity function - returns value unchanged, placeholder for future activation functions
        return net_input

    def train(self, training_data, target_values):
        for inputs, target in zip(training_data, target_values):
            output = self.activation(self.net_input(inputs))  # current prediction
            error = target - output  # how wrong the prediction was
            self.weights[0] += self.learning_rate * error  # update bias weight
            for i in range(len(inputs)):
                # update each feature weight proportional to its input and the error
                self.weights[i + 1] += self.learning_rate * error * inputs[i]
        return self.weights


adaline = SimpleAdaline(learning_rate=0.01, num_weights=2)
training_data = [[0.5, -0.2], [-0.3, 0.8], [0.7, -0.4]]
target_values = [1, -1, 1]
updated_weights = adaline.train(training_data, target_values)
print("Updated weights:", updated_weights)
