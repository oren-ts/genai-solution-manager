# K-Nearest Neighbors (KNN) Classifier
### Exercise 3.C.01 — velpTEC K4.0031 Machine Learning

---

## 1. What Is KNN?

K-Nearest Neighbors (KNN) is a **supervised classification algorithm** that belongs to a special category called **lazy learning**. The name "lazy" does not refer to its simplicity — it refers to the fact that KNN does **no mathematical training at all**. Instead, it simply stores every training example and waits until a prediction is requested.

This stands in sharp contrast to algorithms like Perceptron, ADALINE, or Logistic Regression, which learn a set of weights during training and then discard the original data. KNN never discards anything — every prediction requires going back to the full training set.

### Parameterized vs. Non-Parameterized Models

| Type | Examples | How it works |
|------|----------|--------------|
| **Parameterized** | Perceptron, Logistic Regression, Linear SVM | Learns a fixed set of weights from training data; original data can be discarded |
| **Non-parameterized** | Decision Tree, Kernel SVM, KNN | Cannot be described by a fixed set of parameters; model grows with the data |

KNN belongs to a sub-category of non-parameterized models called **instance-based learning** — models that make predictions by comparing new inputs directly against stored training examples.

---

## 2. How the KNN Algorithm Works

The KNN algorithm has three steps:

1. **Define k and select a distance measure** — choose how many neighbours to consult and how to measure distance between points
2. **Find the k nearest neighbours** — locate the k training examples closest to the new data point
3. **Assign a class by majority vote** — whichever class appears most often among the k neighbours wins

### Visual Intuition

Imagine a new, unknown data point `(?)` appears on a 2D plot. With `k=5`, KNN draws a circle around it and counts the classes of the 5 nearest points:

```
k=5 neighbours found:
  1 × cross
  1 × circle
  3 × triangle   ← majority

Prediction: triangle ✓
```

The unknown point is assigned to the **triangle** class because 3 out of 5 neighbours are triangles.

---

## 3. Distance Metrics

KNN's core operation is measuring distance between points. The choice of metric matters — different metrics produce different decision boundaries.

### The Minkowski Metric (Generalised Distance Formula)

$$d\left(\mathbf{x}^{(i)}, \mathbf{x}^{(j)}\right) = \sqrt[p]{\sum_{k} \left| x_k^{(i)} - x_k^{(j)} \right|^p}$$

Where:
- $\mathbf{x}^{(i)}$ and $\mathbf{x}^{(j)}$ are two data points
- $k$ indexes each feature (dimension)
- $p$ controls which specific metric is used

### Special Cases of the Minkowski Metric

| Value of p | Metric | Behaviour |
|-----------|--------|-----------|
| `p = 1` | **Manhattan distance** | Moves along grid lines (like city blocks) |
| `p = 2` | **Euclidean distance** | Straight-line distance (most common choice) |

In scikit-learn, the default is `metric='minkowski'` with `p=2`, which means **Euclidean distance** is used unless specified otherwise.

### Important: Standardisation and Distance

Because KNN measures distances, features with larger numeric ranges will dominate the distance calculation. For example, if Feature 1 ranges from 0–1000 and Feature 2 ranges from 0–1, Feature 1 will completely overwhelm Feature 2.

> **Rule:** Always standardise your data before applying KNN when features have different scales.

In this exercise we use `make_blobs`, which generates already-comparable synthetic data, so standardisation is not required here.

---

## 4. Choosing k — Bias-Variance Trade-off

The value of `k` has a major effect on model behaviour:

| Value of k | Effect | Risk |
|-----------|--------|------|
| **Small k** (e.g., k=1) | Decision boundary is very jagged, fits training data tightly | **Overfitting** — the model memorises noise |
| **Large k** (e.g., k=100) | Decision boundary is very smooth, ignores local structure | **Underfitting** — the model oversimplifies |
| **k=5 (this exercise)** | Moderate smoothness — a standard starting point | Reasonable balance |

> **Rule of thumb:** Start with `k = sqrt(n_samples)` and tune from there.

### Tie-Breaking

When a majority vote results in a tie (e.g., 2 neighbours of each class with k=4), scikit-learn gives preference to the class whose nearest member is closest. If those are also equidistant, the class label that appears first in the training data is selected.

---

## 5. Advantages and Disadvantages

### Advantages
- **No training time** — the model is ready immediately after storing the data
- **Adapts instantly** — adding new training data requires no retraining
- **Simple and intuitive** — easy to understand and explain
- **Non-linear boundaries** — can model complex decision boundaries without a kernel trick

