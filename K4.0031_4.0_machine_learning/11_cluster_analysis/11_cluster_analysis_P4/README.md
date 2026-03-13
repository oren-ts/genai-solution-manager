# Partial Exam 4 — K-Means Clustering

**Course:** velpTEC K4.0031 Machine Learning  
**Topic:** Unsupervised Learning — K-Means Clustering  
**Language:** Python 3 | scikit-learn, NumPy, Matplotlib

---

## 1. Theory — What is K-Means Clustering?

K-Means is an **unsupervised machine learning algorithm** that groups data points into **k clusters** based on similarity. Unlike supervised algorithms (e.g. logistic regression, SVM), K-Means has **no labels** — it discovers structure in the data on its own.

### Intuition

Think of K-Means like sorting a bag of mixed fruit by eye:
- You decide upfront how many groups you want (e.g. 3)
- You place each fruit into the group whose center it is closest to
- You keep adjusting the group centers until nothing moves anymore

### The Algorithm — Step by Step

1. **Initialise** — randomly place `k` centroids in the data space
2. **Assign** — assign each data point to the nearest centroid
3. **Update** — recalculate each centroid as the mean of its assigned points
4. **Repeat** — repeat steps 2–3 until the centroids stop moving (convergence)

---

## 2. The Math

### Distance Metric

K-Means uses **Euclidean distance** to measure how close a point is to a centroid:

$$d(x, \mu) = \sqrt{\sum_{j=1}^{n} (x_j - \mu_j)^2}$$

Where:
- $x$ = a data point
- $\mu$ = a centroid
- $n$ = number of features (in this exercise: 2, the X and Y values)

### Objective Function — SSE (Sum of Squared Errors)

K-Means minimises the **within-cluster sum of squared errors**:

$$SSE = \sum_{i=1}^{k} \sum_{x \in C_i} \|x - \mu_i\|^2$$

Where:
- $k$ = number of clusters
- $C_i$ = the set of points in cluster $i$
- $\mu_i$ = the centroid of cluster $i$

The algorithm converges when SSE can no longer be reduced by reassigning points or moving centroids.

### Centroid Update Rule

After each assignment step, each centroid is recalculated as the **mean** of all points in its cluster:

$$\mu_i = \frac{1}{|C_i|} \sum_{x \in C_i} x$$

---

## 3. The Dataset

The exercise provides 10 two-dimensional data points:

| X-Value | Y-Value |
|---------|---------|
| 1.5     | 2.4     |
| 3.5     | 4.2     |
| 5.1     | 5.8     |
| 6.2     | 7.4     |
| 7.9     | 8.2     |
| 2.3     | 3.5     |
| 4.6     | 4.9     |
| 6.3     | 6.1     |
| 7.5     | 7.9     |
| 3.4     | 4.0     |

Each row is one data point with two features: an X-value and a Y-value.

---

## 4. Implementation

### a) Import Libraries

```python
import numpy as np
import matplotlib.pyplot as plt
from sklearn.cluster import KMeans
```

- `numpy` — creates and handles the data array
- `matplotlib.pyplot` — draws the scatter plot
- `KMeans` from `sklearn.cluster` — provides the clustering algorithm

---

### b) Create the NumPy Array

```python
# Each row is one data point: [X-value, Y-value]
data_points = np.array(
    [
        [1.5, 2.4],
        [3.5, 4.2],
        [5.1, 5.8],
        [6.2, 7.4],
        [7.9, 8.2],
        [2.3, 3.5],
        [4.6, 4.9],
        [6.3, 6.1],
        [7.5, 7.9],
        [3.4, 4.0],
    ]
)
```

This creates a 2D NumPy array of shape `(10, 2)` — 10 rows (data points), 2 columns (X and Y).

---

### c) Apply K-Means

```python
# n_clusters=3: we want 3 groups
# random_state=42: ensures reproducible results across runs
kmeans_model = KMeans(n_clusters=3, random_state=42)

# fit_predict: trains the model AND returns a cluster label for each data point
cluster_labels = kmeans_model.fit_predict(data_points)
```

**Key parameters:**

| Parameter | Value | Purpose |
|---|---|---|
| `n_clusters` | `3` | Number of clusters to form |
| `random_state` | `42` | Fixes random seed for reproducibility |

**`fit_predict` vs `fit` + `predict`:**

