"""
10.A.01 - Linear Regression with Gradient Descent
===================================================
Exercise: Implement a simple linear regression model using gradient descent.
Dataset: Number of rooms (X) vs. apartment price in thousands of euros (y).

Steps:
    1. Define the dataset
    2. Standardize X and y using StandardScaler
    3. Implement the LinearRegressionGD class
    4. Train the model
    5. Visualize the cost function over epochs
"""

import numpy as np
from sklearn.preprocessing import StandardScaler
import matplotlib.pyplot as plt


# ── 1. Dataset ────────────────────────────────────────────────────────────────

# X: number of rooms (must be 2D — one column — because StandardScaler expects it)
# y: apartment prices in thousands of euros
rooms = np.array([[5], [4], [6], [3], [7]])
prices = np.array([300, 250, 350, 200, 400])


# ── 2. Standardization ───────────────────────────────────────────────────────

# Each feature gets its own scaler so means and std devs stay separate
scaler_rooms = StandardScaler()
scaler_prices = StandardScaler()

rooms_standardized = scaler_rooms.fit_transform(rooms)

# prices is 1D, but StandardScaler needs 2D → add a dimension, scale, then flatten back
prices_standardized = scaler_prices.fit_transform(prices[:, np.newaxis]).flatten()


# ── 3. Model Definition ──────────────────────────────────────────────────────


class LinearRegressionGD:
    """
    Linear Regression using Gradient Descent.

    This is essentially ADALINE without the step function:
    instead of predicting class labels, we predict continuous values.

    Parameters
    ----------
    learning_rate : float
        How large each weight update step is (default: 0.001).
    num_epochs : int
        How many full passes through the training data (default: 20).
    """

    def __init__(self, learning_rate=0.001, num_epochs=20):
        self.learning_rate = learning_rate
        self.num_epochs = num_epochs

    def fit(self, X, y):
        """Train the model by adjusting weights to minimize prediction error."""

        # Initialize all weights to zero: one per feature + one bias (intercept)
        self.weights_ = np.zeros(1 + X.shape[1])

        # Track the cost (total error) after each epoch to check convergence
        self.cost_per_epoch_ = []

        for _ in range(self.num_epochs):

            # Forward pass: compute predictions with current weights
            predictions = self.net_input(X)

            # How wrong are we? Positive = underpredicted, negative = overpredicted
            errors = y - predictions

            # Update feature weights: move in the direction that reduces error
            self.weights_[1:] += self.learning_rate * X.T.dot(errors)

            # Update the bias weight separately (it has no feature to dot with)
            self.weights_[0] += self.learning_rate * errors.sum()

            # Cost = sum of squared errors / 2  (the ½ simplifies the math gradient)
            cost = (errors**2).sum() / 2.0
            self.cost_per_epoch_.append(cost)

        return self

    def net_input(self, X):
        """Compute the linear combination: X·w + bias."""
        return np.dot(X, self.weights_[1:]) + self.weights_[0]

    def predict(self, X):
        """Return the predicted values (no threshold — this is regression, not classification)."""
        return self.net_input(X)


# ── 4. Train the Model ───────────────────────────────────────────────────────

regression_model = LinearRegressionGD()
regression_model.fit(rooms_standardized, prices_standardized)


# ── 5. Visualize the Cost Function ───────────────────────────────────────────

# If the model is learning correctly, cost should decrease with each epoch
epoch_numbers = range(1, regression_model.num_epochs + 1)

plt.plot(epoch_numbers, regression_model.cost_per_epoch_)
plt.xlabel("Epochs")
plt.ylabel("Sum of Squared Errors")
plt.title("Cost Function over Training Epochs")
plt.tight_layout()
plt.show()
