# 11.Ü.02 — Elbow Method
### Finding the Optimal Number of Clusters in K-Means

**Course:** velpTEC K4.0031 — Machine Learning  
**Script file:** `ElbowMethod.py`  
**Libraries:** `scikit-learn`, `matplotlib`

---

## Table of Contents

1. [What Problem Does the Elbow Method Solve?](#1-what-problem-does-the-elbow-method-solve)
2. [K-Means Recap — How Clustering Works](#2-k-means-recap--how-clustering-works)
3. [The Math — Euclidean Distance and SSE](#3-the-math--euclidean-distance-and-sse)
4. [The Elbow Criterion — Theory](#4-the-elbow-criterion--theory)
5. [Implementation — Step by Step](#5-implementation--step-by-step)
   - [a) Creating the Dataset](#a-creating-the-dataset)
   - [b) Calculating SSE for Each k](#b-calculating-sse-for-each-k)
   - [c) Plotting the Elbow Curve](#c-plotting-the-elbow-curve)
6. [Reading the Elbow Plot](#6-reading-the-elbow-plot)
7. [Key Concepts Summary](#7-key-concepts-summary)

---

## 1. What Problem Does the Elbow Method Solve?

K-Means requires you to choose the number of clusters **k before training begins**. This is one of its well-known limitations: if you pick the wrong k, the clustering result will be poor — too few clusters merge groups that should be separate, too many clusters split groups that belong together.

The **Elbow Method** is a simple graphical technique that helps you pick a good value of k by asking: *at what point does adding more clusters stop being worth it?*

---

## 2. K-Means Recap — How Clustering Works

K-Means groups data points into k clusters by repeating four steps:

1. **Initialise** — randomly select k points as starting cluster centres (centroids)
2. **Assign** — assign every data point to its nearest centroid
3. **Update** — recalculate each centroid as the mean of all points assigned to it
4. **Repeat** — go back to step 2 until cluster assignments stop changing, or a maximum number of iterations is reached

> **Intuition:** Imagine dropping k magnets onto a map of cities. Each city snaps to its nearest magnet. Then each magnet moves to the centre of gravity of its cities. Repeat until nothing moves anymore.

K-Means belongs to **prototype-based clustering** — each cluster is represented by a prototype (its centroid), not by a boundary.

---

## 3. The Math — Euclidean Distance and SSE

### Squared Euclidean Distance

To measure how similar two points are, K-Means uses the **squared Euclidean distance** between two points $x$ and $y$ in $m$-dimensional space:

$$d(x, y)^2 = \sum_{j=1}^{m} (x_j - y_j)^2$$

Where:
- $j$ = the dimension index (i.e. which feature column)
- $x_j$, $y_j$ = the value of feature $j$ for points $x$ and $y$

For our 2D dataset, $m = 2$, so this simplifies to:

$$d(x, y)^2 = (x_1 - y_1)^2 + (x_2 - y_2)^2$$

### Sum of Squared Errors (SSE)

Using this distance, K-Means minimises the **SSE** — the total sum of squared distances from every point to its assigned cluster centroid:

$$SSE = \sum_{i=1}^{n} \sum_{j=1}^{k} w^{(i,j)} \; \| x^{(i)} - \mu^{(j)} \|^2$$

Where:
- $x^{(i)}$ = the $i$-th data point
- $\mu^{(j)}$ = the centroid of cluster $j$
- $w^{(i,j)} = 1$ if point $i$ belongs to cluster $j$, otherwise $0$
- $\| \cdot \|^2$ = squared Euclidean distance

**In plain terms:** for every point, measure how far it is from its cluster centre, square that distance, and add them all up. A lower SSE means more compact, tighter clusters.

### SSE in scikit-learn

After fitting a `KMeans` model, scikit-learn stores the SSE automatically as the `inertia_` attribute:

```python
kmeans_model = KMeans(n_clusters=3, random_state=0)
kmeans_model.fit(data_points)

print(kmeans_model.inertia_)  # This is the SSE
```

> **Why "inertia"?** The term comes from physics — it describes how much a cluster "resists" being compacted further. High inertia = spread-out cluster.

---

## 4. The Elbow Criterion — Theory

When you increase k from 1 to 10:

- At **k = 1**, all points belong to one cluster — the SSE is very high
- At **k = 2**, SSE drops sharply — two clusters are already much tighter
- At **k = 3** (the true number of groups in our data), SSE drops again significantly
- At **k = 4, 5, 6...**, SSE keeps decreasing, but the improvement becomes small — you're just splitting existing clusters that were already tight

This produces a curve shaped like an arm. The **elbow** is the bend in the curve — the point where the rate of improvement drops off sharply. That bend tells you the optimal k.

> **Why does SSE always keep going down?**  
> Because if you set k = n (one cluster per point), every point IS its own centroid — SSE would be exactly 0. But that's meaningless. The elbow helps you find the sweet spot before you overfit the number of clusters to the data.

---

## 5. Implementation — Step by Step

### a) Creating the Dataset

`make_blobs` generates synthetic data with clearly defined cluster regions. It's perfect for testing clustering algorithms because you can control exactly how many clusters exist.

```python
from sklearn.datasets import make_blobs
import matplotlib.pyplot as plt

# Generate 300 points spread across 3 clusters
# random_state=0 ensures identical output every run
data_points, _ = make_blobs(
    n_samples=300,   # total number of data points
    n_features=2,    # 2D so we can visualise it
    centers=3,       # 3 true clusters hidden in the data
    cluster_std=0.5, # how tightly packed each cluster is
    random_state=0,  # fixed seed for reproducibility
)
```

**Why `_` for the second return value?**  
`make_blobs` also returns the true cluster labels (`y`). The `_` is a Python convention meaning *"I'm intentionally ignoring this value"* — in unsupervised learning we don't use ground-truth labels.

**Visualising the raw data:**

```python
plt.figure(figsize=(8, 5))
plt.scatter(
    data_points[:, 0],    # all rows, column 0 → x-axis
    data_points[:, 1],    # all rows, column 1 → y-axis
    c="white",
    marker="o",
    edgecolor="black",
    s=50,
)
plt.title("Raw Data — 3 Synthetic Clusters")
plt.xlabel("Feature 1")
plt.ylabel("Feature 2")
plt.grid(True)
plt.tight_layout()
plt.show()
```

The white circles with black borders make individual points easy to see without colour implying cluster membership (we haven't clustered yet at this stage).

---

### b) Calculating SSE for Each k

This is the core of the exercise. We loop through k = 1 to 10, fit a KMeans model for each, and store its `inertia_` (SSE) in a list.

```python
from sklearn.cluster import KMeans

sse_values = []

for k in range(1, 11):  # k = 1, 2, 3, ..., 10
    kmeans_model = KMeans(
        n_clusters=k,       # number of clusters to find
        init="k-means++",   # smarter initialisation — spreads starting centroids out
        n_init=10,          # run 10 times with different starts, keep best result
        max_iter=300,       # stop after 300 iterations if not yet converged
        random_state=0,     # fixed seed for reproducibility
    )
    kmeans_model.fit(data_points)

    # inertia_ = SSE for this value of k
    sse_values.append(kmeans_model.inertia_)
```

**Key parameters explained:**

| Parameter | Value | Why |
|---|---|---|
| `init="k-means++"` | Smart seeding | Spreads initial centroids out, avoids poor local minima |
| `n_init=10` | 10 restarts | Runs 10 times with different random starts; keeps the best SSE |
| `max_iter=300` | 300 iterations max | Prevents infinite loops if convergence is slow |
| `random_state=0` | Fixed seed | Reproducible results across runs |

**Why k-means++ instead of random?**  
With purely random initialisation, starting centroids might all land in the same cluster — leading to poor results. `k-means++` deliberately spreads them out, which consistently produces better clusters.

---

### c) Plotting the Elbow Curve

```python
plt.figure(figsize=(8, 5))
plt.plot(
    range(1, 11),     # x-axis: k values 1 to 10
    sse_values,       # y-axis: SSE for each k
    marker="o",       # dot at each data point
    color="steelblue",
    linewidth=2,
    markersize=7,
)
plt.title("Elbow Method — Finding the Optimal Number of Clusters")
plt.xlabel("Number of Clusters (k)")
plt.ylabel("SSE (Inertia)")
plt.xticks(range(1, 11))  # show every k value on x-axis
plt.grid(True)
plt.tight_layout()
plt.show()
```

---

## 6. Reading the Elbow Plot

The resulting plot looks approximately like this:

```
SSE
 |
1450 ●
     |  \
 600 |    ●
     |      \
 150 |        ●─────●─────●─────●─────●─────●─────●
     |
     +────────────────────────────────────────────
     1    2    3    4    5    6    7    8    9   10
                   k (number of clusters)
```

- **k = 1 → k = 2**: SSE drops dramatically (~1450 → ~600)
- **k = 2 → k = 3**: SSE drops sharply again (~600 → ~150) — the **elbow**
- **k = 3 onwards**: SSE decreases slowly and flatly

**Conclusion:** The elbow clearly appears at **k = 3**, which matches the ground truth (`centers=3` in `make_blobs`). This confirms the method is working correctly.

---

## 7. Key Concepts Summary

| Concept | Plain Explanation | In the Code |
|---|---|---|
| **K-Means** | Groups data by repeatedly assigning points to their nearest centroid | `KMeans(...).fit(data_points)` |
| **SSE / Inertia** | Total squared distance from every point to its cluster centre | `kmeans_model.inertia_` |
| **Elbow Method** | Plot SSE vs k — the bend marks the optimal k | `plt.plot(range(1, 11), sse_values)` |
| **k-means++** | Smarter centroid initialisation to avoid bad starts | `init="k-means++"` |
| **n_init** | Number of independent restarts — best result is kept | `n_init=10` |
| **random_state** | Fixes the random seed so results are reproducible | `random_state=0` |
| **`_` convention** | Pythonic way to discard a return value you don't need | `data_points, _ = make_blobs(...)` |