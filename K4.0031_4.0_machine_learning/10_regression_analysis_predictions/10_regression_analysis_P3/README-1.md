# Simple Linear Regression with scikit-learn

## Introduction

This script trains a simple linear regression model on a synthetically generated dataset. The dataset consists of 100 data points with a linear relationship between an independent variable X and a dependent variable Y, with a random noise term added. The model is trained using sklearn's `LinearRegression` class and evaluated using the R² score.

---

## Dataset Generation

100 evenly spaced values are generated for X using `np.linspace()`. The target Y is defined by the linear equation `Y = 2X + 1` with noise drawn from a normal distribution (mean=0, std=1). X is reshaped to `(100, 1)` to meet sklearn's requirement for a 2D input array.

```python
X = np.linspace(0, 10, 100)
noise = np.random.normal(0, 1, 100)
Y = 2 * X + 1 + noise
X = X.reshape(-1, 1)
```

---

## Task a) Scatter Plot — Raw Data

A scatter plot is created to visualize the generated data before any model is applied.

```python
plt.scatter(X, Y)
plt.xlabel("X (Independent Variable)")
plt.ylabel("Y (Dependent Variable)")
plt.title("Generated Dataset with Linear Relationship and Noise")
plt.show()
```

---

## Task b) Train / Test Split

The dataset is split into 80% training data (80 samples) and 20% test data (20 samples). `random_state=42` ensures the split is identical on every run.

```python
X_train, X_test, Y_train, Y_test = train_test_split(
    X, Y,
    test_size=0.2,
    random_state=42
)
```

---

## Task c) Train the Model

A `LinearRegression` model is created and fitted on the training data only. Fitting on training data only prevents data leakage — using test data during training would inflate performance metrics.

```python
linear_model = LinearRegression()
linear_model.fit(X_train, Y_train)
```

---

## Task d) Model Evaluation — R² Score

The model is evaluated on the test set using the R² score. R² measures how well the regression line explains the variation in Y, where 1.0 is a perfect fit.

$$R^2 = 1 - \frac{\sum(y_i - \hat{y}_i)^2}{\sum(y_i - \bar{y})^2}$$

```python
Y_pred = linear_model.predict(X_test)
r2_score = linear_model.score(X_test, Y_test)
print("R² score:", r2_score)
```

**Result:**

| Metric | Value |
|--------|-------|
| R² Score | ≈ 0.98 |

---

## Task e) Plot Regression Line with Test Data

The regression line is plotted together with the test data points to visualize model fit.

```python
plt.scatter(X_test, Y_test, label="Test Data")
plt.plot(X_test, Y_pred, label="Regression Line")
plt.xlabel("X (Independent Variable)")
plt.ylabel("Y (Dependent Variable)")
plt.title("Linear Regression Model on Test Data")
plt.legend()
plt.show()
```

---

## Complete Script

```python
import numpy as np
import matplotlib.pyplot as plt
from sklearn.model_selection import train_test_split
from sklearn.linear_model import LinearRegression

# ----------------------------- DATA GENERATION -----------------------------

X = np.linspace(0, 10, 100)
noise = np.random.normal(0, 1, 100)
Y = 2 * X + 1 + noise
X = X.reshape(-1, 1)


# ----------------------------- VISUALIZE RAW DATA --------------------------

plt.scatter(X, Y)
plt.xlabel("X (Independent Variable)")
plt.ylabel("Y (Dependent Variable)")
plt.title("Generated Dataset with Linear Relationship and Noise")
plt.show()


# ----------------------------- TRAIN / TEST SPLIT --------------------------

X_train, X_test, Y_train, Y_test = train_test_split(
    X, Y,
    test_size=0.2,
    random_state=42
)


# ----------------------------- TRAIN THE MODEL -----------------------------

linear_model = LinearRegression()
linear_model.fit(X_train, Y_train)


# ----------------------------- EVALUATE THE MODEL --------------------------

Y_pred = linear_model.predict(X_test)
r2_score = linear_model.score(X_test, Y_test)
print("R² score:", r2_score)


# ----------------------------- PLOT RESULTS --------------------------------

plt.scatter(X_test, Y_test, label="Test Data")
plt.plot(X_test, Y_pred, label="Regression Line")
plt.xlabel("X (Independent Variable)")
plt.ylabel("Y (Dependent Variable)")
plt.title("Linear Regression Model on Test Data")
plt.legend()
plt.show()
```