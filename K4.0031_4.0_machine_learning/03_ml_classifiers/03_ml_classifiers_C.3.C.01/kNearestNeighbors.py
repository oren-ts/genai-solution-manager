"""
Exercise 3.C.01 — K-Nearest Neighbors (KNN)
Course: velpTEC K4.0031 Machine Learning

KNN classifies a new data point by looking at its k nearest neighbours
and taking a majority vote. No explicit training step — the model simply
memorises the training data and computes distances at prediction time.
"""

from sklearn.datasets import make_blobs
from sklearn.model_selection import train_test_split
from sklearn.neighbors import KNeighborsClassifier
from sklearn.metrics import accuracy_score
import matplotlib.pyplot as plt
import numpy as np


# ── a) Generate a synthetic dataset ───────────────────────────────────────────
# make_blobs creates labelled fake data, useful for testing classifiers.
# X = feature matrix (100 rows × 2 columns), y = class labels (0 or 1)
X, y = make_blobs(
    n_samples=100,  # total number of data points
    n_features=2,  # two features so we can plot in 2D
    centers=2,  # two classes (blobs)
    random_state=42,  # fixed seed ensures the same data every run
)


# ── b) Split into training and test data ──────────────────────────────────────
# 70% of the data is used to train the model.
# 30% is held back as test data — the model never sees this during training,
# which gives us an honest measure of how well it generalises to new data.
X_train, X_test, y_train, y_test = train_test_split(
    X,
    y,
    test_size=0.3,  # 30% test, 70% training
    random_state=42,  # fixed seed ensures the same split every run
)


# ── c) Implement the KNN algorithm ────────────────────────────────────────────
# KNeighborsClassifier stores the training data and, at prediction time,
# finds the k=5 closest points and takes a majority vote on the class.
knn_classifier = KNeighborsClassifier(n_neighbors=5)

# .fit() stores the training data — there is no mathematical optimisation here,
# unlike Perceptron or ADALINE. KNN is a "lazy learner".
knn_classifier.fit(X_train, y_train)


# ── d) Evaluate the model ─────────────────────────────────────────────────────
# We predict class labels for the test set and compare against the true labels.
# accuracy = correct predictions / total predictions
y_pred = knn_classifier.predict(X_test)
accuracy = accuracy_score(y_test, y_pred)
print(f"Model accuracy: {accuracy}")


# ── e) Visualise the decision boundary ────────────────────────────────────────
# To draw the decision boundary we colour every point in the background:
# step 1 — define a fine grid of points covering the whole feature space
# step 2 — ask the classifier to predict the class for every grid point
# step 3 — colour each region by its predicted class (contourf)
# step 4 — scatter the actual training and test points on top

# Step 1: build the grid
# step_size controls resolution — smaller = smoother boundary, slower to compute
step_size = 0.02
x_min, x_max = X[:, 0].min() - 1, X[:, 0].max() + 1  # feature 1 range + margin
y_min, y_max = X[:, 1].min() - 1, X[:, 1].max() + 1  # feature 2 range + margin

# np.meshgrid produces two 2D arrays — one for all x-coordinates, one for all y-coordinates
grid_x1, grid_x2 = np.meshgrid(
    np.arange(x_min, x_max, step_size), np.arange(y_min, y_max, step_size)
)

# Step 2: predict the class for every point in the grid
# np.c_ stacks grid_x1 and grid_x2 into a two-column array that knn.predict() expects
# .ravel() flattens each 2D grid into a 1D list first
grid_predictions = knn_classifier.predict(np.c_[grid_x1.ravel(), grid_x2.ravel()])

# Reshape predictions back into the same 2D shape as the grid for plotting
grid_predictions = grid_predictions.reshape(grid_x1.shape)

# Step 3 & 4: plot the coloured regions and scatter the data points
plt.figure()

# contourf fills the background with colours based on the predicted class
plt.contourf(grid_x1, grid_x2, grid_predictions, alpha=0.8)

# Training points shown as circles (marker='o')
plt.scatter(
    X_train[:, 0],
    X_train[:, 1],
    c=y_train,
    edgecolors="k",
    marker="o",
    label="Training data",
)

# Test points shown as triangles (marker='^') so they are visually distinct
plt.scatter(
    X_test[:, 0], X_test[:, 1], c=y_test, edgecolors="k", marker="^", label="Test data"
)

plt.xlabel("Feature 1")
plt.ylabel("Feature 2")
plt.title("KNN Decision Boundary (k=5)")
plt.legend()
plt.show()
