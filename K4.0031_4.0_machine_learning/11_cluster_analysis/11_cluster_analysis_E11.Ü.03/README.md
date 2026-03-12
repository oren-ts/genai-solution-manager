# 11.Ü.03 — Agglomerative Clustering

**Course:** velpTEC K4.0031 — Machine Learning  
**Chapter:** 11 — Cluster Analysis  
**Exercise:** 11.Ü.03  
**Script:** `Agglomeratives_Clustering.py`

---

## Table of Contents

1. [What is Agglomerative Clustering?](#1-what-is-agglomerative-clustering)
2. [Agglomerative vs Divisive](#2-agglomerative-vs-divisive)
3. [Linkage Methods](#3-linkage-methods)
4. [The Math: Euclidean Distance](#4-the-math-euclidean-distance)
5. [The Math: Cluster Center (Centroid)](#5-the-math-cluster-center-centroid)
6. [The Algorithm Step by Step](#6-the-algorithm-step-by-step)
7. [Agglomerative Clustering vs K-Means](#7-agglomerative-clustering-vs-k-means)
8. [Code Walkthrough](#8-code-walkthrough)
9. [Full Script](#9-full-script)

---

## 1. What is Agglomerative Clustering?

Agglomerative clustering is an **unsupervised machine learning** algorithm. This means it finds structure in data **without any labels** — you do not tell it which group a point belongs to. It figures that out on its own.

The core idea is beautifully simple:

> Start by treating every single data point as its own tiny cluster. Then, repeatedly merge the two closest clusters together — until you are left with the number of clusters you want.

Think of it like a family tree in reverse: you start with every individual person as a separate leaf, and keep connecting branches upward until you reach the root.

---

## 2. Agglomerative vs Divisive

Hierarchical clustering has two opposite approaches:

| Approach | Direction | Description |
|---|---|---|
| **Agglomerative** (this exercise) | Bottom-up ↑ | Start with N individual clusters, merge until 1 remains |
| **Divisive** | Top-down ↓ | Start with 1 big cluster, split until each point is alone |

In this exercise we use the **agglomerative** approach, which is by far the most common in practice.

---

## 3. Linkage Methods

When merging clusters, we need a rule to decide which two clusters are "closest". This rule is called the **linkage method**. The two standard methods are:

### Single Linkage
Merge the two clusters whose **most similar** (closest) members are nearest to each other.

```
Distance(A, B) = min{ d(a, b) : a ∈ A, b ∈ B }
```

### Complete Linkage ✅ (used by default in scikit-learn)
Merge the two clusters whose **most dissimilar** (farthest) members are nearest to each other.

```
Distance(A, B) = max{ d(a, b) : a ∈ A, b ∈ B }
```

Complete linkage tends to produce **more compact, equally sized clusters**, which is why it is the default in scikit-learn's `AgglomerativeClustering`.

---

## 4. The Math: Euclidean Distance

Before clusters can be merged, we need to measure the distance between every pair of points. The standard way is **Euclidean distance** — the straight-line distance between two points in space.

For two points $p = (p_1, p_2)$ and $q = (q_1, q_2)$ in 2D space:

$$d(p, q) = \sqrt{(p_1 - q_1)^2 + (p_2 - q_2)^2}$$

**Example:**  
Point A = (1, 2), Point B = (4, 6)

$$d(A, B) = \sqrt{(1-4)^2 + (2-6)^2} = \sqrt{9 + 16} = \sqrt{25} = 5$$

In general for $n$ dimensions:

$$d(p, q) = \sqrt{\sum_{k=1}^{n}(p_k - q_k)^2}$$

scikit-learn uses Euclidean distance by default when you create an `AgglomerativeClustering` object.

---

## 5. The Math: Cluster Center (Centroid)

Once clustering is done, we want to mark the **center** of each cluster visually. The center is calculated as the **arithmetic mean** of all points in a cluster.

For a cluster containing $m$ points, where each point has coordinates $(x_i, y_i)$:

$$\text{center}_x = \frac{1}{m} \sum_{i=1}^{m} x_i \qquad \text{center}_y = \frac{1}{m} \sum_{i=1}^{m} y_i$$

**Example:**  
Cluster with 3 points: (1, 2), (3, 4), (5, 6)

$$\text{center}_x = \frac{1 + 3 + 5}{3} = 3 \qquad \text{center}_y = \frac{2 + 4 + 6}{3} = 4$$

Center = (3, 4)

> ⚠️ **Important difference from K-Means:** In K-Means, the centroid is used *during* the algorithm to assign points. In agglomerative clustering, the algorithm never uses centroids internally — we calculate them manually *after* clustering, only for the visualization.

In NumPy, `.mean(axis=0)` calculates this across rows, giving one average value per column (i.e., one center coordinate per feature):

```python
cluster_center = points_in_cluster.mean(axis=0)
# axis=0 means: average across rows (down the column)
# Result: array([center_x, center_y])
```

---

## 6. The Algorithm Step by Step

Here is exactly what agglomerative clustering does internally:

```
Step 1: Assign each of the 300 data points its own cluster.
        → 300 clusters, each containing 1 point.

Step 2: Calculate the distance between every pair of clusters.
        → Build a distance matrix (300 × 300).

Step 3: Find the two clusters with the smallest distance.
        → Merge them into one new cluster.

Step 4: Update the distance matrix to reflect the new cluster.

Step 5: Repeat steps 3 and 4...
        → 299 clusters → 298 → ... → 3 clusters.

Step 6: Stop when the target number of clusters (n_clusters=3) is reached.
```

The result is a **cluster label** (0, 1, or 2) for each of the 300 data points.

---

## 7. Agglomerative Clustering vs K-Means

| Feature | K-Means | Agglomerative |
|---|---|---|
| Type | Prototype-based | Hierarchical |
| Needs `n_clusters` upfront | Yes | Yes (for scikit-learn's implementation) |
| Uses centroids internally | Yes | No |
| Result depends on random init | Yes (`random_state`) | No |
| Can visualize as dendrogram | No | Yes |
| Handles non-spherical clusters | Poorly | Better |
| `inertia_` attribute available | Yes | **No** |

---

## 8. Code Walkthrough

### Imports

```python
import matplotlib.pyplot as plt
from sklearn.cluster import AgglomerativeClustering
from sklearn.datasets import make_blobs
```

- `make_blobs` — generates synthetic 2D data in natural groups (blobs)
- `AgglomerativeClustering` — scikit-learn's hierarchical clustering class
- `matplotlib.pyplot` — for plotting the result

---

### a) Generate the Dataset

```python
# Create 300 data points spread across 3 natural groups (clusters)
# random_state=42 ensures we get the same data every time we run the script
X, y = make_blobs(n_samples=300, centers=3, random_state=42)
```

**What `make_blobs` returns:**
- `X` — shape `(300, 2)`: the 300 data points, each with 2 coordinates (Feature 1, Feature 2)
- `y` — shape `(300,)`: the *true* group label for each point (0, 1, or 2)

> Note: `y` is **not used** in the clustering — agglomerative clustering is unsupervised and does not see labels. We only use `y` here because `make_blobs` always returns it.

---

### b) Apply Agglomerative Clustering

```python
# Create the agglomerative clustering model with 3 target clusters
agglomerative_clustering = AgglomerativeClustering(n_clusters=3)

# Fit the model to the data and get the cluster label for each point (0, 1, or 2)
cluster_labels = agglomerative_clustering.fit_predict(X)
```

**Key parameters of `AgglomerativeClustering`:**

| Parameter | Default | Meaning |
|---|---|---|
| `n_clusters` | 2 | How many clusters to produce |
| `metric` | `'euclidean'` | How to measure distance between points |
| `linkage` | `'ward'` | Which linkage rule to use when merging |

**What `.fit_predict(X)` does:**  
Runs the full agglomerative algorithm on `X` and returns an array of cluster labels — one integer per data point. Unlike K-Means, there is no separate `.fit()` and `.predict()` step; the algorithm assigns labels during fitting itself.

```python
print(cluster_labels)
# Output: array([0, 2, 1, 0, 2, 1, ...])  — one label per point
print(cluster_labels.shape)
# Output: (300,)
```

> ⚠️ `AgglomerativeClustering` has **no `inertia_` attribute**. This is because the algorithm does not use centroids internally, so there is no SSE to report. If you need cluster quality metrics, use silhouette analysis instead.

---

### c) Visualize the Result

```python
plt.figure(figsize=(8, 6))

# One color per cluster — used in the loop below
cluster_colors = ["red", "green", "blue"]
```

The visualization loops through each cluster label (0, 1, 2) and draws two things:

**1. The cluster points**

```python
for i in range(3):
    # Select only the points that belong to cluster i
    points_in_cluster = X[cluster_labels == i]
```

`X[cluster_labels == i]` is **boolean indexing**:
- `cluster_labels == i` creates a True/False array of length 300
- `X[...]` then selects only the rows where the value is True
- Result: a sub-array containing only the points from cluster `i`

```python
    # Plot the cluster points in their assigned color
    plt.scatter(
        points_in_cluster[:, 0],   # x-coordinates (Feature 1)
        points_in_cluster[:, 1],   # y-coordinates (Feature 2)
        s=50,                       # marker size
        c=cluster_colors[i],        # color from our list
        label=f"Cluster {i + 1}",  # legend entry
    )
```

**2. The cluster center (manually calculated)**

```python
    # Calculate the center as the average position of all points in the cluster
    cluster_center = points_in_cluster.mean(axis=0)
    # → array([mean_x, mean_y])

    # Mark the cluster center with a large black star
    plt.scatter(
        cluster_center[0],   # x-coordinate of center
        cluster_center[1],   # y-coordinate of center
        s=200,               # larger marker size to make it stand out
        c="black",
        marker="*",          # star shape
        label=f"Center {i + 1}",
    )
```

**Plot labels and display**

```python
plt.title("Agglomerative Clustering")
plt.xlabel("Feature 1")
plt.ylabel("Feature 2")
plt.legend()
plt.grid(True)
plt.show()
```

---

## 9. Full Script

```python
# ==============================================================================
# 11.Ü.03 - Agglomerative Clustering
# ==============================================================================

import matplotlib.pyplot as plt
from sklearn.cluster import AgglomerativeClustering
from sklearn.datasets import make_blobs

# ==============================================================================
# a) Generate the synthetic dataset
# ==============================================================================

# Create 300 data points spread across 3 natural groups (clusters)
# random_state=42 ensures we get the same data every time we run the script
X, y = make_blobs(n_samples=300, centers=3, random_state=42)

# ==============================================================================
# b) Apply agglomerative clustering
# ==============================================================================

# Create the agglomerative clustering model with 3 target clusters
# Agglomerative clustering starts with each point as its own cluster,
# then merges the closest pairs step by step until 3 clusters remain
agglomerative_clustering = AgglomerativeClustering(n_clusters=3)

# Fit the model to the data and get the cluster label for each point (0, 1, or 2)
cluster_labels = agglomerative_clustering.fit_predict(X)

# ==============================================================================
# c) Visualize the clusters and their centers
# ==============================================================================

plt.figure(figsize=(8, 6))

# One color per cluster — used in the loop below
cluster_colors = ["red", "green", "blue"]

for i in range(3):
    # Select only the points that belong to cluster i
    points_in_cluster = X[cluster_labels == i]

    # Plot the cluster points in their assigned color
    plt.scatter(
        points_in_cluster[:, 0],
        points_in_cluster[:, 1],
        s=50,
        c=cluster_colors[i],
        label=f"Cluster {i + 1}",
    )

    # Calculate the cluster center as the average position of all points in the cluster
    cluster_center = points_in_cluster.mean(axis=0)

    # Mark the cluster center with a large black star
    plt.scatter(
        cluster_center[0],
        cluster_center[1],
        s=200,
        c="black",
        marker="*",
        label=f"Center {i + 1}",
    )

plt.title("Agglomerative Clustering")
plt.xlabel("Feature 1")
plt.ylabel("Feature 2")
plt.legend()
plt.grid(True)
plt.show()
```