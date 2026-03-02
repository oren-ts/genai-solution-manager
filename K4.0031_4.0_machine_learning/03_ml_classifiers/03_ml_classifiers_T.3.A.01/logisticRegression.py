"""
Exercise 3.A.01 - Logistic Regression
Course: Machine Learning K4.0031

Binary classification using scikit-learn's LogisticRegression.
A synthetic dataset is generated, split, standardized, trained,
evaluated, and visualized with a decision boundary.
"""

from sklearn.datasets import make_classification
from sklearn.model_selection import train_test_split
from sklearn.preprocessing import StandardScaler
from sklearn.linear_model import LogisticRegression
from sklearn.metrics import accuracy_score
import matplotlib.pyplot as plt
import numpy as np


# ── a) Generate a synthetic dataset ───────────────────────────────────────────
# make_classification creates fake labelled data for us to practice on.
# X = feature matrix (100 rows, 2 columns), y = class labels (0 or 1)
X, y = make_classification(
    n_samples=100,  # 100 data points
    n_features=2,  # 2 input features so we can plot in 2D
    n_redundant=0,  # no noise features
    n_informative=2,  # both features carry useful signal
    random_state=1,  # fixed seed for reproducibility
)


# ── b) Split into training and test data ──────────────────────────────────────
# 80% of the data is used for training, 20% is held back for testing.
# The model never sees the test data during training — this gives an honest
# measure of how well the model generalizes to new, unseen data.
X_train, X_test, y_train, y_test = train_test_split(
    X,
    y,
    test_size=0.2,  # 20% test, 80% training
    random_state=1,  # same seed = same split every run
)


# ── c) Standardize the features ───────────────────────────────────────────────
# StandardScaler rescales each feature to mean=0 and std=1.
# This prevents features with larger values from dominating the algorithm.
# IMPORTANT: we fit the scaler on training data only, then apply it to both.
# Fitting on test data too would be "data leakage" — the model would
# indirectly see test statistics during training.
scaler = StandardScaler()
X_train_std = scaler.fit_transform(X_train)  # learn mean/std from train, then scale
X_test_std = scaler.transform(X_test)  # apply the same scaling to test data


# ── d) Train the logistic regression model ────────────────────────────────────
# C=1.0 is the regularization parameter (inverse of strength).
# Lower C = stronger regularization = simpler model.
# Higher C = weaker regularization = more complex model.
# lbfgs is an efficient optimization algorithm for small/medium datasets.
logistic_model = LogisticRegression(solver="lbfgs", C=1.0, random_state=1)
logistic_model.fit(X_train_std, y_train)  # find the best weights using training data


# ── e) Evaluate the model ─────────────────────────────────────────────────────
# We predict class labels for the test set and compare against the true labels.
# accuracy_score = correct predictions / total predictions
y_pred = logistic_model.predict(X_test_std)
accuracy = accuracy_score(y_test, y_pred)
print(f"Model accuracy: {accuracy}")


# ── f) Visualize the decision boundary ────────────────────────────────────────
# To draw the decision boundary, we:
# 1. Create a fine grid of points covering the entire feature space
# 2. Predict the class for every point on the grid
# 3. Color the background by predicted class (this IS the decision boundary)
# 4. Plot the actual training and test points on top

# Step 1: define the grid boundaries with a small padding around the data
x_min, x_max = X_train_std[:, 0].min() - 1, X_train_std[:, 0].max() + 1
y_min, y_max = X_train_std[:, 1].min() - 1, X_train_std[:, 1].max() + 1

# Step 2: build the grid — one point every 0.02 units in both directions
xx, yy = np.meshgrid(np.arange(x_min, x_max, 0.02), np.arange(y_min, y_max, 0.02))

# Step 3: predict the class for every point on the grid
# ravel() flattens the grid, .T transposes so each row is one [x, y] pair
grid_predictions = logistic_model.predict(np.array([xx.ravel(), yy.ravel()]).T)
grid_predictions = grid_predictions.reshape(xx.shape)  # reshape back to grid

# Step 4: draw the colored background regions and scatter the data points
plt.contourf(xx, yy, grid_predictions, alpha=0.4)  # shaded decision regions

plt.scatter(  # training points as circles
    X_train_std[:, 0],
    X_train_std[:, 1],
    c=y_train,
    marker="o",
    s=20,
    label="Training data",
)
plt.scatter(  # test points as squares
    X_test_std[:, 0], X_test_std[:, 1], c=y_test, marker="s", s=20, label="Test data"
)

plt.xlabel("Feature 1")
plt.ylabel("Feature 2")
plt.legend(loc="upper left")
plt.title("Logistic Regression — Decision Boundary")
plt.show()
