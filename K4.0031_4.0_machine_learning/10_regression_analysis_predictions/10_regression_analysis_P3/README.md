# Linear Regression — Simple Linear Regression with scikit-learn

**Course:** velpTEC K4.0031 — Machine Learning  
**Exercise:** 10.Ü.02 — Partial Exam 3  
**Topic:** Supervised Learning — Regression  

---

## Table of Contents

1. [What is Linear Regression?](#1-what-is-linear-regression)
2. [The Mathematical Model](#2-the-mathematical-model)
3. [The Cost Function — Ordinary Least Squares](#3-the-cost-function--ordinary-least-squares)
4. [R² — Coefficient of Determination](#4-r²--coefficient-of-determination)
5. [Implementation Walkthrough](#5-implementation-walkthrough)
   - [a) Data Generation](#a-data-generation)
   - [b) Scatter Plot — Raw Data](#b-scatter-plot--raw-data)
   - [c) Train/Test Split](#c-traintest-split)
   - [d) Training the Model](#d-training-the-model)
   - [e) Model Evaluation — R² Score](#e-model-evaluation--r²-score)
   - [f) Plotting the Regression Line](#f-plotting-the-regression-line)
6. [Complete Script](#6-complete-script)

---

## 1. What is Linear Regression?

Linear regression is one of the oldest and most widely used algorithms in machine learning and statistics. It belongs to the family of **supervised learning** algorithms, meaning the model learns from labeled data — data where we already know the correct output.

The goal of linear regression is simple: **find the best-fitting straight line through a set of data points**.

Imagine you have data about house sizes and prices. Linear regression would find the line that best describes the relationship between size (input) and price (output), so you can predict the price of a house you've never seen before.

**Key terminology:**
- **Independent variable (X):** The input feature — what we use to make a prediction
- **Dependent variable (Y):** The output — what we are trying to predict
- **Regression line:** The straight line the model learns
- **Residuals:** The vertical distances between the actual data points and the regression line — the prediction errors

---

## 2. The Mathematical Model

A simple linear regression model with one input feature is described by the equation:

```
Ŷ = w₁ · X + w₀
```

Where:
- `Ŷ` (Y-hat) — the **predicted** value of Y
- `X` — the independent variable (input)
- `w₁` — the **slope** (weight/coefficient for X): how much Y changes when X increases by 1
- `w₀` — the **intercept** (bias): the value of Y when X = 0

This is identical to the equation of a straight line from basic algebra (`y = mx + b`), where `m = w₁` and `b = w₀`.

### How the dataset was generated

In this exercise, we generated synthetic data using a known linear relationship with added random noise:

```
Y = 2 · X + 1 + noise
```

This means:
- The **true slope** is `w₁ = 2`
- The **true intercept** is `w₀ = 1`
- The **noise** is a random disturbance drawn from a normal distribution with mean 0 and standard deviation 1

In the real world, data is never perfectly linear — there is always some noise or unexplained variation. Adding noise to synthetic data simulates this reality and makes the learning task more realistic.

---

## 3. The Cost Function — Ordinary Least Squares

The model needs a way to measure how wrong its predictions are, so it can adjust the weights `w₀` and `w₁` to minimize those errors. This measurement is called the **cost function**.

Linear regression uses the **Sum of Squared Errors (SSE)**, also called **Ordinary Least Squares (OLS)**:

```
SSE = Σ (yᵢ - ŷᵢ)²
```

For each data point `i`:
- `yᵢ` — the **actual** value
- `ŷᵢ` — the **predicted** value
- `(yᵢ - ŷᵢ)` — the residual (prediction error)
- `(yᵢ - ŷᵢ)²` — the squared error (squaring removes negative signs so errors don't cancel out)

The model finds the values of `w₀` and `w₁` that **minimize** this total squared error. This is why it is called "least squares."

**Why square the errors?**
- Squaring makes all errors positive — an error of -3 and +3 are equally bad
- Squaring penalizes large errors more heavily than small ones
- The squared function is smooth and differentiable, making it easy to minimize mathematically

In practice, sklearn's `LinearRegression` uses an optimized implementation of least squares under the hood — you do not need to implement the minimization manually.

---

## 4. R² — Coefficient of Determination

Once the model is trained, we need to measure how well it performs. For regression, the most common metric is **R²** (R-squared), also called the **coefficient of determination**.

### Formula

```
R² = 1 - (SS_res / SS_tot)
```

Where:
- `SS_res` = Σ (yᵢ - ŷᵢ)² — **residual sum of squares** (errors from the model's predictions)
- `SS_tot` = Σ (yᵢ - ȳ)² — **total sum of squares** (errors from simply predicting the mean ȳ)

### Interpretation

| R² Value | Meaning |
|----------|---------|
| R² = 1.0 | Perfect fit — the model explains all variation in Y |
| R² = 0.0 | No better than predicting the mean of Y |
| R² < 0.0 | Worse than predicting the mean (poor model) |
| R² ≈ 0.95 | The model explains 95% of the variation in Y |

For clean, synthetically generated data like in this exercise, we expect an R² value very close to 1.0 — because the underlying relationship really is linear.

---

## 5. Implementation Walkthrough

### a) Data Generation

**Theory:**  
We generate 100 data points with `np.linspace()`, which creates evenly spaced values. The target `Y` is defined by the known linear equation `Y = 2X + 1`, with noise added from `np.random.normal()`.

sklearn's `LinearRegression` requires `X` to be **2-dimensional** — a matrix with shape `(n_samples, n_features)`. Even with a single feature, we must reshape `X` from `(100,)` to `(100, 1)` using `.reshape(-1, 1)`. The `-1` tells NumPy to calculate that dimension automatically.

```python
import numpy as np

# Generate 100 evenly spaced values between 0 and 10
X = np.linspace(0, 10, 100)

# Generate noise from a normal distribution (mean=0, std=1)
noise = np.random.normal(0, 1, 100)

# Create the target variable with a linear relationship
Y = 2 * X + 1 + noise

# Reshape X to make it compatible with sklearn (100 rows, 1 feature)
X = X.reshape(-1, 1)
```

**What this produces:**
- `X`: values from 0.0 to 10.0, shape `(100, 1)`
- `Y`: values roughly between 1 and 21, with small random deviations around the line `2X + 1`
- `noise`: 100 random values centered around 0

---

### b) Scatter Plot — Raw Data

**Theory:**  
Before training any model, it is always good practice to **visualize the raw data**. A scatter plot shows each data point as a dot at position `(X, Y)`. This helps us verify the linear relationship is visible and understand the spread of the data before applying any algorithm.

```python
import matplotlib.pyplot as plt

# Create a scatter plot of the generated dataset
plt.scatter(X, Y)

# Label the axes
plt.xlabel("X (Independent Variable)")
plt.ylabel("Y (Dependent Variable)")

# Add a title
plt.title("Generated Dataset with Linear Relationship and Noise")

# Display the plot
plt.show()
```

**What we expect to see:** A cloud of points that roughly follows a diagonal line from bottom-left to top-right, with small deviations caused by the noise term.

---

### c) Train/Test Split

**Theory:**  
We must never evaluate a model on the same data it was trained on — this would give an overly optimistic result that does not reflect real-world performance. Instead, we split the dataset:
- **Training set (80%):** Used to fit the model — the model learns from this data
- **Test set (20%):** Held back and only used after training to evaluate how well the model generalizes

With 100 data points:
- 80 samples → training
- 20 samples → testing

`random_state=42` ensures the split is reproducible — every run produces the same split.

```python
from sklearn.model_selection import train_test_split

# Split the dataset into training (80%) and testing (20%)
X_train, X_test, Y_train, Y_test = train_test_split(
    X, Y,
    test_size=0.2,
    random_state=42
)
```

**Result:**
- `X_train`: shape `(80, 1)` — 80 input samples for training
- `X_test`: shape `(20, 1)` — 20 input samples for testing
- `Y_train`: shape `(80,)` — 80 target values for training
- `Y_test`: shape `(20,)` — 20 target values for testing

---

### d) Training the Model

**Theory:**  
`LinearRegression` from sklearn finds the optimal weights `w₀` (intercept) and `w₁` (slope) by minimizing the Sum of Squared Errors using the **Ordinary Least Squares** method.

Internally, sklearn solves this using an efficient matrix formula:

```
w = (XᵀX)⁻¹ Xᵀy
```

This is called the **Normal Equation** — a closed-form mathematical solution that directly computes the best weights without iterating. Unlike gradient descent (which we used in ADALINE), this method finds the exact solution in one calculation.

The `.fit()` method does all of this automatically when called on the training data.

```python
from sklearn.linear_model import LinearRegression

# Create the linear regression model
linear_model = LinearRegression()

# Train (fit) the model using the training data only
linear_model.fit(X_train, Y_train)
```

**What happens during `.fit()`:**
1. sklearn solves the Normal Equation using the 80 training samples
2. It stores the learned weights internally:
   - `linear_model.coef_` → the learned slope `w₁` (should be close to 2.0)
   - `linear_model.intercept_` → the learned intercept `w₀` (should be close to 1.0)

**Important:** We fit the model on `X_train` and `Y_train` only — never on the full dataset. Using test data during training would constitute **data leakage** and inflate performance metrics.

---

### e) Model Evaluation — R² Score

**Theory:**  
After training, we evaluate the model on the **test set** — data the model has never seen. We use `.predict()` to generate predictions and `.score()` to compute R².

`.score()` on a `LinearRegression` object computes R² directly:
```
R² = 1 - (SS_res / SS_tot)
```

A value close to 1.0 means the model captures the linear relationship well.

```python
# Generate predictions for the test dataset
Y_pred = linear_model.predict(X_test)

# Calculate and print the R² score on the test dataset
r2_score = linear_model.score(X_test, Y_test)
print("R² score:", r2_score)
```

**Expected output:**  
Something close to `R² score: 0.98` or higher, because the data was generated with a clean linear relationship. The small deviation from 1.0 is caused by the noise term.

**Why use the test set for evaluation?**  
The model was optimized on the training set, so its training R² would be artificially high. The test R² tells us how well the model generalizes to data it has not seen before — which is what matters in practice.

---

### f) Plotting the Regression Line

**Theory:**  
The final step is to visualize the regression line on top of the test data points. We plot:
- **Scatter plot:** Each test point `(X_test, Y_test)` — the actual values
- **Line plot:** The predictions `(X_test, Y_pred)` — the model's fitted line

The regression line represents the equation `Ŷ = w₁ · X + w₀` with the learned weights. Where the line passes close to the data points, the model is accurate.

```python
# Plot the test data points
plt.scatter(X_test, Y_test, label="Test Data")

# Plot the regression line using the model's predictions
plt.plot(X_test, Y_pred, label="Regression Line")

# Add labels and title
plt.xlabel("X (Independent Variable)")
plt.ylabel("Y (Dependent Variable)")
plt.title("Linear Regression Model on Test Data")

# Add legend to distinguish data points from the regression line
plt.legend()

# Display the plot
plt.show()
```

**What we expect to see:** A diagonal regression line running cleanly through the scattered test data points, closely following the trend of the data.

---

## 6. Complete Script

```python
import numpy as np
import matplotlib.pyplot as plt
from sklearn.model_selection import train_test_split
from sklearn.linear_model import LinearRegression

# ----------------------------- DATA GENERATION -----------------------------

# Generate 100 evenly spaced values between 0 and 10
X = np.linspace(0, 10, 100)

# Generate noise from a normal distribution (mean=0, std=1)
noise = np.random.normal(0, 1, 100)

# Create the target variable with a linear relationship
Y = 2 * X + 1 + noise

# Reshape X to make it compatible with sklearn (100 rows, 1 feature)
X = X.reshape(-1, 1)


# ----------------------------- VISUALIZE RAW DATA --------------------------

# Create a scatter plot of the generated dataset
plt.scatter(X, Y)
plt.xlabel("X (Independent Variable)")
plt.ylabel("Y (Dependent Variable)")
plt.title("Generated Dataset with Linear Relationship and Noise")
plt.show()


# ----------------------------- TRAIN / TEST SPLIT --------------------------

# Split the dataset into training (80%) and testing (20%)
X_train, X_test, Y_train, Y_test = train_test_split(
    X, Y,
    test_size=0.2,
    random_state=42
)


# ----------------------------- TRAIN THE MODEL -----------------------------

# Create the linear regression model
linear_model = LinearRegression()

# Train (fit) the model using the training data only
linear_model.fit(X_train, Y_train)


# ----------------------------- EVALUATE THE MODEL --------------------------

# Generate predictions for the test dataset
Y_pred = linear_model.predict(X_test)

# Calculate and print the R² score on the test dataset
r2_score = linear_model.score(X_test, Y_test)
print("R² score:", r2_score)


# ----------------------------- PLOT RESULTS --------------------------------

# Plot the test data points and the regression line together
plt.scatter(X_test, Y_test, label="Test Data")
plt.plot(X_test, Y_pred, label="Regression Line")
plt.xlabel("X (Independent Variable)")
plt.ylabel("Y (Dependent Variable)")
plt.title("Linear Regression Model on Test Data")
plt.legend()
plt.show()
```

---

## Summary

| Step | Task | Tool Used |
|------|------|-----------|
| a | Generate 100 data points with linear relationship + noise | `numpy` |
| b | Scatter plot of raw data | `matplotlib.pyplot` |
| c | Split into 80% train / 20% test | `sklearn.model_selection.train_test_split` |
| d | Fit linear regression model on training data | `sklearn.linear_model.LinearRegression` |
| e | Evaluate model performance using R² on test data | `.score()` |
| f | Plot regression line over test data points | `matplotlib.pyplot` |

**Key principle learned:** Always fit the model on training data only. Evaluating on unseen test data gives a realistic picture of how well the model generalizes — which is the true measure of a good machine learning model.