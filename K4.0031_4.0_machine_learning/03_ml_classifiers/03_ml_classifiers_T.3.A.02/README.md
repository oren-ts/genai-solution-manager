# Decision Tree Classifier
### Exercise 3.A.02 — Gender Classification
**Course:** velpTEC K4.0031 — Machine Learning
**Dataset:** `gender_classification.csv` (5,001 rows, 7 features)
**Algorithm:** Decision Tree (scikit-learn `DecisionTreeClassifier`)

---

## 1. What is a Decision Tree?

A Decision Tree is a supervised classification algorithm that learns a series of yes/no questions about the input features and uses them to predict a class label.

The intuition is simple: imagine a flowchart. At each step, you ask a question about the data — *"Is the forehead width greater than 14.5 cm?"* — and follow the Yes or No branch. You keep asking questions until you reach a final answer (a **leaf node**), which gives you the predicted class.

```
Is forehead_width_cm <= 14.07?
        |               |
       Yes              No
        |               |
  Is nose_wide = 0?   → Predict: Male
        |       |
       Yes      No
        |       |
  Predict:   Predict:
  Female      Male
```

Decision Trees work with both **categorical** and **continuous** (numeric) features, making them highly flexible. They are also **interpretable** — you can read the tree and understand exactly why a prediction was made.

---

## 2. How the Tree is Built — Information Gain

The algorithm must decide at each node: *which feature, and which threshold, produces the cleanest split?*

This is measured using **Information Gain (IG)**:

$$IG(D_p, f) = I(D_p) - \sum_{j=1}^{m} \frac{N_j}{N_p} I(D_j)$$

Where:
- $D_p$ = the parent node's dataset
- $D_j$ = the $j$-th child node's dataset
- $N_p$ = number of samples in the parent
- $N_j$ = number of samples in child $j$
- $I$ = an impurity measure (how "mixed" the classes are)
- $f$ = the feature being evaluated for the split

**The goal:** maximize Information Gain — i.e., find the split that produces the purest child nodes.

For binary trees (which scikit-learn uses), every node splits into exactly two children:

$$IG(D_p, f) = I(D_p) - \frac{N_{left}}{N_p} I(D_{left}) - \frac{N_{right}}{N_p} I(D_{right})$$

---

## 3. Impurity Measures

Three impurity criteria are commonly used. scikit-learn defaults to **Gini**.

### 3.1 Gini Impurity

Measures the probability of misclassifying a randomly chosen sample:

$$I_G(t) = 1 - \sum_{i=1}^{c} p(i|t)^2$$

Where $p(i|t)$ is the proportion of samples belonging to class $i$ at node $t$.

- **Gini = 0** → perfectly pure node (all samples belong to one class)
- **Gini = 0.5** → maximally impure (classes perfectly mixed, two classes)

**Example:** A node with 50% Female and 50% Male:

$$I_G = 1 - (0.5^2 + 0.5^2) = 1 - 0.5 = 0.5$$

A perfectly pure node (100% Female):

$$I_G = 1 - (1.0^2 + 0.0^2) = 0$$

### 3.2 Entropy

Measures the amount of disorder or uncertainty in a node:

$$I_H(t) = -\sum_{i=1}^{c} p(i|t) \log_2 p(i|t)$$

- **Entropy = 0** → all samples belong to the same class
- **Entropy = 1** → classes are perfectly mixed (two-class case)

### 3.3 Classification Error

$$I_E(t) = 1 - \max\{p(i|t)\}$$

Useful for pruning a tree after training, but not recommended for building it — it is less sensitive to changes in class probabilities at the nodes.

### Which to use?

In practice, Gini and Entropy produce very similar results. Gini is slightly faster to compute (no logarithm), which is why it is the scikit-learn default. The `DecisionTreeClassifier()` in this exercise uses Gini by default.

---

## 4. Overfitting and Pruning

A fully grown Decision Tree will keep splitting until every leaf node is perfectly pure — meaning it memorizes the training data exactly. This is called **overfitting**: the model performs perfectly on training data but poorly on new data.

The standard solution is **pruning** — limiting how deep the tree is allowed to grow:

```python
# Limiting tree depth prevents overfitting
tree_classifier = DecisionTreeClassifier(max_depth=4)
```

In this exercise, no `max_depth` is set (matching the course solution), so the tree grows fully. For the gender classification dataset this still produces strong results, but in noisier datasets depth-limiting would be important.

---

## 5. The Dataset

`gender_classification.csv` contains 5,001 rows of physical measurements labeled with gender.

| Feature | Description |
|---|---|
| `long_hair` | Binary: 1 = long hair, 0 = short hair |
| `forehead_width_cm` | Forehead width in centimetres |
| `forehead_height_cm` | Forehead height in centimetres |
| `nose_wide` | Binary: 1 = wide nose, 0 = narrow |
| `nose_long` | Binary: 1 = long nose, 0 = short |
| `lips_thin` | Binary: 1 = thin lips, 0 = full |
| `distance_nose_to_lip_long` | Binary: 1 = long distance, 0 = short |
| `gender` | Target: "Male" or "Female" |

The target column contains text labels, which must be converted to numbers before scikit-learn can process them.

---

## 6. Implementation

### 6.1 Imports

