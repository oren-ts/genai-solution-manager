# =============================================================================
# Exercise 10.Ü.01 — Correlation Matrix
# Goal: Generate a fictitious housing dataset and visualize the correlation
#       between its variables using a seaborn heatmap.
# =============================================================================

import pandas as pd
import numpy as np
import seaborn as sns
import matplotlib.pyplot as plt


# =============================================================================
# Section 1 — Generate the fictitious housing dataset
# =============================================================================

# Fix the random seed so results are the same every time the script runs
np.random.seed(0)

# Create a dictionary where each key is a column name and each value
# is an array of 100 randomly generated numbers scaled to a realistic range
housing_data = {
    "CRIM": np.random.rand(100),  # Per capita crime rate (0–1)
    "ZN": np.random.rand(100) * 100,  # % residential land for large lots (0–100)
    "INDUS": np.random.rand(100) * 25,  # % non-retail business land (0–25)
    "NOX": np.random.rand(100),  # Nitrogen monoxide concentration (0–1)
    "RM": np.random.rand(100) * 10,  # Average number of rooms per dwelling (0–10)
    "AGE": np.random.rand(100)
    * 100,  # % owner-occupied homes built before 1940 (0–100)
    "DIS": np.random.rand(100) * 10,  # Weighted distance to employment centres (0–10)
    "RAD": np.random.randint(
        1, 10, 100
    ),  # Accessibility index for arterial roads (1–9)
    "TAX": np.random.randint(200, 700, 100),  # Property tax per $10,000 (200–700)
    "PTRATIO": np.random.rand(100) * 20,  # Pupil-to-teacher ratio (0–20)
}

# Convert the dictionary into a pandas DataFrame (a structured table)
housing_df = pd.DataFrame(housing_data)


# =============================================================================
# Section 2 — Calculate the correlation matrix
# =============================================================================

# Compute the Pearson correlation coefficient between every pair of columns.
# Each value in the matrix tells us how strongly two variables move together:
#   +1 = perfect positive relationship
#    0 = no linear relationship
#   -1 = perfect negative relationship
correlation_matrix = housing_df.corr(method="pearson")


# =============================================================================
# Section 3 — Visualize the correlation matrix as a heatmap
# =============================================================================

# Set the figure size so the heatmap is large enough to read comfortably
plt.figure(figsize=(10, 8))

# Draw the heatmap:
#   annot=True    → print the correlation value inside each cell
#   cmap='coolwarm' → red for positive correlations, blue for negative
sns.heatmap(correlation_matrix, annot=True, cmap="coolwarm")

plt.title("Correlation Matrix — Fictitious Housing Dataset")
plt.tight_layout()
plt.show()