- `fit_predict(data_points)` does both in one step: it trains the model on the data and immediately returns the cluster label for each point
- `cluster_labels` is an array like `[0, 1, 2, 1, 2, 0, 1, 2, 2, 1]` — one integer per data point indicating its cluster

**Accessing the centroids after fitting:**

```python
kmeans_model.cluster_centers_  # shape: (3, 2) — one centroid per cluster
```

---

### d) Plot Clusters and Centroids

```python
# Plot data points, colored by their assigned cluster
plt.scatter(
    data_points[:, 0],   # all X values
    data_points[:, 1],   # all Y values
    c=cluster_labels,    # color each point by its cluster label
    cmap="viridis",      # color map for the 3 clusters
    label="Data Points",
)

# Plot the cluster centroids as large red X markers
plt.scatter(
    kmeans_model.cluster_centers_[:, 0],  # centroid X coordinates
    kmeans_model.cluster_centers_[:, 1],  # centroid Y coordinates
    c="red",
    marker="X",
    s=200,               # marker size — large enough to stand out
    label="Centroids",
)

plt.title("K-Means Clustering (k=3)")
plt.xlabel("X Value")
plt.ylabel("Y Value")
plt.legend()
plt.show()
```

**Indexing explained:**

| Expression | Meaning |
|---|---|
| `data_points[:, 0]` | All rows, column 0 → all X values |
| `data_points[:, 1]` | All rows, column 1 → all Y values |
| `cluster_centers_[:, 0]` | X coordinate of each centroid |
| `cluster_centers_[:, 1]` | Y coordinate of each centroid |

---

## 5. Result

The plot shows:
- **3 color-coded groups** of data points (teal, yellow, purple)
- **3 red X markers** — the centroids, one per cluster, positioned at the geometric center of each group
- The data follows a natural diagonal trend, and K-Means correctly identifies three distinct regions along this trend

---

## 6. Key Concepts Summary

| Concept | Description |
|---|---|
| Unsupervised learning | No labels — the algorithm finds structure on its own |
| Centroid | The mean position of all points in a cluster |
| SSE | The objective function K-Means minimises |
| `n_clusters` | Must be chosen in advance (use Elbow Method to decide) |
| `fit_predict` | Trains the model and returns cluster labels in one call |
| `cluster_centers_` | Attribute storing the final centroid coordinates |
| `random_state` | Fixes the random seed for reproducible initialisation |k — K-Means Clustering

**Course:** velpTEC K4.0031 Machine Learning  
**Topic:** Unsupervised Learning — K-Means Clustering  
**Language:** Python 3 | scikit-learn, NumPy, Matplotlib

---

## 1. Theory — What is K-Means Clustering?

K-Means is an **unsupervised machine learning algorithm** that groups data points into **k clusters** based on similarity. Unlike supervised algorithms (e.g. logistic regression, SVM), K-Means has **no labels** — it discovers structure in the data on its own.

### Intuition

Think of K-Means like sorting a bag of mixed fruit by eye:
- You decide upfront how many groups you want (e.g. 3)
- You place each fruit into the group whose center it is closest to
- You keep adjusting the group centers until nothing moves anymore

### The Algorithm — Step by Step

1. **Initialise** — randomly place `k` centroids in the data space
2. **Assign** — assign each data point to the nearest centroid
3. **Update** — recalculate each centroid as the mean of its assigned points
4. **Repeat** — repeat steps 2–3 until the centroids stop moving (convergence)

---

## 2. The Math

### Distance Metric

K-Means uses **Euclidean distance** to measure how close a point is to a centroid:

$$d(x, \mu) = \sqrt{\sum_{j=1}^{n} (x_j - \mu_j)^2}$$

Where:
- $x$ = a data point
- $\mu$ = a centroid
- $n$ = number of features (in this exercise: 2, the X and Y values)

### Objective Function — SSE (Sum of Squared Errors)

K-Means minimises the **within-cluster sum of squared errors**:

$$SSE = \sum_{i=1}^{k} \sum_{x \in C_i} \|x - \mu_i\|^2$$

Where:
- $k$ = number of clusters
- $C_i$ = the set of points in cluster $i$
- $\mu_i$ = the centroid of cluster $i$

The algorithm converges when SSE can no longer be reduced by reassigning points or moving centroids.

### Centroid Update Rule

After each assignment step, each centroid is recalculated as the **mean** of all points in its cluster:

$$\mu_i = \frac{1}{|C_i|} \sum_{x \in C_i} x$$

---

