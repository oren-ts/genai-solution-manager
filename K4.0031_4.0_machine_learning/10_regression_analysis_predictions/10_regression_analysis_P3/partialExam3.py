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
    X, Y, test_size=0.2, random_state=42
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