```python
import os
import pandas as pd
from sklearn import metrics
from sklearn.model_selection import train_test_split
from sklearn.preprocessing import LabelEncoder
from sklearn.tree import DecisionTreeClassifier
```

| Import | Purpose |
|---|---|
| `os` | Build portable file paths |
| `pandas` | Load and manipulate the CSV data |
| `metrics` | Calculate accuracy and precision scores |
| `train_test_split` | Split data into training and test sets |
| `LabelEncoder` | Convert text labels to integers |
| `DecisionTreeClassifier` | The Decision Tree model itself |

---

### 6.2 Loading the Data

```python
script_folder = os.path.dirname(os.path.abspath(__file__))
csv_path = os.path.join(script_folder, "gender_classification.csv")

gender_data = pd.read_csv(csv_path)
pd.set_option("display.max_columns", None)
print(gender_data)
```

`os.path.dirname(os.path.abspath(__file__))` finds the folder where this script lives. Joining it with the filename creates a path that works on any machine regardless of where the project is saved.

`pd.set_option("display.max_columns", None)` prevents pandas from hiding columns when printing wide DataFrames.

---

### 6.3 Encoding the Target Label

The `gender` column contains strings: `"Male"` and `"Female"`. scikit-learn requires numeric input for all columns, including the target.

```python
label_encoder = LabelEncoder()
gender_data["gender"] = label_encoder.fit_transform(gender_data["gender"])
```

`LabelEncoder` assigns an integer to each unique string value alphabetically:

```
"Female" → 0
"Male"   → 1
```

`fit_transform()` does two things in one call:
- **fit**: learns the mapping from the data
- **transform**: applies the mapping, replacing strings with integers

---

### 6.4 Splitting Features and Target

```python
X = gender_data.drop(columns=["gender"])  # 7 physical measurements
y = gender_data["gender"]                 # 0 = Female, 1 = Male
```

`X` contains everything the model learns *from* — the 7 numeric feature columns.
`y` contains what the model tries to *predict* — the encoded gender label.

---

### 6.5 Train/Test Split

```python
X_train, X_test, y_train, y_test = train_test_split(
    X, y, test_size=0.2, random_state=42
)
```

| Parameter | Value | Meaning |
|---|---|---|
| `test_size=0.2` | 20% | 1,000 rows held back for evaluation |
| `random_state=42` | 42 | Fixed seed — same split every run |

This gives 4,001 rows for training and 1,000 rows for testing.

The model is trained on `X_train` / `y_train` only. `X_test` / `y_test` simulate unseen real-world data and are used exclusively for evaluation. Evaluating on training data would give an artificially inflated score.

---

### 6.6 Training the Decision Tree

```python
tree_classifier = DecisionTreeClassifier()
tree_classifier.fit(X_train, y_train)
```

`DecisionTreeClassifier()` with no arguments uses these defaults:
- **criterion**: `gini` — uses Gini impurity to evaluate splits
- **max_depth**: `None` — tree grows until all leaves are pure
- **random_state**: not set — tie-breaking between equally good splits may vary between runs

`.fit(X_train, y_train)` triggers the tree-building process:
1. Start at the root with all training samples
2. Evaluate every feature and every threshold — find the split with highest Information Gain
3. Create two child nodes, divide the samples
4. Repeat recursively until leaves are pure or no further split is possible

---

### 6.7 Prediction and Evaluation

```python
y_predictions = tree_classifier.predict(X_test)

accuracy = metrics.accuracy_score(y_test, y_predictions)
precision = metrics.precision_score(y_test, y_predictions)

print("\n--- Decision Tree Results ---")
print(f"Model accuracy:  {accuracy:.2%}")
print(f"Model precision: {precision:.2%}")
```

**Accuracy** — the proportion of all predictions that were correct:

$$\text{Accuracy} = \frac{\text{Correct Predictions}}{\text{Total Predictions}}$$

**Precision** — of all samples predicted as Male (positive class), how many actually were Male:

$$\text{Precision} = \frac{\text{True Positives}}{\text{True Positives} + \text{False Positives}}$$

High precision means: *when the model says "Male", it is usually right.*

---

## 7. Results

```
Model accuracy:  95.30%
Model precision: 95.75%
```

**95.30% accuracy** means the model correctly classified 953 out of 1,000 test samples.

**95.75% precision** means that when the model predicted "Male", it was correct 95.75% of the time.

These are strong results for a default, unpruned Decision Tree with no feature scaling or hyperparameter tuning — demonstrating that the 7 physical measurement features carry clear and learnable signal for gender classification.

---

## 8. Key Concepts Summary

| Concept | Meaning |
|---|---|
| **Node** | A decision point — asks a yes/no question about one feature |
| **Leaf node** | A terminal node — gives the final class prediction |
| **Gini impurity** | How mixed the classes are at a node (0 = pure, 0.5 = maximally mixed) |
| **Information Gain** | How much a split reduces impurity — higher is better |
| **Pruning** | Limiting tree depth to prevent overfitting |
| **Overfitting** | Model memorizes training data but fails to generalize |
| **LabelEncoder** | Converts text class labels to integers for scikit-learn |
| **train_test_split** | Divides data so evaluation is done on unseen samples |