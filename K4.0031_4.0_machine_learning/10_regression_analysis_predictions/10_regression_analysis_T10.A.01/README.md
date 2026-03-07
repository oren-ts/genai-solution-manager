# 10.A.01 — Linear Regression with Gradient Descent

**Course:** velpTEC K4.0031 — Machine Learning  
**Topic:** Supervised Learning / Regression  
**Script:** `10_A_01_Regression.py`

---

## Table of Contents

1. [What is Linear Regression?](#1-what-is-linear-regression)
2. [The Regression Line — Mathematical Foundation](#2-the-regression-line--mathematical-foundation)
3. [The Cost Function — Measuring Error](#3-the-cost-function--measuring-error)
4. [Gradient Descent — Finding the Best Weights](#4-gradient-descent--finding-the-best-weights)
5. [Why Standardize?](#5-why-standardize)
6. [Connection to ADALINE](#6-connection-to-adaline)
7. [Full Implementation Walkthrough](#7-full-implementation-walkthrough)
8. [Key Concepts Summary](#8-key-concepts-summary)

---

## 1. What is Linear Regression?

Linear regression is a **supervised learning** algorithm for predicting a **continuous numeric value** — for example, the price of an apartment based on its number of rooms.

> **Analogy:** Imagine drawing the single best-fitting straight line through a scatter plot of data points. Linear regression finds that line mathematically.

It belongs to the **regression** family (not classification), because the output is a real number — not a category like "spam" or "not spam".

### Regression vs. Classification

| | Regression | Classification |
|---|---|---|
| Output | Continuous number | Discrete class label |
| Example | Predict price: 312,000 € | Predict gender: Male / Female |
| Algorithm (this exercise) | LinearRegressionGD | Perceptron, Logistic Regression |

---

## 2. The Regression Line — Mathematical Foundation

The model we want to learn is a straight line:

$$\hat{y} = w_1 x + w_0$$

Where:

| Symbol | Meaning |
|---|---|
| $\hat{y}$ | Predicted value (e.g. apartment price) |
| $x$ | Input feature (e.g. number of rooms) |
| $w_1$ | Feature weight — controls the slope |
| $w_0$ | Bias weight — controls the intercept (shifts the line up or down) |

For multiple features, this generalizes to:

$$\hat{y} = \mathbf{w}^T \mathbf{x} + w_0 = \sum_{j=1}^{m} w_j x_j + w_0$$

In code, this is the `net_input` method:

```python
def net_input(self, X):
    # Dot product of input features with weights, plus the bias
    return np.dot(X, self.weights_[1:]) + self.weights_[0]
```

`self.weights_[1:]` holds the feature weights ($w_1, w_2, ...$) and `self.weights_[0]` is the bias $w_0$.

---

## 3. The Cost Function — Measuring Error

To find the best line, we need a way to measure how wrong our predictions are. We use the **Sum of Squared Errors (SSE)**:

$$J(\mathbf{w}) = \frac{1}{2} \sum_{i=1}^{n} \left( y^{(i)} - \hat{y}^{(i)} \right)^2$$

Where:

| Symbol | Meaning |
|---|---|
| $y^{(i)}$ | True value for training sample $i$ |
| $\hat{y}^{(i)}$ | Predicted value for training sample $i$ |
| $\frac{1}{2}$ | Convenience factor — cancels out cleanly when taking the derivative |

### Why squared errors?

- **Squaring removes negatives** — otherwise positive and negative errors would cancel each other out
- **Squaring penalizes large errors more** — a prediction that's off by 10 contributes 100 to the cost, not just 10
- **The function is convex** — it has exactly one global minimum, so gradient descent is guaranteed to find it

In code:

```python
errors = y - predictions          # How wrong we are for each sample
cost   = (errors ** 2).sum() / 2.0  # Total cost for this epoch
self.cost_per_epoch_.append(cost)
```

---

## 4. Gradient Descent — Finding the Best Weights

The cost function $J(\mathbf{w})$ is a bowl-shaped surface in weight space. Gradient descent navigates this bowl by always stepping in the **downhill direction**.

### The weight update rules

At each epoch, we update the weights using:

$$w_j \leftarrow w_j + \eta \sum_{i} \left( y^{(i)} - \hat{y}^{(i)} \right) x_j^{(i)}$$

$$w_0 \leftarrow w_0 + \eta \sum_{i} \left( y^{(i)} - \hat{y}^{(i)} \right)$$

Where:

| Symbol | Meaning |
|---|---|
| $\eta$ (eta) | Learning rate — how large each step is |
| $\sum_i (y^{(i)} - \hat{y}^{(i)}) x_j^{(i)}$ | Gradient of the cost w.r.t. weight $w_j$ |

> **Intuition:** If our predictions are too low (errors are positive), we increase the weights. If too high (errors are negative), we decrease them. The learning rate controls how aggressively we adjust.

### The learning rate — a critical hyperparameter

| Learning rate too **high** | Learning rate too **low** |
|---|---|
| Overshoots the minimum | Converges very slowly |
| Cost may oscillate or diverge | Needs many more epochs |

In this exercise: `learning_rate = 0.001`, `num_epochs = 20`.

### In code — the full training loop

```python
def fit(self, X, y):
    # Initialize all weights to zero before training begins
    self.weights_ = np.zeros(1 + X.shape[1])
    self.cost_per_epoch_ = []

    for _ in range(self.num_epochs):

        # Step 1: Predict with current weights
        predictions = self.net_input(X)

        # Step 2: Compute how wrong we are
        errors = y - predictions

        # Step 3: Update feature weights (vectorized — updates all features at once)
        self.weights_[1:] += self.learning_rate * X.T.dot(errors)

        # Step 4: Update the bias weight separately
        self.weights_[0]  += self.learning_rate * errors.sum()

        # Step 5: Record the total cost for this epoch
        cost = (errors ** 2).sum() / 2.0
        self.cost_per_epoch_.append(cost)

    return self
```

### Why `X.T.dot(errors)`?

This is a vectorized way to compute $\sum_i e^{(i)} x_j^{(i)}$ for **all features at once**.

- `X` has shape `(5, 1)` — 5 samples, 1 feature
- `X.T` has shape `(1, 5)` — transposed
- `errors` has shape `(5,)` — one error per sample
- `X.T.dot(errors)` produces shape `(1,)` — one gradient per feature

This replaces a nested loop with a single matrix operation. Efficient and Pythonic.

---

## 5. Why Standardize?

Before training, both `X` (rooms) and `y` (prices) are standardized using **z-score normalization**:

$$x_{std} = \frac{x - \mu}{\sigma}$$

Where $\mu$ is the mean and $\sigma$ is the standard deviation. After transformation, each variable has mean = 0 and standard deviation = 1.

### Why is this necessary?

- The gradient descent algorithm is **sensitive to the scale** of the input features
- Without standardization, features on larger scales dominate the weight updates
- Standardized data helps gradient descent converge **faster and more stably**

### Two separate scalers

```python
scaler_rooms  = StandardScaler()
scaler_prices = StandardScaler()

rooms_standardized  = scaler_rooms.fit_transform(rooms)

# y is 1D — StandardScaler needs 2D input
# np.newaxis adds a dimension temporarily, .flatten() removes it after scaling
prices_standardized = scaler_prices.fit_transform(prices[:, np.newaxis]).flatten()
```

> **Important:** We use **two separate scalers** because `rooms` and `prices` have completely different distributions. Each must be scaled relative to its own mean and standard deviation.

### The `np.newaxis` trick explained

```python
prices              # shape: (5,)   — 1D array
prices[:, np.newaxis]  # shape: (5, 1) — 2D column array (StandardScaler requires this)
...fit_transform(...).flatten()  # shape: (5,)  — back to 1D after scaling
```

---

## 6. Connection to ADALINE

Linear Regression with Gradient Descent is structurally **identical to ADALINE** — with one key difference:

| | ADALINE | Linear Regression GD |
|---|---|---|
| Cost function | Sum of Squared Errors | Sum of Squared Errors |
| Weight update rule | Gradient descent on SSE | Gradient descent on SSE |
| Output of `net_input` | Continuous value | Continuous value |
| Final output | **Step function** → class label (-1 or +1) | **No step function** → raw number |
| Use case | Binary classification | Regression |

The course notes make this explicit:

> *"Linear regression with the least squares method can be understood as an Adaline method without a step function, so that we obtain continuous target values instead of the class labels -1 and +1."*

```python
# ADALINE predict — applies step function
def predict(self, X):
    return np.where(self.net_input(X) >= 0.5, 1, 0)  # threshold applied

# Linear Regression predict — no step function needed
def predict(self, X):
    return self.net_input(X)  # return the raw continuous value
```

---

## 7. Full Implementation Walkthrough

### Complete annotated script

```python
"""
10.A.01 - Linear Regression with Gradient Descent
"""

import numpy as np
from sklearn.preprocessing import StandardScaler
import matplotlib.pyplot as plt


# ── 1. Dataset ────────────────────────────────────────────────────────────────

# X must be 2D (shape 5×1) because StandardScaler expects 2D arrays
rooms  = np.array([[5], [4], [6], [3], [7]])
prices = np.array([300, 250, 350, 200, 400])


# ── 2. Standardization ───────────────────────────────────────────────────────

scaler_rooms  = StandardScaler()
scaler_prices = StandardScaler()

rooms_standardized  = scaler_rooms.fit_transform(rooms)
prices_standardized = scaler_prices.fit_transform(prices[:, np.newaxis]).flatten()


# ── 3. Model Definition ──────────────────────────────────────────────────────

class LinearRegressionGD:

    def __init__(self, learning_rate=0.001, num_epochs=20):
        self.learning_rate = learning_rate
        self.num_epochs    = num_epochs

    def fit(self, X, y):
        self.weights_        = np.zeros(1 + X.shape[1])
        self.cost_per_epoch_ = []

        for _ in range(self.num_epochs):
            predictions = self.net_input(X)
            errors      = y - predictions

            self.weights_[1:] += self.learning_rate * X.T.dot(errors)
            self.weights_[0]  += self.learning_rate * errors.sum()

            cost = (errors ** 2).sum() / 2.0
            self.cost_per_epoch_.append(cost)

        return self

    def net_input(self, X):
        return np.dot(X, self.weights_[1:]) + self.weights_[0]

    def predict(self, X):
        return self.net_input(X)


# ── 4. Train the Model ───────────────────────────────────────────────────────

regression_model = LinearRegressionGD()
regression_model.fit(rooms_standardized, prices_standardized)


# ── 5. Visualize the Cost Function ───────────────────────────────────────────

epoch_numbers = range(1, regression_model.num_epochs + 1)

plt.plot(epoch_numbers, regression_model.cost_per_epoch_)
plt.xlabel("Epochs")
plt.ylabel("Sum of Squared Errors")
plt.title("Cost Function over Training Epochs")
plt.tight_layout()
plt.show()
```

### What the plot tells us

The cost function plot shows how the total prediction error changes over each training epoch.

- A **steadily decreasing curve** means the model is learning correctly — gradient descent is working
- A curve that **flattens out** indicates convergence — the weights have stabilized near the minimum
- A curve that **oscillates or increases** would indicate the learning rate is too high

With `learning_rate=0.001` and `num_epochs=20`, the model converges smoothly (as visible in the reference solution output).

---

## 8. Key Concepts Summary

| Concept | Description |
|---|---|
| **Linear Regression** | Supervised learning algorithm for predicting continuous values |
| **Regression line** | $\hat{y} = w_1 x + w_0$ — the model we are fitting |
| **Cost function (SSE)** | $J = \frac{1}{2} \sum (y - \hat{y})^2$ — measures total prediction error |
| **Gradient Descent** | Iterative algorithm that updates weights to reduce cost at each step |
| **Learning rate ($\eta$)** | Controls the size of each weight update step |
| **Epoch** | One full pass through the entire training dataset |
| **Standardization** | Rescaling features to mean=0, std=1 for stable gradient descent |
| **`np.newaxis`** | Adds a dimension to a 1D array so sklearn 2D-expecting methods accept it |
| **`X.T.dot(errors)`** | Vectorized gradient computation — replaces a nested loop |
| **No step function** | What distinguishes regression from ADALINE — output is raw, not thresholded |