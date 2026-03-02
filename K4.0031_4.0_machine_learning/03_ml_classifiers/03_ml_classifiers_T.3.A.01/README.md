# Logistic Regression — Binary Classification with scikit-learn

**Course:** Machine Learning K4.0031 | **Exercise:** 3.A.01  
**Author:** Oren | **Language:** Python 3 | **Library:** scikit-learn

---

## Table of Contents

1. [Problem Statement](#1-problem-statement)
2. [What is Logistic Regression?](#2-what-is-logistic-regression)
3. [The Pipeline — Step by Step](#3-the-pipeline--step-by-step)
4. [Full Annotated Script](#4-full-annotated-script)
5. [Key Parameters Explained](#5-key-parameters-explained)
6. [Results & Interpretation](#6-results--interpretation)
7. [Design Decisions](#7-design-decisions)

---

## 1. Problem Statement

The goal is to build a binary classifier that can predict which of two classes a data point belongs to, given two numerical features.

Rather than using a real-world dataset, a **synthetic dataset** is generated using scikit-learn's `make_classification` — this is a standard technique in ML development that lets you control the data shape precisely, which is ideal for learning and testing algorithms before applying them to messy real-world data.

**The pipeline covers the full supervised learning workflow:**

- Generate labelled data
- Split into training and test sets
- Standardize features
- Train the model
- Evaluate accuracy
- Visualize the decision boundary

---

## 2. What is Logistic Regression?

Despite the name, **logistic regression is a classification algorithm**, not a regression one. It predicts the probability that a data point belongs to a given class.

### The Core Idea

A linear combination of the input features is computed:

```
z = w₀ + w₁·x₁ + w₂·x₂
```

This value `z` is then passed through the **sigmoid function** (also called the logistic function):

```
σ(z) = 1 / (1 + e^(-z))
```

The sigmoid maps any real number to a value between 0 and 1, which can be interpreted as a **probability**. If `σ(z) ≥ 0.5`, the model predicts class 1; otherwise, class 0.

### Why Not Just Use Linear Regression for Classification?

Linear regression outputs unbounded values (e.g., -300, 7.5, 1000). For classification, we need probabilities between 0 and 1 — the sigmoid function enforces exactly that.

### Decision Boundary

The boundary where `σ(z) = 0.5` corresponds to `z = 0`. This is where the model is equally uncertain between two classes. In a 2-feature problem, this boundary is a **line** (a linear hyperplane).

---

## 3. The Pipeline — Step by Step

### Step a) — Generate Synthetic Data

```python
X, y = make_classification(
    n_samples=100, n_features=2, n_redundant=0, n_informative=2, random_state=1
)
```

- `n_samples=100` — 100 data points
- `n_features=2` — two input features (allows 2D visualization)
- `n_redundant=0` — no noise features that are linear combinations of others
- `n_informative=2` — both features carry useful signal for classification
- `random_state=1` — seeds the random number generator so results are reproducible

`X` is a (100, 2) array of feature values. `y` is a (100,) array of class labels (0 or 1).

---

### Step b) — Train/Test Split

```python
X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=1)
```

80% of the data (80 points) goes to training, 20% (20 points) to testing.

**Why split?** A model trained and evaluated on the same data will appear artificially accurate — it has simply memorised the data. The test set acts as unseen data, giving an honest estimate of real-world performance.

`random_state=1` ensures the same split every run, making results comparable across experiments.

---

### Step c) — Feature Standardization

```python
scaler = StandardScaler()
X_train_std = scaler.fit_transform(X_train)  # compute mean/std from training data, then scale
X_test_std = scaler.transform(X_test)        # apply the same scaling to test data
```

`StandardScaler` transforms each feature to have **mean = 0** and **standard deviation = 1** using:

```
x_scaled = (x - mean) / std
```

**Why standardize?**

Logistic regression uses gradient descent internally. If one feature has values in the range [0, 10000] and another in [0, 1], the algorithm will take much larger steps in one direction, slowing or destabilizing convergence. Standardization puts all features on equal footing.

**Critical rule:** The scaler is **fit only on training data**. The mean and std computed from training data are then applied to the test set. Fitting on the test set would constitute **data leakage** — the model would indirectly "see" test data during training.

---

### Step d) — Train the Model

```python
lr = LogisticRegression(solver='lbfgs', C=1.0, random_state=1)
lr.fit(X_train_std, y_train)
```

`LogisticRegression` is scikit-learn's implementation of the algorithm. Calling `.fit()` runs the optimization process that finds the best weights `w` to separate the two classes.

The solver `lbfgs` (Limited-memory Broyden–Fletcher–Goldfarb–Shanno) is a quasi-Newton optimization algorithm well-suited for small-to-medium datasets. See [Key Parameters](#5-key-parameters-explained) for more on `C`.

---

### Step e) — Evaluate Accuracy

```python
y_pred = lr.predict(X_test_std)           # predict class labels for unseen test data
score = accuracy_score(y_test, y_pred)    # compare predictions to ground truth
print(f"Model accuracy: {score}")
```

`accuracy_score` computes the fraction of correctly classified test points:

```
accuracy = correct predictions / total predictions
```

A score of 0.95 means 95% of test points were classified correctly.

---

### Step f) — Visualize the Decision Boundary

This is the most technically involved step. The goal is to shade the background of a scatter plot to show which region the model assigns to each class.

```python
# 1. Define the grid boundaries (with a 1-unit padding around the data)
x_min, x_max = X_train_std[:, 0].min() - 1, X_train_std[:, 0].max() + 1
y_min, y_max = X_train_std[:, 1].min() - 1, X_train_std[:, 1].max() + 1

# 2. Create a dense grid of points across the feature space
xx, yy = np.meshgrid(np.arange(x_min, x_max, 0.02),
                     np.arange(y_min, y_max, 0.02))

# 3. Predict the class for every point on the grid
Z = lr.predict(np.array([xx.ravel(), yy.ravel()]).T)
Z = Z.reshape(xx.shape)

# 4. Color the background by predicted class, then overlay the actual data points
plt.contourf(xx, yy, Z, alpha=0.4)
plt.scatter(X_train_std[:, 0], X_train_std[:, 1], c=y_train, marker='o', s=20, label='Training data')
plt.scatter(X_test_std[:, 0], X_test_std[:, 1], c=y_test, marker='s', s=20, label='Test data')
plt.xlabel('Feature 1')
plt.ylabel('Feature 2')
plt.legend(loc='upper left')
plt.show()
```

**How the grid works:**

`np.meshgrid` creates two 2D arrays that together represent every (x, y) coordinate on the grid. `.ravel()` flattens them into 1D arrays, `.T` transposes so each row is a coordinate pair `[x, y]`, and the model predicts a class for each. The result is reshaped back into the grid shape and passed to `contourf`, which fills each region with a color.

Training points are plotted as **circles**, test points as **squares** — this allows visual inspection of misclassified examples on both sets.

---

## 4. Full Annotated Script

```python
from sklearn.datasets import make_classification      # synthetic data generator
from sklearn.model_selection import train_test_split  # split data into train/test
from sklearn.preprocessing import StandardScaler      # feature standardization
from sklearn.linear_model import LogisticRegression   # the classifier
from sklearn.metrics import accuracy_score            # evaluation metric
import matplotlib.pyplot as plt                       # plotting
import numpy as np                                    # numerical operations

# a) Generate a synthetic binary classification dataset
X, y = make_classification(
    n_samples=100, n_features=2, n_redundant=0, n_informative=2, random_state=1
)

# b) Split into 80% training and 20% test data
X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=1)

# c) Standardize features (fit only on training data to avoid data leakage)
scaler = StandardScaler()
X_train_std = scaler.fit_transform(X_train)
X_test_std = scaler.transform(X_test)

# d) Train the logistic regression model
lr = LogisticRegression(solver='lbfgs', C=1.0, random_state=1)
lr.fit(X_train_std, y_train)

# e) Evaluate model accuracy on unseen test data
y_pred = lr.predict(X_test_std)
score = accuracy_score(y_test, y_pred)
print(f"Model accuracy: {score}")

# f) Visualize the decision boundary
x_min, x_max = X_train_std[:, 0].min() - 1, X_train_std[:, 0].max() + 1
y_min, y_max = X_train_std[:, 1].min() - 1, X_train_std[:, 1].max() + 1
xx, yy = np.meshgrid(np.arange(x_min, x_max, 0.02),
                     np.arange(y_min, y_max, 0.02))
Z = lr.predict(np.array([xx.ravel(), yy.ravel()]).T)
Z = Z.reshape(xx.shape)

plt.contourf(xx, yy, Z, alpha=0.4)
plt.scatter(X_train_std[:, 0], X_train_std[:, 1], c=y_train, marker='o', s=20, label='Training data')
plt.scatter(X_test_std[:, 0], X_test_std[:, 1], c=y_test, marker='s', s=20, label='Test data')
plt.xlabel('Feature 1')
plt.ylabel('Feature 2')
plt.legend(loc='upper left')
plt.show()
```

---

## 5. Key Parameters Explained

| Parameter | Value | Meaning |
|-----------|-------|---------|
| `solver='lbfgs'` | lbfgs | Optimization algorithm used to find model weights. Efficient for small/medium datasets. |
| `C=1.0` | 1.0 | Inverse of regularization strength. **Low C = stronger regularization** (simpler model, higher bias). **High C = weaker regularization** (more complex model, higher variance). `1.0` is the neutral default. |
| `random_state=1` | 1 | Seeds the random number generator for reproducibility. |
| `test_size=0.2` | 0.2 | 20% of data reserved for testing, 80% for training. |
| `alpha=0.4` | 0.4 | Transparency of the decision region fill in the plot (0 = invisible, 1 = solid). |

### On Regularization and C

Regularization prevents **overfitting** — the tendency of a model to memorize the training data rather than learn general patterns. It adds a penalty term to the loss function that discourages large weights.

```
C = 1 / λ
```

Where `λ` is the regularization strength. Choosing `C`:
- `C = 0.01` → heavy regularization → underfitting risk
- `C = 1.0` → balanced (default)
- `C = 100` → very weak regularization → overfitting risk

In practice, `C` is tuned via cross-validation.

---

## 6. Results & Interpretation

### Decision Boundary Plot

The plot shows a near-vertical linear boundary around `Feature 1 = 0`. Points to the left are classified as class 0 (purple region), points to the right as class 1 (yellow region).

- **Circles** = training data points
- **Squares** = test data points
- Points on the wrong side of the boundary = misclassified examples

The two classes are well-separated in feature space, which is why logistic regression performs well here. A few points near the boundary are misclassified — this is expected and represents the model's natural uncertainty in the ambiguous region.

### What the Accuracy Score Tells Us

An accuracy close to 1.0 (100%) on this dataset indicates the two synthetic classes are largely linearly separable. In a real-world scenario with overlapping classes or noise, accuracy would be lower and additional metrics (precision, recall, F1) would be needed.

---

## 7. Design Decisions

**Why `random_state=1` everywhere?**  
Consistency. Using the same seed for data generation, train/test split, and model initialization ensures that results are fully reproducible — essential for debugging and comparing experiments.

**Why standardize after splitting (not before)?**  
To prevent data leakage. If you standardize the entire dataset first and then split, the test set statistics influence the scaler — the model has indirectly "seen" the test data. Always fit the scaler on training data only.

**Why use a synthetic dataset?**  
Synthetic data gives full control over the problem: number of features, degree of class separation, noise level. This makes it ideal for validating that an implementation is correct before applying it to real, messy data.

**Why `lbfgs` over other solvers?**  
`lbfgs` is the default solver for logistic regression in modern scikit-learn and works well for small-to-medium datasets with L2 regularization. For very large datasets, `saga` (stochastic gradient descent variant) would be preferred.