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
