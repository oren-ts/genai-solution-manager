# Decision Tree vs. KNN — Synthetic 3-Class Classification

## Introduction

This script compares two supervised classification algorithms, a Decision Tree and a K-Nearest Neighbors (KNN) classifier, on a synthetically generated dataset. The dataset consists of three classes with two features each, designed with deliberate overlap to simulate real-world classification challenges.

---

## Dataset Generation

The dataset is created using NumPy's normal distribution generator. Each class is sampled from a different Gaussian distribution with its own mean and standard deviation. The means are spaced apart to create class separation, while the standard deviations are large enough to create overlap between classes.

| Class | Mean (Feature 1, Feature 2) | Std (Feature 1, Feature 2) |
|-------|-------------------------------|----------------------------|
| 0     | 0.0, 0.0                      | 1.2, 1.0                   |
| 1     | 2.0, 1.5                      | 1.1, 1.3                   |
| 2     | 4.0, 3.0                      | 1.2, 1.1                   |

Each class contains 50 points, giving a total dataset of 150 samples with shape `(150, 2)`.

```python
np.random.seed(42)
points_per_class = 50

class_0 = np.random.normal(loc=[0.0, 0.0], scale=[1.2, 1.0], size=(points_per_class, 2))
class_1 = np.random.normal(loc=[2.0, 1.5], scale=[1.1, 1.3], size=(points_per_class, 2))
class_2 = np.random.normal(loc=[4.0, 3.0], scale=[1.2, 1.1], size=(points_per_class, 2))

X = np.vstack((class_0, class_1, class_2))
y = np.array([0] * points_per_class + [1] * points_per_class + [2] * points_per_class)
```

---

## Task a) Train / Test Split

The dataset is split into 70% training data (105 samples) and 30% test data (45 samples). A fixed `random_state=42` ensures the split is identical on every run.

```python
X_train, X_test, y_train, y_test = train_test_split(
    X,
    y,
    test_size=0.3,
    random_state=42
)
```

---

## Task b) Decision Tree Classifier

### Theory

A Decision Tree learns a series of axis-aligned rules by splitting the feature space recursively. At each node, it finds the feature and threshold that best separates the classes. The tree grows until it reaches the maximum allowed depth or the data is pure.

Setting `max_depth=3` limits the tree to three levels of splits. This prevents overfitting by keeping the model from memorising the training data at the cost of flexibility.

### Code

```python
decision_tree_classifier = DecisionTreeClassifier(max_depth=3, random_state=42)
decision_tree_classifier.fit(X_train, y_train)
y_pred_tree = decision_tree_classifier.predict(X_test)
```

---

## Task c) K-Nearest Neighbors Classifier

### Theory

KNN is a non-parametric algorithm that makes predictions based on proximity. For each test point, it finds the `k` closest training points and assigns the majority class label among them. With `k=5`, each prediction is determined by a vote among the 5 nearest neighbours.

Unlike the Decision Tree, KNN has no explicit training phase, it simply stores the training data and performs all computation at prediction time. This makes it flexible but sensitive to local noise and class overlap.

### Code

```python
knn_classifier = KNeighborsClassifier(n_neighbors=5)
knn_classifier.fit(X_train, y_train)
y_pred_knn = knn_classifier.predict(X_test)
```

---

## Task d) Model Evaluation

Both models are evaluated using accuracy, the proportion of correctly classified test samples.

$$\text{Accuracy} = \frac{\text{Number of correct predictions}}{\text{Total number of predictions}}$$

```python
tree_accuracy = accuracy_score(y_test, y_pred_tree)
knn_accuracy = accuracy_score(y_test, y_pred_knn)

print(f"Decision Tree Accuracy: {tree_accuracy:.2f}")
print(f"KNN Accuracy:           {knn_accuracy:.2f}")
```

**Results:**

| Model         | Accuracy |
|---------------|----------|
| Decision Tree | 0.76     |
| KNN           | 0.76     |

---

## Task e) Model Comparison and Discussion

Both models achieve identical accuracy of 0.76 on the test set,  meaning both correctly classified 34 out of 45 test samples.

### Why the results are equal

The dataset was deliberately designed with class overlap. Points from different classes occupy the same regions of the 2D feature space, creating ambiguous samples that no simple classifier can reliably separate. This produces an effective accuracy ceiling that both models hit independently.

The two models reach this limit through fundamentally different mechanisms:

- The **Decision Tree** partitions the feature space using a fixed set of axis-aligned splits. With `max_depth=3`, it can make at most 7 decisions across the entire space, a deliberately limited and global boundary.
- **KNN** adapts locally, basing each prediction on the 5 nearest training points. However, in regions of class overlap, those nearest neighbours carry mixed labels, so the majority vote is unreliable.

### Resolution of the test set

With only 45 test samples, accuracy changes in steps of `1/45 ≈ 0.022`. A difference of a single correctly classified point would shift accuracy by that amount. An identical score of 0.76 therefore does not prove the models are equivalent, it means the test set resolution is too coarse to detect a difference, if one exists.

### Conclusion

Neither model outperforms the other on this dataset. The overlap built into the data creates an inherent limit on what any model with these hyperparameters can achieve. To meaningfully differentiate the two, a larger test set, cross-validation, or a less ambiguous dataset would be needed.
