# Polynomial Regression
### Exercise 10.Ü.03 — velpTEC K4.0031

---

## Table of Contents

1. [What is Regression?](#1-what-is-regression)
2. [The Problem with Linear Regression](#2-the-problem-with-linear-regression)
3. [What is Polynomial Regression?](#3-what-is-polynomial-regression)
4. [The Math Behind Polynomial Regression](#4-the-math-behind-polynomial-regression)
5. [The PolynomialFeatures Trick](#5-the-polynomialfeatures-trick)
6. [Implementation Step by Step](#6-implementation-step-by-step)
7. [Full Annotated Script](#7-full-annotated-script)
8. [Key Concepts Summary](#8-key-concepts-summary)

---

## 1. What is Regression?

Regression is a **supervised learning** technique used to predict **continuous values** — as opposed to classification, which predicts discrete labels (e.g. "cat" or "dog").

Examples of regression problems:
- Predicting house prices from area and number of rooms
- Forecasting monthly sales revenue
- Estimating a person's age from a photo

In all these cases, the output is a number on a continuous scale, not a category.

---

## 2. The Problem with Linear Regression

A standard linear regression fits a **straight line** through data:

$$\hat{y} = w_0 + w_1 \cdot x$$

Where:
- $w_0$ is the **y-intercept** (where the line crosses the y-axis)
- $w_1$ is the **slope** (how steeply the line rises or falls)
- $\hat{y}$ is the **predicted value**

This works well when the relationship between `X` and `y` is roughly linear. But what if the data looks like this?

```
y
|        *
|      *   *
|    *       *
|  *           *
+-----------------> x
```

A straight line cannot capture this U-shape. No matter how you tilt or shift it, it will always miss large parts of the data. This is called **underfitting** — the model is too simple for the data.

---

## 3. What is Polynomial Regression?

Polynomial regression solves this by adding **higher-order terms** of `X` as new features. Instead of fitting a straight line, we fit a **curve**.

For a **degree 2** polynomial (quadratic):

$$\hat{y} = w_0 + w_1 \cdot x + w_2 \cdot x^2$$

For a **degree 3** polynomial (cubic):

$$\hat{y} = w_0 + w_1 \cdot x + w_2 \cdot x^2 + w_3 \cdot x^3$$

The general form for degree $d$:

$$\hat{y} = w_0 + w_1 x + w_2 x^2 + \cdots + w_d x^d = \sum_{j=0}^{d} w_j x^j$$

> **Key insight:** Even though the curve is non-linear, the model is still called a *linear* regression — because the weights $w_0, w_1, w_2, \ldots$ appear **linearly** in the equation. The non-linearity comes from the *features* ($x^2$, $x^3$), not the weights.

---

## 4. The Math Behind Polynomial Regression

### 4.1 The Target Function in This Exercise

The data in this exercise was generated using the equation:

$$y = 1 + 2x + x^2 + \varepsilon$$

Where $\varepsilon \sim \mathcal{N}(0, 1)$ is **Gaussian noise** — random values drawn from a normal distribution with mean 0 and standard deviation 1.

This means the true underlying relationship is a **quadratic** (degree 2) curve. The noise simulates real-world measurement error.

### 4.2 How the Model Learns — Ordinary Least Squares

Linear regression (and polynomial regression) finds the weights $w$ that **minimise the sum of squared residuals**:

$$\text{MSE} = \frac{1}{n} \sum_{i=1}^{n} \left( y_i - \hat{y}_i \right)^2$$

Where:
- $y_i$ is the **true** target value
- $\hat{y}_i$ is the **predicted** value
- $n$ is the number of data points

The optimal weights can be found analytically with the **Normal Equation**:

$$\mathbf{w} = (\mathbf{X}^T \mathbf{X})^{-1} \mathbf{X}^T \mathbf{y}$$

Scikit-learn handles this internally — you do not need to compute it manually.

### 4.3 What PolynomialFeatures Actually Does

Given a single feature $x$, `PolynomialFeatures(degree=2)` expands it into:

$$[1, \; x, \; x^2]$$

For example, if $x = 3$:

$$[1, \; 3, \; 9]$$

After this transformation, the original 1-column matrix `X` becomes a 3-column matrix `X_poly`:

| Bias ($1$) | $x$ | $x^2$ |
|:---:|:---:|:---:|
| 1 | -2.9 | 8.41 |
| 1 | 0.4 | 0.16 |
| 1 | 2.1 | 4.41 |
| ... | ... | ... |

The bias column of all 1s allows the model to learn the intercept $w_0$.

---

## 5. The PolynomialFeatures Trick

The clever part of sklearn's approach is that it **separates feature transformation from model training**:

```
Step 1: PolynomialFeatures  →  transforms X into [1, X, X²]
Step 2: LinearRegression    →  fits a straight line through the expanded features
```

This means you are technically still running a **linear regression** — just on a richer, expanded feature set. The curve comes from the features, not the model.

### fit_transform vs transform

| Method | When to use | What it does |
|:---|:---|:---|
| `poly.fit_transform(X)` | On **training data** | Learns the structure AND transforms |
| `poly.transform(X_fit)` | On **new data** | Applies the already-learned transformation |

> **Why does this matter?** If you call `fit_transform` on new data, you risk data leakage — the transformer would re-learn from data it should never have seen. Always fit only on training data.

---

## 6. Implementation Step by Step

### Step 1 — Generate Data

```python
np.random.seed(0)  # Ensures the same random numbers every run

# 30 random X values between -3 and 3, shaped as a column for sklearn
X = np.random.uniform(-3, 3, 30).reshape(-1, 1)

# Target values follow y = 1 + 2X + X² plus some random noise
y = 1 + 2 * X + X**2 + np.random.normal(0, 1, X.shape)
```

**Why `reshape(-1, 1)`?**
Scikit-learn expects a 2D array of shape `(n_samples, n_features)`. A flat array of 30 numbers has shape `(30,)` — one-dimensional. Reshaping to `(-1, 1)` gives shape `(30, 1)` — 30 rows, 1 column. The `-1` tells NumPy to calculate that dimension automatically.

**Why `np.random.uniform` and not `np.random.randint`?**
`randint` returns whole numbers only (-3, -2, -1, 0, 1, 2). `uniform` returns decimal values spread across the full range, giving a much richer and more realistic dataset for regression.

**Why `np.random.normal(0, 1, X.shape)`?**
Real-world data always contains measurement noise. This adds small random perturbations to each data point, drawn from a normal distribution with mean $\mu = 0$ and standard deviation $\sigma = 1$.

---

### Step 2 — Perform Polynomial Regression

```python
# Expand X to include a quadratic term: [1, X, X²]
poly = PolynomialFeatures(degree=2)
X_poly = poly.fit_transform(X)  # Fit and transform the training data

# Train a linear regression model on the expanded features
regression_model = LinearRegression()
regression_model.fit(X_poly, y)
```

**What does `PolynomialFeatures(degree=2)` do?**
It creates a transformer object configured to expand features up to degree 2. It has not done anything to the data yet — it just stores the configuration.

**What does `poly.fit_transform(X)` do?**
Two things at once:
1. **fit** — learns the number of features and the degree from `X`
2. **transform** — produces the expanded matrix `[1, X, X²]`

**What does `regression_model.fit(X_poly, y)` do?**
It finds the weights $w_0, w_1, w_2$ that minimise the mean squared error between predictions and true values. After this line, the model knows the equation of the best-fitting parabola.

---

### Step 3 — Visualise Results

```python
# Generate 100 evenly spaced X values for a smooth curve
X_fit = np.linspace(-3, 3, 100).reshape(-1, 1)

# Transform using the same poly object — do NOT fit again
X_fit_poly = poly.transform(X_fit)

# Predict y values for the smooth curve
y_fit = regression_model.predict(X_fit_poly)

# Plot original data points and the fitted polynomial curve
plt.scatter(X, y, color="blue", label="Data points")
plt.plot(X_fit, y_fit, color="red", label="Polynomial regression")
plt.xlabel("X")
plt.ylabel("y")
plt.title("Polynomial regression")
plt.legend()
plt.show()
```

**Why `np.linspace` instead of the original `X`?**
The original 30 `X` values are randomly scattered. If you plotted the predictions on those points, the line would look jagged and uneven. `linspace` generates 100 **evenly spaced** values, so the plotted curve is perfectly smooth.

**Why `poly.transform` and not `poly.fit_transform`?**
The `poly` object was already fitted on the training data. You only need to *apply* the same transformation to the new points — not re-learn it. Using `fit_transform` here would be incorrect and could introduce subtle bugs.

**Why `plt.plot` for the curve and `plt.scatter` for the data points?**
- `plt.scatter` draws individual dots — perfect for showing raw, unordered data points
- `plt.plot` connects values with a line — perfect for showing a smooth, continuous prediction curve

---

## 7. Full Annotated Script

```python
import numpy as np
from sklearn.linear_model import LinearRegression
from sklearn.preprocessing import PolynomialFeatures
import matplotlib.pyplot as plt


# =============================================================
# 1. Generate Data
# =============================================================

np.random.seed(0)  # Ensures the same random numbers every run

# 30 random X values between -3 and 3, shaped as a column for sklearn
X = np.random.uniform(-3, 3, 30).reshape(-1, 1)

# Target values follow y = 1 + 2X + X² plus some random noise
y = 1 + 2 * X + X**2 + np.random.normal(0, 1, X.shape)


# =============================================================
# 2. Perform Polynomial Regression
# =============================================================

# Expand X to include a quadratic term: [1, X, X²]
poly = PolynomialFeatures(degree=2)
X_poly = poly.fit_transform(X)  # Fit and transform the training data

# Train a linear regression model on the expanded features
regression_model = LinearRegression()
regression_model.fit(X_poly, y)


# =============================================================
# 3. Visualise Results
# =============================================================

# Generate 100 evenly spaced X values for a smooth curve
X_fit = np.linspace(-3, 3, 100).reshape(-1, 1)

# Transform using the same poly object — do NOT fit again
X_fit_poly = poly.transform(X_fit)

# Predict y values for the smooth curve
y_fit = regression_model.predict(X_fit_poly)

# Plot original data points and the fitted polynomial curve
plt.scatter(X, y, color="blue", label="Data points")
plt.plot(X_fit, y_fit, color="red", label="Polynomial regression")
plt.xlabel("X")
plt.ylabel("y")
plt.title("Polynomial regression")
plt.legend()
plt.show()
```

---

## 8. Key Concepts Summary

| Concept | Explanation |
|:---|:---|
| **Regression** | Predicts continuous values (not categories) |
| **Underfitting** | Model too simple — a straight line can't fit a curve |
| **Polynomial features** | Adding $x^2$, $x^3$ etc. to enable curve fitting |
| **Degree** | How many polynomial terms to add (degree 2 = quadratic) |
| **fit_transform** | Learn from AND transform training data — used once on training data |
| **transform** | Apply already-learned transformation — used on new/test data |
| **linspace** | Generates evenly spaced values for a smooth plot curve |
| **Gaussian noise** | Random perturbation simulating real-world measurement error |
| **MSE** | Mean Squared Error — the loss function minimised during training |