## 3. The Dataset

The exercise provides 10 two-dimensional data points:

| X-Value | Y-Value |
|---------|---------|
| 1.5     | 2.4     |
| 3.5     | 4.2     |
| 5.1     | 5.8     |
| 6.2     | 7.4     |
| 7.9     | 8.2     |
| 2.3     | 3.5     |
| 4.6     | 4.9     |
| 6.3     | 6.1     |
| 7.5     | 7.9     |
| 3.4     | 4.0     |

Each row is one data point with two features: an X-value and a Y-value.

---

## 4. Implementation

### a) Import Libraries

```python
import numpy as np
import matplotlib.pyplot as plt
from sklearn.cluster import KMeans
```

- `numpy` — creates and handles the data array
- `matplotlib.pyplot` — draws the scatter plot
- `KMeans` from `sklearn.cluster` — provides the clustering algorithm

---

### b) Create the NumPy Array

```python
# Each row is one data point: [X-value, Y-value]
data_points = np.array(
    [
        [1.5, 2.4],
        [3.5, 4.2],
        [5.1, 5.8],
        [6.2, 7.4],
        [7.9, 8.2],
        [2.3, 3.5],
        [4.6, 4.9],
        [6.3, 6.1],
        [7.5, 7.9],
        [3.4, 4.0],
    ]
)
```

This creates a 2D NumPy array of shape `(10, 2)` — 10 rows (data points), 2 columns (X and Y).

---

### c) Apply K-Means

```python
# n_clusters=3: we want 3 groups
# random_state=42: ensures reproducible results across runs
kmeans_model = KMeans(n_clusters=3, random_state=42)

# fit_predict: trains the model AND returns a cluster label for each data point
cluster_labels = kmeans_model.fit_predict(data_points)
```

**Key parameters:**

| Parameter | Value | Purpose |
|---|---|---|
| `n_clusters` | `3` | Number of clusters to form |
| `random_state` | `42` | Fixes random seed for reproducibility |

**`fit_predict` vs `fit` + `predict`:**

- `fit_predict(data_points)` does both in one step: it trains the model on the data and immediately returns the cluster label for each point
- `cluster_labels` is an array like `[0, 1, 2, 1, 2, 0, 1, 2, 2, 1]` — one integer per data point indicating its cluster

**Accessing the centroids after fitting:**

```python
kmeans_model.cluster_centers_  # shape: (3, 2) — one centroid per cluster
```

---

### d) Plot Clusters and Centroids

```python
# Plot data points, colored by their assigned cluster
plt.scatter(
    data_points[:, 0],   # all X values
    data_points[:, 1],   # all Y values
    c=cluster_labels,    # color each point by its cluster label
    cmap="viridis",      # color map for the 3 clusters
    label="Data Points",
)

# Plot the cluster centroids as large red X markers
plt.scatter(
    kmeans_model.cluster_centers_[:, 0],  # centroid X coordinates
    kmeans_model.cluster_centers_[:, 1],  # centroid Y coordinates
    c="red",
    marker="X",
    s=200,               # marker size — large enough to stand out
    label="Centroids",
)

plt.title("K-Means Clustering (k=3)")
plt.xlabel("X Value")
plt.ylabel("Y Value")
plt.legend()
plt.show()
```

**Indexing explained:**

| Expression | Meaning |
|---|---|
| `data_points[:, 0]` | All rows, column 0 → all X values |
| `data_points[:, 1]` | All rows, column 1 → all Y values |
| `cluster_centers_[:, 0]` | X coordinate of each centroid |
| `cluster_centers_[:, 1]` | Y coordinate of each centroid |

---

## 5. Result

The plot shows:
- **3 color-coded groups** of data points (teal, yellow, purple)
- **3 red X markers** — the centroids, one per cluster, positioned at the geometric center of each group
- The data follows a natural diagonal trend, and K-Means correctly identifies three distinct regions along this trend

---

## 6. Key Concepts Summary

| Concept | Description |
|---|---|
| Unsupervised learning | No labels — the algorithm finds structure on its own |
| Centroid | The mean position of all points in a cluster |
| SSE | The objective function K-Means minimises |
| `n_clusters` | Must be chosen in advance (use Elbow Method to decide) |
| `fit_predict` | Trains the model and returns cluster labels in one call |
| `cluster_centers_` | Attribute storing the final centroid coordinates |
| `random_state` | Fixes the random seed for reproducible initialisation |