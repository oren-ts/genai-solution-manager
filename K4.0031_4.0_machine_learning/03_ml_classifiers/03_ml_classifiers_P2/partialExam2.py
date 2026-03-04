import numpy as np
from sklearn.model_selection import train_test_split
from sklearn.tree import DecisionTreeClassifier
from sklearn.neighbors import KNeighborsClassifier
from sklearn.metrics import accuracy_score

# Fix the random seed so results are identical on every run
np.random.seed(42)

# --- Data Generation ---
# Generate a synthetic dataset with 3 classes, 2 features each, 50 points per class
# Using different means per class creates separation
# Larger standard deviations create overlap between classes
points_per_class = 50

class_0 = np.random.normal(loc=[0.0, 0.0], scale=[1.2, 1.0], size=(points_per_class, 2))
class_1 = np.random.normal(loc=[2.0, 1.5], scale=[1.1, 1.3], size=(points_per_class, 2))
class_2 = np.random.normal(loc=[4.0, 3.0], scale=[1.2, 1.1], size=(points_per_class, 2))

# Stack all classes into one feature matrix (150 rows, 2 columns)
X = np.vstack((class_0, class_1, class_2))

# Create matching labels: 50 zeros, 50 ones, 50 twos
y = np.array([0] * points_per_class + [1] * points_per_class + [2] * points_per_class)

# --- Task a) Train / Test Split ---
# 70% of data goes to training, 30% to testing
# random_state=42 ensures the split is the same every run
X_train, X_test, y_train, y_test = train_test_split(
    X, y, test_size=0.3, random_state=42
)

# --- Task b) Decision Tree Classifier ---
# max_depth=3 limits how deep the tree grows — prevents overfitting
decision_tree_classifier = DecisionTreeClassifier(max_depth=3, random_state=42)
decision_tree_classifier.fit(X_train, y_train)
y_pred_tree = decision_tree_classifier.predict(X_test)

# --- Task c) K-Nearest Neighbors Classifier ---
# n_neighbors=5 means each prediction is based on the 5 closest training points
knn_classifier = KNeighborsClassifier(n_neighbors=5)
knn_classifier.fit(X_train, y_train)
y_pred_knn = knn_classifier.predict(X_test)

# --- Task d) Evaluate Both Models ---
# Accuracy = number of correct predictions / total predictions
tree_accuracy = accuracy_score(y_test, y_pred_tree)
knn_accuracy = accuracy_score(y_test, y_pred_knn)

print(f"Decision Tree Accuracy: {tree_accuracy:.2f}")
print(f"KNN Accuracy:           {knn_accuracy:.2f}")
