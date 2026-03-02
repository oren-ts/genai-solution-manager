# Support Vector Machine — Gender Classification
### ML Portfolio Entry | Course: velpTEC K4.0031

---

## 1. Problem Statement

Classify a person's gender based on physical facial measurements using a **Support Vector Machine (SVM)** — a supervised learning algorithm for binary classification.

**Dataset:** `gender_classification.csv` — 5,001 records, 8 columns  
**Features:** `long_hair`, `forehead_width_cm`, `forehead_height_cm`, `nose_wide`, `nose_long`, `lips_thin`, `distance_nose_to_lip_long`  
**Target:** `gender` (string: `"Male"` / `"Female"`)

---

## 2. What is a Support Vector Machine?

An SVM finds the **optimal decision boundary** between two classes by maximising the margin between them.
```
     Female  |  Male
        ●    |    ○
      ●   ●  |  ○   ○
        ●    |    ○
             |
      <--- margin --->
           decision
           boundary
```

The data points closest to the boundary are called **Support Vectors** — they define where the boundary sits. The algorithm's goal is to make this margin as wide as possible, which leads to better generalisation on unseen data.

### The Kernel Parameter

| Kernel | When to use |
|--------|-------------|
| `linear` | Data is roughly linearly separable — our case |
| `rbf` | Complex, non-linear boundaries |
| `poly` | Polynomial patterns |

We use `kernel="linear"` because the 7 physical features provide a clean enough separation without needing higher-dimensional transformation.

---

## 3. Data Preparation

### 3.1 Loading the Data
```python
script_folder = os.path.dirname(os.path.abspath(__file__))
df = pd.read_csv(os.path.join(script_folder, "gender_classification.csv"))
```

Path is built dynamically relative to the script — not hard-coded — making it **portable across machines**.

---

### 3.2 Label Encoding
```python
label = LabelEncoder()
df["gender"] = label.fit_transform(df["gender"])
# "Female" → 0 | "Male" → 1
```

ML algorithms require numbers. `LabelEncoder` converts string categories to integers. We update only the `gender` column inside the existing DataFrame to preserve all features.

---

### 3.3 Feature / Label Split
```python
features = df.drop("gender", axis=1)   # 7 physical measurements (input X)
labels   = df["gender"]                 # Encoded gender (output y)
```

---

### 3.4 Train / Test Split
```python
feature_train, feature_test, label_train, label_test = train_test_split(
    features, labels, test_size=0.2, random_state=42
)
```

| Split | Size | Purpose |
|-------|------|---------|
| Training | 80% (~4,000 rows) | Model learns the pattern |
| Test | 20% (~1,000 rows) | Unseen data for honest evaluation |

`random_state=42` ensures the split is **reproducible** across runs.

---

## 4. Model Training & Prediction
```python
classifier = svm.SVC(kernel="linear")
classifier.fit(feature_train, label_train)   # Learn from training data
label_pred = classifier.predict(feature_test) # Predict on unseen data
```

`svm.SVC` — Support Vector **Classifier**. `.fit()` is where learning happens: the algorithm finds the maximum-margin hyperplane across 4,000 training examples. `.predict()` applies that learned boundary to 1,000 unseen rows.

---

## 5. Evaluation
```python
accuracy  = metrics.accuracy_score(label_test, label_pred)
precision = metrics.precision_score(label_test, label_pred)
```

### Results
```
Model accuracy:  0.9600  →  96.0%
Model precision: 0.9636  →  96.4%
```

### Metric Definitions

**Accuracy** — What percentage of all predictions were correct?
```
Accuracy = Correct predictions / Total predictions
```

**Precision** — Of all "Male" predictions, how many were actually Male?
```
Precision = True Positives / (True Positives + False Positives)
```

High precision means few false positives — the model doesn't frequently misclassify Females as Males.

> **Note:** For a complete picture, future work should also report **Recall** and **F1-score**, especially if the dataset were imbalanced.

---

## 6. Complete Script
```python
import pandas as pd
from sklearn import svm, metrics
from sklearn.model_selection import train_test_split
from sklearn.preprocessing import LabelEncoder
import os

# Load data — path built relative to script for portability
script_folder = os.path.dirname(os.path.abspath(__file__))
df = pd.read_csv(os.path.join(script_folder, "gender_classification.csv"))
pd.set_option("display.max_columns", None)

# Encode string labels to integers: Female=0, Male=1
label = LabelEncoder()
df["gender"] = label.fit_transform(df["gender"])

# Separate input features from output label
features = df.drop("gender", axis=1)
labels   = df["gender"]

# 80/20 train-test split with fixed seed for reproducibility
feature_train, feature_test, label_train, label_test = train_test_split(
    features, labels, test_size=0.2, random_state=42
)

# Train SVM with linear kernel
classifier = svm.SVC(kernel="linear")
classifier.fit(feature_train, label_train)
label_pred = classifier.predict(feature_test)

# Evaluate
accuracy  = metrics.accuracy_score(label_test, label_pred)
precision = metrics.precision_score(label_test, label_pred)

print(f"Model accuracy:  {accuracy}")
print(f"Model precision: {precision}")
```

---

## 7. Key Concepts Summary

| Concept | Applied Here |
|---------|-------------|
| Supervised learning | Gender labels known during training |
| Binary classification | Two output classes: Male / Female |
| Label encoding | String → integer for ML compatibility |
| Train/test split | Honest evaluation on unseen data |
| SVM linear kernel | Maximum-margin boundary between classes |
| Accuracy & Precision | Complementary model quality metrics |

---

## 8. Possible Extensions

- Add a **confusion matrix** to visualise TP / FP / FN / TN
- Test `kernel="rbf"` — does non-linear separation improve accuracy?
- Add **StandardScaler** — SVMs are sensitive to feature scale differences
- Report **F1-score** for a balanced view of precision and recall