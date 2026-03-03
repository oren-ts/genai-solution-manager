# SVM Kernel Trick — Non-Linear Classification with RBF Kernel

**Course:** velpTEC K4.0031 — Machine Learning  
**Exercise:** 3.Ü.02 — Support Vector Machines Kernel Trick  
**Script:** `SVM_KernelTrick.py`  
**Libraries:** NumPy, Matplotlib, scikit-learn

---

## Table of Contents

1. [The Problem — Why Linear SVMs Fail](#1-the-problem--why-linear-svms-fail)
2. [Theory — What is the Kernel Trick?](#2-theory--what-is-the-kernel-trick)
3. [The RBF Kernel — Math and Intuition](#3-the-rbf-kernel--math-and-intuition)
4. [Hyperparameters — C and Gamma](#4-hyperparameters--c-and-gamma)
5. [Part a) — Generating the XOR Dataset](#5-part-a--generating-the-xor-dataset)
6. [Part b) — Training the RBF Kernel SVM](#6-part-b--training-the-rbf-kernel-svm)
7. [Part c) — Visualizing the Decision Boundary](#7-part-c--visualizing-the-decision-boundary)
8. [Full Script](#8-full-script)
9. [Output and Interpretation](#9-output-and-interpretation)
10. [Key Takeaways](#10-key-takeaways)

---

## 1. The Problem — Why Linear SVMs Fail

A standard linear SVM finds the optimal hyperplane that separates two classes with the maximum possible margin. In two dimensions, this hyperplane is simply a straight line. The decision function takes the form:

```
f(x) = w · x + b
```

Where `w` is the weight vector, `x` is the input, and `b` is the bias. The SVM classifies a point as class `+1` if `f(x) >= 0` and class `-1` if `f(x) < 0`.

This works well when data is **linearly separable** — meaning a straight line can cleanly divide the two classes. However, many real-world problems are not linearly separable.

### The XOR Problem

The XOR (exclusive OR) pattern is a classic example of a non-linearly separable dataset. The logic is:

| Feature 1 (x) | Feature 2 (y) | XOR result | Class Label |
|---|---|---|---|
| Positive (+) | Positive (+) | False | -1 |
| Positive (+) | Negative (-) | True | +1 |
| Negative (-) | Positive (+) | True | +1 |
| Negative (-) | Negative (-) | False | -1 |

Class `+1` occupies the **top-left and bottom-right** quadrants. Class `-1` occupies the **top-right and bottom-left** quadrants. No single straight line can separate these two groups — they are interleaved diagonally.

---

## 2. Theory — What is the Kernel Trick?

### The Core Idea

When data is not linearly separable in its original feature space, the kernel trick solves this by **implicitly mapping the data into a higher-dimensional space** where it *can* be linearly separated.

Imagine taking a 2D dataset and projecting it into 3D. What was a tangled mess in 2D might become cleanly separable in 3D by a flat plane (hyperplane). When that hyperplane is projected *back* into 2D, it becomes a curved non-linear boundary.

The mathematical transformation that maps data from the original space to the higher-dimensional space is represented by the function `φ` (phi):

```
φ : x ∈ ℝᵈ  →  φ(x) ∈ ℝᴰ    where D >> d
```

### The Problem with Explicit Transformation

Explicitly computing `φ(x)` is extremely computationally expensive, especially with high-dimensional data. The transformed feature space can have thousands or even infinite dimensions.

### The Trick

The SVM optimization problem only ever requires the **dot product** of pairs of data points — never the individual transformed vectors themselves. The kernel function `k` computes this dot product *directly in the original space*, without ever explicitly transforming the data:

```
k(x⁽ⁱ⁾, x⁽ʲ⁾) = φ(x⁽ⁱ⁾) · φ(x⁽ʲ⁾)
```

This is the kernel trick: **replace the expensive dot product in high-dimensional space with a cheap kernel function in the original space.** The result is identical, but the computation is orders of magnitude faster.

---

## 3. The RBF Kernel — Math and Intuition

### The Formula

The Radial Basis Function (RBF) kernel, also called the Gaussian kernel, is the most widely used kernel in practice. Its formula is:

```
k(x⁽ⁱ⁾, x⁽ʲ⁾) = exp(−γ · ‖x⁽ⁱ⁾ − x⁽ʲ⁾‖²)
```

Where:
- `x⁽ⁱ⁾` and `x⁽ʲ⁾` are two data points
- `‖x⁽ⁱ⁾ − x⁽ʲ⁾‖²` is the squared Euclidean distance between them
- `γ` (gamma) is a free parameter that controls the shape of the boundary
- `exp` is the exponential function

### Intuition — A Similarity Measure

The RBF kernel can be understood as a **similarity function** between two data points:

- The `−` sign converts distance into similarity — points that are close together have a *large* kernel value (near 1), and points that are far apart have a *small* kernel value (near 0)
- The exponential term ensures the output is always between 0 and 1:
  - Two identical points: `exp(0) = 1` → maximum similarity
  - Two very distant points: `exp(−∞) → 0` → minimum similarity

In other words, the RBF kernel asks: *"How similar are these two points based on their distance?"* The SVM then uses this similarity information to build a decision boundary.

---

## 4. Hyperparameters — C and Gamma

The RBF kernel SVM has two key hyperparameters that must be chosen carefully.

### The C Parameter — Regularization

`C` controls the trade-off between maximizing the margin and minimizing misclassification errors:

- **High C** (e.g., `C=10.0`): The model is penalized heavily for misclassifications. It tries hard to classify every training point correctly, producing a tighter and potentially more complex boundary. Risk: overfitting.
- **Low C** (e.g., `C=0.1`): The model accepts more misclassifications in exchange for a wider, smoother margin. Risk: underfitting.

```python
# High C — tight boundary, low tolerance for errors
svm_classifier = SVC(kernel='rbf', C=10.0, gamma=0.10)

# Low C — wide margin, more misclassifications accepted
svm_classifier = SVC(kernel='rbf', C=0.1, gamma=0.10)
```

### The Gamma Parameter — Boundary Smoothness

`gamma` controls the **reach of influence** of each training point:

- **Low gamma** (e.g., `gamma=0.10`): Each training point influences a wide area. The decision boundary is smooth and broad.
- **High gamma** (e.g., `gamma=10.0`): Each training point only influences a very small area around it. The decision boundary becomes tight and wiggly, closely hugging individual data points. Risk: overfitting.

```python
# Low gamma — smooth, broad boundary
svm_classifier = SVC(kernel='rbf', C=10.0, gamma=0.10)

# High gamma — tight, wiggly boundary
svm_classifier = SVC(kernel='rbf', C=10.0, gamma=10.0)
```

For this exercise, `gamma=0.10` and `C=10.0` produce a well-balanced decision boundary that separates the XOR pattern without overfitting.

---

## 5. Part a) — Generating the XOR Dataset

### Goal
Generate 200 random 2D data points and assign class labels of `1` and `-1` according to XOR logic.

### Code

```python
# Fix the random state so results are reproducible across runs
np.random.seed(1)

# Generate 200 random points with 2 features (x and y coordinates)
# np.random.randn draws from a standard normal distribution (mean=0, std=1)
xor_data_points = np.random.randn(200, 2)

# Apply XOR logic: a point is True if exactly one of its features is positive
# data[:, 0] > 0  →  checks whether the x-coordinate is positive
# data[:, 1] > 0  →  checks whether the y-coordinate is positive
# logical_xor returns True only when exactly one of these conditions is True
xor_boolean_labels = np.logical_xor(xor_data_points[:, 0] > 0,
                                     xor_data_points[:, 1] > 0)

# Convert the boolean array to class labels: True → 1, False → -1
xor_class_labels = np.where(xor_boolean_labels, 1, -1)
```

### Step-by-Step Explanation

**`np.random.randn(200, 2)`** creates a 200×2 array. Each row is one data point with two features (x and y). Values are drawn from a standard normal distribution, so most points cluster around the origin.

**`np.logical_xor(condition_A, condition_B)`** returns `True` when exactly one condition is `True`:

```
condition_A: x > 0   →  [True,  False, True,  False, ...]
condition_B: y > 0   →  [True,  True,  False, False, ...]
XOR result:           →  [False, True,  True,  False, ...]
```

**`np.where(condition, 1, -1)`** converts booleans to numeric class labels:

```
[False, True, True, False, ...]  →  [-1, 1, 1, -1, ...]
```

---

## 6. Part b) — Training the RBF Kernel SVM

### Goal
Train an SVM with an RBF kernel on the XOR dataset using appropriate hyperparameters.

### Code

```python
# Create the SVM classifier with RBF kernel
# kernel='rbf'     — use the Radial Basis Function kernel for non-linear boundaries
# random_state=1   — ensures reproducible results
# gamma=0.10       — low value = smooth decision boundary
# C=10.0           — high value = low tolerance for misclassification errors
svm_classifier = SVC(kernel='rbf', random_state=1, gamma=0.10, C=10.0)

# Train the classifier on the XOR data
# The SVM learns the optimal curved decision boundary during this step
svm_classifier.fit(xor_data_points, xor_class_labels)
```

### What Happens During `.fit()`?

During training, the SVM solves a quadratic optimization problem to find the **support vectors** — the data points closest to the decision boundary. The RBF kernel computes the similarity between every pair of training points using the formula from Section 3, and the optimizer finds the boundary that maximizes the margin between classes in the higher-dimensional space.

---

## 7. Part c) — Visualizing the Decision Boundary

### Goal
Plot the curved decision boundary learned by the RBF SVM, with data points colored by class.

### Strategy

To visualize a decision boundary, you cannot simply draw a line. Instead, you must:

1. Create a fine grid of points covering the entire plot area
2. Ask the trained classifier to predict the class for every grid point
3. Color each grid point according to its predicted class — this creates the background regions
4. Overlay the actual data points on top

### The Full Visualization Function

```python
def plot_decision_regions(data_points, class_labels, classifier, resolution=0.02):
    # Define marker shapes and a colormap — one per class
    markers = ('s', 'x', 'o', '^', 'v')
    cmap = plt.cm.brg  # Blue-Red-Green colormap

    # ── Step 1: Define the grid boundaries ───────────────────────────────────
    # Find the min and max of each feature, with +/-1 buffer for padding
    x1_min, x1_max = data_points[:, 0].min() - 1, data_points[:, 0].max() + 1
    x2_min, x2_max = data_points[:, 1].min() - 1, data_points[:, 1].max() + 1

    # ── Step 2: Create the mesh grid ─────────────────────────────────────────
    # np.meshgrid creates a full grid of coordinate pairs
    # resolution=0.02 means one grid point every 0.02 units — a fine grid
    grid_x1, grid_x2 = np.meshgrid(np.arange(x1_min, x1_max, resolution),
                                    np.arange(x2_min, x2_max, resolution))

    # ── Step 3: Predict the class for every grid point ────────────────────────
    # .ravel() flattens the 2D grid into a 1D list
    # np.array([...]).T reshapes into (n_points, 2) — one [x, y] pair per row
    grid_predictions = classifier.predict(
        np.array([grid_x1.ravel(), grid_x2.ravel()]).T
    )
    # Reshape predictions back into the grid shape for plotting
    grid_predictions = grid_predictions.reshape(grid_x1.shape)

    # ── Step 4: Draw the colored background regions ───────────────────────────
    # contourf fills regions with color based on predicted class
    # alpha=0.4 makes it semi-transparent so data points are visible on top
    plt.contourf(grid_x1, grid_x2, grid_predictions, alpha=0.4, cmap=cmap)
    plt.xlim(grid_x1.min(), grid_x1.max())
    plt.ylim(grid_x2.min(), grid_x2.max())

    # ── Step 5: Plot the actual data points on top ────────────────────────────
    # Loop through each unique class label and scatter plot its points
    for class_index, class_label in enumerate(np.unique(class_labels)):
        plt.scatter(
            x=data_points[class_labels == class_label, 0],  # x-coords for this class
            y=data_points[class_labels == class_label, 1],  # y-coords for this class
            alpha=0.8,
            c=[cmap(class_index)],       # assign a distinct color per class
            marker=markers[class_index], # assign a distinct marker shape per class
            label=class_label            # used by plt.legend()
        )
```

### Key Concepts in the Visualization

**`np.meshgrid`** — creates a grid of coordinate pairs. Think of it like graph paper: `grid_x1` holds all x-coordinates and `grid_x2` holds all y-coordinates for every intersection point on the paper.

**`.ravel()`** — flattens a 2D array into a 1D list so it can be passed to the classifier:
```
[[1, 2],              [1, 2, 3, 4]
 [3, 4]]    →
```

**`.T` (transpose)** — rotates the array so each row is one `[x, y]` coordinate pair, which is the format `classifier.predict()` expects:
```
Before .T:           After .T:
[[1, 2, 3, 4],  →   [[1, 5],
 [5, 6, 7, 8]]       [2, 6],
                      [3, 7],
                      [4, 8]]
```

**Boolean filtering `data_points[class_labels == class_label]`** — selects only the rows belonging to the current class during scatter plotting.

---

## 8. Full Script

```python
import numpy as np
import matplotlib.pyplot as plt
from sklearn.svm import SVC

# ── Part c) Decision boundary visualisation function ──────────────────────────

def plot_decision_regions(data_points, class_labels, classifier, resolution=0.02):
    # Define marker shapes and a colormap for the two classes
    markers = ('s', 'x', 'o', '^', 'v')
    cmap = plt.cm.brg

    # Find the min/max range of each feature to define the plot boundaries
    x1_min, x1_max = data_points[:, 0].min() - 1, data_points[:, 0].max() + 1
    x2_min, x2_max = data_points[:, 1].min() - 1, data_points[:, 1].max() + 1

    # Create a fine grid of points covering the entire plot area
    grid_x1, grid_x2 = np.meshgrid(np.arange(x1_min, x1_max, resolution),
                                    np.arange(x2_min, x2_max, resolution))

    # Predict the class for every point on the grid to create the background regions
    grid_predictions = classifier.predict(
        np.array([grid_x1.ravel(), grid_x2.ravel()]).T
    )
    grid_predictions = grid_predictions.reshape(grid_x1.shape)

    # Draw the colored background regions
    plt.contourf(grid_x1, grid_x2, grid_predictions, alpha=0.4, cmap=cmap)
    plt.xlim(grid_x1.min(), grid_x1.max())
    plt.ylim(grid_x2.min(), grid_x2.max())

    # Plot each class's data points with a distinct marker and color
    for class_index, class_label in enumerate(np.unique(class_labels)):
        plt.scatter(
            x=data_points[class_labels == class_label, 0],
            y=data_points[class_labels == class_label, 1],
            alpha=0.8, c=[cmap(class_index)],
            marker=markers[class_index], label=class_label
        )

# ── Part a) Generate XOR dataset ──────────────────────────────────────────────

np.random.seed(1)  # Fix random state so results are reproducible

xor_data_points = np.random.randn(200, 2)  # 200 random points with 2 features (x and y)

# XOR logic: a point is "true" if exactly one of its two features is positive
xor_boolean_labels = np.logical_xor(xor_data_points[:, 0] > 0,
                                     xor_data_points[:, 1] > 0)

# Convert True/False to class labels 1 and -1
xor_class_labels = np.where(xor_boolean_labels, 1, -1)

# ── Part b) Train SVM with RBF kernel ─────────────────────────────────────────

# RBF kernel handles non-linear boundaries; C controls penalty, gamma controls reach
svm_classifier = SVC(kernel='rbf', random_state=1, gamma=0.10, C=10.0)
svm_classifier.fit(xor_data_points, xor_class_labels)

# ── Part c) Visualise decision boundary ───────────────────────────────────────

plot_decision_regions(xor_data_points, xor_class_labels, classifier=svm_classifier)
plt.legend(loc='upper left')
plt.tight_layout()
plt.show()
```

---

## 9. Output and Interpretation

The script produces a scatter plot showing:

- **Green regions** — areas predicted as class `+1` (top-left and bottom-right quadrants)
- **Purple regions** — areas predicted as class `-1` (top-right and bottom-left quadrants)
- **Curved red boundary** — the non-linear decision boundary learned by the RBF SVM
- **Square markers (■)** — class `-1` data points
- **Cross markers (×)** — class `+1` data points

The curved S-shaped boundary confirms that the RBF kernel has successfully learned the XOR pattern — something that would be impossible with a linear kernel.

---

## 10. Key Takeaways

| Concept | Summary |
|---|---|
| XOR Problem | A non-linearly separable dataset — no straight line can divide the two classes |
| Kernel Trick | Implicitly maps data to higher dimensions using `k(xᵢ, xⱼ) = φ(xᵢ) · φ(xⱼ)` |
| RBF Kernel | `k(xᵢ, xⱼ) = exp(−γ · ‖xᵢ − xⱼ‖²)` — a distance-based similarity function |
| `gamma` | Controls boundary smoothness — low = smooth, high = tight and wiggly |
| `C` | Controls misclassification penalty — high = tight fit, low = wider margin |
| `np.logical_xor` | Applies XOR logic element-wise across two boolean arrays |
| `np.meshgrid` | Creates a coordinate grid for visualizing the decision boundary |
| `classifier.predict()` | Classifies every grid point to generate the colored background regions |

---

## Libraries Used

| Library | Purpose |
|---|---|
| `numpy` | Dataset generation, XOR logic, array operations |
| `matplotlib.pyplot` | Decision boundary visualization and scatter plotting |
| `sklearn.svm.SVC` | SVM classifier with RBF kernel support |