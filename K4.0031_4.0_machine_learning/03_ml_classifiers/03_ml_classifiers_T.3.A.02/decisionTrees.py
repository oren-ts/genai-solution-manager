# -------------------- IMPORTS --------------------
# pandas: load and work with our CSV data as a table
# train_test_split: split data into training and test portions
# metrics: tools to measure how good our model is
# LabelEncoder: converts text labels ("Male"/"Female") to numbers
# os: build file paths that work on any computer

import os
import pandas as pd
from sklearn import metrics
from sklearn.model_selection import train_test_split
from sklearn.preprocessing import LabelEncoder
from sklearn.tree import DecisionTreeClassifier


# -------------------- DATA PREPARATION --------------------

# Build the file path relative to this script's location
# This makes the code portable — works on any machine, not just yours
script_folder = os.path.dirname(os.path.abspath(__file__))
csv_path = os.path.join(script_folder, "gender_classification.csv")

# Load the CSV into a DataFrame (like a spreadsheet in Python)
gender_data = pd.read_csv(csv_path)

# Show all columns when printing — useful for inspection
pd.set_option("display.max_columns", None)
print(gender_data)

# Encode the "gender" column: ML models need numbers, not text
# LabelEncoder converts: "Female" → 0, "Male" → 1
label_encoder = LabelEncoder()
gender_data["gender"] = label_encoder.fit_transform(gender_data["gender"])

# Split the data into:
# - features: everything the model learns FROM (the 7 measurements)
# - labels:   what the model tries to PREDICT (gender)
X = gender_data.drop(columns=["gender"])  # Input: 7 physical measurements
y = gender_data["gender"]  # Output: 0 (Female) or 1 (Male)

# Split into 80% training data and 20% test data
# random_state=42 makes the split reproducible — same result every run
X_train, X_test, y_train, y_test = train_test_split(
    X, y, test_size=0.2, random_state=42
)


# -------------------- DECISION TREE --------------------

# Create the Decision Tree classifier with default settings
# By default, scikit-learn uses the Gini impurity criterion to find the best splits
tree_classifier = DecisionTreeClassifier()

# Train the model — it learns decision rules from the training data
tree_classifier.fit(X_train, y_train)

# Make predictions on the test data (data the model has never seen)
y_predictions = tree_classifier.predict(X_test)


# -------------------- EVALUATION --------------------

# Accuracy: what % of all predictions were correct?
accuracy = metrics.accuracy_score(y_test, y_predictions)

# Precision: of all "Male" predictions, how many were actually Male?
precision = metrics.precision_score(y_test, y_predictions)

print("\n--- Decision Tree Results ---")
print(f"Model accuracy:  {accuracy:.2%}")
print(f"Model precision: {precision:.2%}")