### Disadvantages
- **Slow predictions** — classifying a new point requires computing distance to every training example (O(n) in the worst case)
- **High memory usage** — the entire training dataset must be kept in memory
- **Curse of dimensionality** — in high-dimensional spaces, all points become roughly equidistant, making "nearest neighbour" meaningless

### The Curse of Dimensionality

As the number of features grows, the training data becomes increasingly sparse relative to the feature space. Even the closest neighbours in a high-dimensional space can be so far apart that they provide no meaningful information. For this reason, KNN works best on low-dimensional data, and feature selection or dimensionality reduction techniques should be applied before using KNN on complex datasets.

---

## 6. Implementation

### Imports

```python
from sklearn.datasets import make_blobs
from sklearn.model_selection import train_test_split
from sklearn.neighbors import KNeighborsClassifier
from sklearn.metrics import accuracy_score
import matplotlib.pyplot as plt
import numpy as np
```

> **Note:** The correct spelling in scikit-learn is `KNeighbors` (American English). A common mistake is writing `KNeighbours` (British English), which causes an `ImportError`.

---

### a) Generate a Synthetic Dataset

```python
# make_blobs creates labelled fake data, useful for testing classifiers.
# X = feature matrix (100 rows × 2 columns), y = class labels (0 or 1)
X, y = make_blobs(
    n_samples=100,    # total number of data points
    n_features=2,     # two features so we can plot in 2D
    centers=2,        # two classes (blobs)
    random_state=42   # fixed seed ensures the same data every run
)
```

`make_blobs` generates clusters of normally distributed points. With `centers=2`, it creates two clearly separated groups — an ideal scenario for testing a binary classifier. The `random_state=42` guarantees reproducible results across runs.

---

### b) Split into Training and Test Data

```python
# 70% of the data is used for training, 30% is held back for testing.
# The model never sees test data during training — this gives an honest
# measure of how well the model generalises to new, unseen data.
X_train, X_test, y_train, y_test = train_test_split(
    X,
    y,
    test_size=0.3,    # 30% test, 70% training
    random_state=42   # fixed seed ensures the same split every run
)
```

With 100 samples:
- Training set: 70 samples
- Test set: 30 samples

`random_state=42` ensures the exact same 70/30 split is produced every time the script runs, making results reproducible.

---

### c) Implement the KNN Algorithm

```python
# KNeighborsClassifier stores the training data and, at prediction time,
# finds the k=5 closest points and takes a majority vote on the class.
knn_classifier = KNeighborsClassifier(n_neighbors=5)

# .fit() stores the training data — there is no mathematical optimisation here,
# unlike Perceptron or ADALINE. KNN is a "lazy learner".
knn_classifier.fit(X_train, y_train)
```

Unlike parameterized models, `.fit()` here does not solve any equations or update weights. It simply stores `X_train` and `y_train` in memory so they can be searched during prediction.

**Default parameters in scikit-learn:**

| Parameter | Default | Meaning |
|-----------|---------|---------|
| `n_neighbors` | 5 | Number of neighbours to consult |
| `metric` | `'minkowski'` | Distance formula to use |
| `p` | 2 | Minkowski exponent — `p=2` gives Euclidean distance |

---

### d) Evaluate the Model

```python
# We predict class labels for the test set and compare against the true labels.
# accuracy = correct predictions / total predictions
y_pred = knn_classifier.predict(X_test)
accuracy = accuracy_score(y_test, y_pred)
print(f"Model accuracy: {accuracy}")
```

**Output:**
```
Model accuracy: 1.0
```

The model achieves 100% accuracy on this dataset. This is expected — `make_blobs` with `centers=2` generates two well-separated, non-overlapping clusters with no noise, making the classification task trivial.

In real-world datasets with overlapping classes and noisy data, 100% accuracy would be a red flag for **overfitting**.

---

### e) Visualise the Decision Boundary

The decision boundary shows which class KNN would predict for any possible point in the feature space. To draw it, we colour the entire background of the plot based on predictions.

#### Building the Grid

```python
# step_size controls resolution — smaller = smoother boundary, slower to compute
step_size = 0.02
x_min, x_max = X[:, 0].min() - 1, X[:, 0].max() + 1  # feature 1 range + margin
y_min, y_max = X[:, 1].min() - 1, X[:, 1].max() + 1  # feature 2 range + margin

# np.meshgrid produces two 2D arrays of coordinates covering the entire plot area
grid_x1, grid_x2 = np.meshgrid(
    np.arange(x_min, x_max, step_size),
    np.arange(y_min, y_max, step_size)
)
```

`np.meshgrid` creates a dense grid of coordinate pairs. With `step_size=0.02`, there is a prediction point every 0.02 units — fine enough to produce a smooth-looking boundary.

#### Predicting Every Grid Point

```python
# np.c_ stacks grid_x1 and grid_x2 into a two-column array that knn.predict() expects
# .ravel() flattens each 2D grid into a 1D list first
grid_predictions = knn_classifier.predict(np.c_[grid_x1.ravel(), grid_x2.ravel()])

# Reshape predictions back into the same 2D shape as the grid for plotting
grid_predictions = grid_predictions.reshape(grid_x1.shape)
```

`np.c_` combines two flat arrays column by column, producing the `(n_points, 2)` shape that `predict()` expects. The `.reshape()` call folds the flat predictions back into the 2D grid shape required for `contourf`.

#### Plotting

```python
plt.figure()

# contourf fills the background with colours based on the predicted class
plt.contourf(grid_x1, grid_x2, grid_predictions, alpha=0.8)

# Training points shown as circles (marker='o')
plt.scatter(
    X_train[:, 0], X_train[:, 1],
    c=y_train, edgecolors='k', marker='o', label='Training data'
)

# Test points shown as triangles (marker='^') so they are visually distinct
plt.scatter(
    X_test[:, 0], X_test[:, 1],
    c=y_test, edgecolors='k', marker='^', label='Test data'
)

plt.xlabel('Feature 1')
plt.ylabel('Feature 2')
plt.title('KNN Decision Boundary (k=5)')
plt.legend()
plt.show()
```

The `alpha=0.8` on `contourf` makes the background slightly transparent so the scatter points remain clearly visible on top. Using different markers (`'o'` vs `'^'`) makes it easy to distinguish training from test points at a glance.

---

## 7. Full Script

```python
#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Exercise 3.C.01 — K-Nearest Neighbors (KNN)
Course: velpTEC K4.0031 Machine Learning
"""

from sklearn.datasets import make_blobs
from sklearn.model_selection import train_test_split
from sklearn.neighbors import KNeighborsClassifier
from sklearn.metrics import accuracy_score
import matplotlib.pyplot as plt
import numpy as np


# ── a) Generate a synthetic dataset ───────────────────────────────────────────
X, y = make_blobs(
    n_samples=100,
    n_features=2,
    centers=2,
    random_state=42
)

# ── b) Split into training and test data ──────────────────────────────────────
X_train, X_test, y_train, y_test = train_test_split(
    X, y, test_size=0.3, random_state=42
)

# ── c) Implement the KNN algorithm ────────────────────────────────────────────
knn_classifier = KNeighborsClassifier(n_neighbors=5)
knn_classifier.fit(X_train, y_train)

# ── d) Evaluate the model ─────────────────────────────────────────────────────
y_pred = knn_classifier.predict(X_test)
accuracy = accuracy_score(y_test, y_pred)
print(f"Model accuracy: {accuracy}")

# ── e) Visualise the decision boundary ────────────────────────────────────────
step_size = 0.02
x_min, x_max = X[:, 0].min() - 1, X[:, 0].max() + 1
y_min, y_max = X[:, 1].min() - 1, X[:, 1].max() + 1

grid_x1, grid_x2 = np.meshgrid(
    np.arange(x_min, x_max, step_size),
    np.arange(y_min, y_max, step_size)
)

grid_predictions = knn_classifier.predict(np.c_[grid_x1.ravel(), grid_x2.ravel()])
grid_predictions = grid_predictions.reshape(grid_x1.shape)

plt.figure()
plt.contourf(grid_x1, grid_x2, grid_predictions, alpha=0.8)
plt.scatter(X_train[:, 0], X_train[:, 1], c=y_train,
            edgecolors='k', marker='o', label='Training data')
plt.scatter(X_test[:, 0], X_test[:, 1], c=y_test,
            edgecolors='k', marker='^', label='Test data')
plt.xlabel('Feature 1')
plt.ylabel('Feature 2')
plt.title('KNN Decision Boundary (k=5)')
plt.legend()
plt.show()
```

---

## 8. Key Takeaways

- KNN is a **lazy learner** — it stores training data instead of building a model
- Predictions are made by **majority vote** among the k nearest neighbours
- Distance is measured using the **Minkowski metric**, which generalises both Euclidean (`p=2`) and Manhattan (`p=1`) distance
- The choice of **k controls the bias-variance trade-off** — small k overfits, large k underfits
- KNN **requires standardised data** when features have different scales, because distance calculations are sensitive to magnitude
- KNN is **computationally expensive at prediction time** and is vulnerable to the **curse of dimensionality** in high-dimensional spaces

---

*Course: velpTEC K4.0031 — Machine Learning | Exercise 3.C.01*