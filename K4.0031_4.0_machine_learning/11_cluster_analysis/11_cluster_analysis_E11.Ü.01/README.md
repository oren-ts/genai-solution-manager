# 11.Ü.01 — K-Means Clustering

---

## Table of Contents

1. [Overview](#1-overview)
2. [Theoretical Background](#2-theoretical-background)
   - 2.1 [Supervised vs. Unsupervised Learning](#21-supervised-vs-unsupervised-learning)
   - 2.2 [What is Clustering?](#22-what-is-clustering)
   - 2.3 [What is K-Means?](#23-what-is-k-means)
   - 2.4 [The Four-Step Algorithm](#24-the-four-step-algorithm)
   - 2.5 [Similarity — Squared Euclidean Distance](#25-similarity--squared-euclidean-distance)
   - 2.6 [The SSE Objective Function](#26-the-sse-objective-function)
   - 2.7 [K-Means as an Optimization Problem](#27-k-means-as-an-optimization-problem)
   - 2.8 [Limitations of K-Means](#28-limitations-of-k-means)
3. [Dataset](#3-dataset)
4. [Implementation](#4-implementation)
   - 4.1 [Step a — Create the Dataset](#41-step-a--create-the-dataset)
   - 4.2 [Step b — Visualize the Raw Dataset](#42-step-b--visualize-the-raw-dataset)
   - 4.3 [Step c — Build and Fit the K-Means Model](#43-step-c--build-and-fit-the-k-means-model)
   - 4.4 [Step d — Visualize the Cluster Centers](#44-step-d--visualize-the-cluster-centers)
   - 4.5 [Step e — Calculate and Output the SSE](#45-step-e--calculate-and-output-the-sse)
5. [Key Concepts Summary](#5-key-concepts-summary)
6. [Full Script](#6-full-script)

---

## 1. Overview

This exercise implements **K-Means clustering** — an unsupervised machine learning algorithm that automatically groups data points into k clusters based on similarity, without any labels or prior knowledge of the groups.

| Property         | Value                          |
|------------------|-------------------------------|
| Algorithm        | K-Means                        |
| Learning type    | Unsupervised                   |
| Task type        | Clustering                     |
| Dataset          | Synthetic (make_blobs)         |
| Data points      | 200                            |
| Features         | 2 (x and y coordinates)        |
| Clusters (k)     | 4                              |
| Library          | scikit-learn                   |

---

## 2. Theoretical Background

### 2.1 Supervised vs. Unsupervised Learning

All previous exercises in this course used **supervised learning** — the dataset contained both features `X` and labels `y`, and the model learned a mapping from inputs to known outputs.

| Type                  | Labels? | Goal                          | Examples                        |
|-----------------------|---------|-------------------------------|---------------------------------|
| Supervised learning   | ✅ Yes  | Learn X → y mapping           | Classification, Regression      |
| Unsupervised learning | ❌ No   | Discover hidden structure     | Clustering, Dimensionality reduction |

K-Means belongs to unsupervised learning. The algorithm receives only feature data `X` and must find the groups on its own.

---

### 2.2 What is Clustering?

Clustering tries to find **natural groups** in data, where:

- Points **within** the same cluster are as similar as possible
- Points **across** different clusters are as different as possible

Real-world examples:

| Domain              | Clustering application                            |
|---------------------|--------------------------------------------------|
| Marketing           | Group customers by purchasing behavior           |
| Streaming platforms | Group movies or songs by similarity              |
| Biology             | Group genes with similar expression patterns     |
| Document analysis   | Group articles by topic                          |

Clustering is **exploratory analysis** — you discover structure that was not previously known.

---

### 2.3 What is K-Means?

K-Means is a **prototype-based clustering** algorithm. This means each cluster is represented by a single point called a **centroid** (or prototype), which is the mean position of all points assigned to that cluster.

Key properties:

- Divides data into exactly **k clusters**
- Each point belongs to **exactly one cluster** (hard/crisp assignment)
- Each cluster is represented by its **centroid** — the mean of all its points
- Works best with **spherical, evenly sized, clearly separated** clusters
- You must choose **k in advance**

> **Analogy:** Imagine dropping k magnets onto a map. Each magnet attracts the nearest people to it. Then each magnet slides to the center of its group. Repeat until the magnets stop moving. That is K-Means.

---

### 2.4 The Four-Step Algorithm

K-Means follows a simple iterative procedure:

```
Step 1 — Initialization
    Randomly select k points as the initial cluster centers (centroids)

Step 2 — Assignment
    For each data point, calculate its distance to every centroid
    Assign the point to the cluster of the nearest centroid

Step 3 — Update
    Recompute each centroid as the mean of all points currently assigned to it

Step 4 — Convergence check
    If the centroids have stopped moving (or moved less than a threshold), stop
    Otherwise, go back to Step 2
```

Visually:

```
Iteration 1:              Iteration 2:              Converged:
  ★  ● ●                   ● ●★ ●                   ● ●★●
● ● ●    ● ●             ● ● ●    ● ●             ●●●●●   ●●●
    ★● ●                     ● ●★                       ●★●
```

The algorithm is guaranteed to converge, but may find a **local minimum** rather than the global optimum — which is why running it multiple times (`n_init`) matters.

---

### 2.5 Similarity — Squared Euclidean Distance

K-Means measures similarity using **distance**. The closer two points are, the more similar they are.

The distance measure used is the **squared Euclidean distance**:

$$d(x, y)^2 = \sum_{j=1}^{m} (x_j - y_j)^2 = \|x - y\|_2^2$$

Where:

| Symbol     | Meaning                                      |
|------------|----------------------------------------------|
| `x`, `y`   | Two data points being compared               |
| `m`        | Number of features (dimensions)              |
| `x_j`      | Value of feature j for point x              |
| `y_j`      | Value of feature j for point y              |

**Example** with 2D points `x = (2, 5)` and `y = (4, 1)`:

$$d(x, y)^2 = (2 - 4)^2 + (5 - 1)^2 = (-2)^2 + 4^2 = 4 + 16 = 20$$

Why **squared** distance rather than regular distance?

- Penalizes points that are far away more strongly
- Avoids computing a square root (computationally cheaper)
- Connects naturally to the SSE objective function below

---

### 2.6 The SSE Objective Function

K-Means is not just "group nearby points" — it is a formal **optimization problem**. The goal is to minimize the **Sum of Squared Errors (SSE)**, also called **inertia**:

$$SSE = \sum_{i=1}^{n} \sum_{j=1}^{k} w^{(i,j)} \|x^{(i)} - \mu^{(j)}\|_2^2$$

Where:

| Symbol          | Meaning                                                  |
|-----------------|----------------------------------------------------------|
| `n`             | Total number of data points                              |
| `k`             | Number of clusters                                       |
| `x^(i)`         | The i-th data point                                      |
| `μ^(j)`         | The centroid of cluster j                                |
| `‖x^(i) − μ^(j)‖²` | Squared Euclidean distance from point i to centroid j |
| `w^(i,j)`       | Membership indicator: 1 if point i belongs to cluster j, 0 otherwise |

The membership indicator `w^(i,j)` acts as an on/off switch — it ensures only the distance to the point's **assigned** cluster is counted in the total error.

**Intuition:** SSE measures how tightly packed points are around their cluster centers.

| SSE value   | Meaning                                         |
|-------------|-------------------------------------------------|
| Small SSE   | Points are close to their centers — compact clusters, good result |
| Large SSE   | Points are far from their centers — loose clusters, poor result   |

**Small example:**

Centroid: `μ = (2, 2)`, assigned points: `(2, 3)`, `(1, 2)`, `(3, 2)`

```
point (2,3) → distance² to (2,2) = 0² + 1² = 1
point (1,2) → distance² to (2,2) = 1² + 0² = 1
point (3,2) → distance² to (2,2) = 1² + 0² = 1

Cluster SSE = 1 + 1 + 1 = 3  ✅ compact cluster
```

---

### 2.7 K-Means as an Optimization Problem

Connecting the four steps to the math:

| Algorithm step         | Mathematical operation                              |
|------------------------|-----------------------------------------------------|
| Step 1 — Initialize    | Choose k random starting centroids                  |
| Step 2 — Assign        | Use squared Euclidean distance to assign each point |
| Step 3 — Update        | Recompute μ^(j) = mean of assigned points           |
| Step 4 — Repeat        | Each iteration reduces SSE until convergence        |

The algorithm's formal objective is:

$$\min_{\{w, \mu\}} SSE = \min \sum_{i=1}^{n} \sum_{j=1}^{k} w^{(i,j)} \|x^{(i)} - \mu^{(j)}\|_2^2$$

Each iteration provably reduces or maintains the SSE — it never gets worse. This is why the algorithm always converges.

---

### 2.8 Limitations of K-Means

| Limitation                     | Explanation                                                   |
|--------------------------------|---------------------------------------------------------------|
| Must choose k in advance       | The algorithm cannot discover the number of clusters itself   |
| Sensitive to initialization    | Poor random starting centers can lead to suboptimal results   |
| Assumes spherical clusters     | Struggles with elongated, ring-shaped, or irregular clusters  |
| Assumes similar cluster sizes  | Unevenly sized clusters are often merged or split incorrectly |
| Hard assignments only          | Each point belongs to exactly one cluster (no overlap)        |

The **Elbow Method** (Exercise 11.Ü.02) addresses the first limitation by plotting SSE vs. k to find the optimal number of clusters.

---

## 3. Dataset

The dataset is generated synthetically using `make_blobs` from scikit-learn. It creates 200 points divided into 4 well-separated clusters in 2D space.

| Parameter      | Value  | Meaning                                          |
|----------------|--------|--------------------------------------------------|
| `n_samples`    | 200    | Total number of data points                      |
| `n_features`   | 2      | Each point has 2 coordinates (x and y)           |
| `centers`      | 4      | 4 cluster groups are generated                   |
| `cluster_std`  | 0.60   | Points are spread tightly around each center     |
| `random_state` | 42     | Fixed random seed — same dataset every run       |

The result is a matrix `X` of shape `(200, 2)`:

```
X = [
    [-3.2,  8.1],   ← point 1: x=-3.2, y=8.1
    [ 4.5,  2.3],   ← point 2: x=4.5,  y=2.3
    [-8.1,  7.6],   ← point 3: x=-8.1, y=7.6
    ...
]
```

`y` contains the true cluster labels generated by `make_blobs`, but these are **not used** — K-Means is unsupervised and discovers the groups on its own.

---

## 4. Implementation

### 4.1 Step a — Create the Dataset

```python
from sklearn.datasets import make_blobs

X, y = make_blobs(
    n_samples=200,    # total number of data points
    n_features=2,     # 2 features → can be plotted as x and y coordinates
    centers=4,        # generate 4 cluster groups
    cluster_std=0.60, # how spread out points are around each center
    random_state=42   # fix the random seed for reproducibility
)
```

**Why `make_blobs` for this exercise?**

Real datasets are often messy, high-dimensional, and hard to visualize. `make_blobs` creates ideal conditions for K-Means — spherical, clearly separated clusters — which lets us focus on understanding the algorithm without data preprocessing complications.

**Why `cluster_std=0.60`?**

The standard deviation controls how tightly points cluster around their center. A value of 0.60 creates tight, distinct groups. A larger value (e.g. 2.0) would cause clusters to overlap, making the problem harder for K-Means.

---

### 4.2 Step b — Visualize the Raw Dataset

```python
import matplotlib.pyplot as plt

plt.scatter(
    X[:, 0],            # x-axis: first feature (all rows, column 0)
    X[:, 1],            # y-axis: second feature (all rows, column 1)
    c="white",          # fill color: white
    marker="o",         # marker shape: circle
    edgecolors="black", # border color: black
    s=50                # marker size
)

plt.title("Raw Dataset (before clustering)")
plt.grid()
plt.tight_layout()
plt.show()
```

**NumPy slice notation recap:**

| Expression    | Meaning                                        |
|---------------|------------------------------------------------|
| `X[:, 0]`     | All rows, column 0 → x-coordinates of all points |
| `X[:, 1]`     | All rows, column 1 → y-coordinates of all points |

At this stage the algorithm has not run yet. All 200 points are drawn identically — white circles with black borders. Even so, 4 natural groups are already visually apparent, which is exactly what K-Means will detect mathematically.

---

### 4.3 Step c — Build and Fit the K-Means Model

```python
from sklearn.cluster import KMeans

km = KMeans(
    n_clusters=4,   # number of clusters to find (k = 4)
    init="random",  # choose initial cluster centers randomly
    n_init=10,      # run 10 times, keep the result with lowest SSE
    max_iter=300,   # maximum update cycles per run
    tol=1e-04,      # stop early if improvement drops below this threshold
    random_state=0  # fix the random seed for reproducibility
)

y_km = km.fit_predict(X)
```

**Parameter breakdown:**

| Parameter      | Value    | Maps to theory                                          |
|----------------|----------|---------------------------------------------------------|
| `n_clusters`   | 4        | k = 4 in the SSE formula                               |
| `init`         | `random` | Step 1 — randomly select initial centroids             |
| `n_init`       | 10       | Run 10 independent trials, keep the one with min SSE   |
| `max_iter`     | 300      | Step 4 — maximum number of assign + update cycles      |
| `tol`          | `1e-04`  | Step 4 — convergence threshold (stop when Δ < 0.0001)  |
| `random_state` | 0        | Makes the random initialization reproducible           |

**Why `n_init=10`?**

Because random initialization can lead to different outcomes. Some starting positions lead to better cluster assignments than others. Running 10 independent trials and keeping the best result (by SSE) protects against unlucky initialization.

**`fit_predict(X)` — what it does internally:**

```
1. Initialize 4 random centroids                    ← init='random'
2. Assign each point to its nearest centroid        ← uses squared Euclidean distance
3. Recompute each centroid as the mean of its points ← that is why it is called k-Means
4. Repeat steps 2–3 until convergence               ← tol=1e-04 or max_iter=300
5. Return cluster ID for each point                 ← stored in y_km
```

After running, `y_km` contains a cluster label for every point:

```python
y_km = [2, 2, 0, 1, 3, 0, 1, 3, ...]
#        ↑             ↑
#  point 1 → cluster 2    point 4 → cluster 1
```

These are not ordered or ranked — cluster 0 is not "better" than cluster 3. They are simply group IDs assigned by the algorithm.

---

### 4.4 Step d — Visualize the Cluster Centers

```python
# Data points
plt.scatter(
    X[:, 0],
    X[:, 1],
    c="white",
    marker="o",
    edgecolors="black",
    s=50,
    label="Data points"
)

# Cluster centers
plt.scatter(
    km.cluster_centers_[:, 0],  # x-coordinates of all 4 cluster centers
    km.cluster_centers_[:, 1],  # y-coordinates of all 4 cluster centers
    s=100,                      # larger size so centers stand out
    marker="s",                 # square marker
    c="red",                    # red fill
    edgecolors="black",         # black border for contrast
    label="Cluster centers"
)

plt.title("K-Means Clustering — Cluster Centers")
plt.legend()
plt.grid()
plt.tight_layout()
plt.show()
```

**`km.cluster_centers_` explained:**

After fitting, scikit-learn stores the final centroid positions in `km.cluster_centers_`. This is a NumPy array of shape `(k, n_features)` — one row per cluster, one column per feature:

```
km.cluster_centers_ = [
    [-3.1,  8.2],   ← centroid of cluster 0
    [ 4.4,  2.1],   ← centroid of cluster 1
    [-8.0,  7.5],   ← centroid of cluster 2
    [-6.2, -7.1],   ← centroid of cluster 3
]
```

This directly corresponds to `μ^(j)` in the SSE formula:

$$\mu^{(j)} = \frac{1}{|C_j|} \sum_{x^{(i)} \in C_j} x^{(i)}$$

In plain English: the centroid is the average position of all points assigned to that cluster.

**Why plot the raw points again in step d?**

Because `plt.show()` in step b closed and cleared the figure. To add the centers to the same scatter plot, we need to redraw the data points first.

---

### 4.5 Step e — Calculate and Output the SSE

```python
print(f"Sum of squared deviations within the clusters (SSE): {km.inertia_}")
```

**`km.inertia_` explained:**

After fitting, scikit-learn computes and stores the SSE in `km.inertia_`. This is the direct implementation of the SSE formula:

$$SSE = \sum_{i=1}^{n} \sum_{j=1}^{k} w^{(i,j)} \|x^{(i)} - \mu^{(j)}\|_2^2$$

In code terms:

```python
km.inertia_  ==  SSE  ==  sum of squared distances from each point to its centroid
```

Example output:

```
Sum of squared deviations within the clusters (SSE): 130.65234716643346
```

**What this number tells us:**

- It is the total compactness of all 4 clusters combined
- A lower value means points are tighter around their centers — better clustering
- This value is used by the **Elbow Method** (next exercise) to compare different values of k

---

## 5. Key Concepts Summary

| Concept                  | Definition                                                                 |
|--------------------------|----------------------------------------------------------------------------|
| Unsupervised learning    | No labels — the algorithm discovers structure from features alone          |
| Clustering               | Grouping similar data points, separating dissimilar ones                   |
| Centroid / μ^(j)         | The mean position of all points in a cluster                               |
| Squared Euclidean distance | The sum of squared coordinate differences between two points             |
| SSE / inertia            | Total sum of squared distances from each point to its assigned centroid    |
| `make_blobs`             | Generates synthetic clustered data for testing                             |
| `fit_predict(X)`         | Runs K-Means and returns cluster ID for each point                         |
| `km.cluster_centers_`   | Array of shape (k, features) storing final centroid coordinates            |
| `km.inertia_`            | The SSE value after fitting — measures cluster compactness                 |
| `n_init=10`              | Run 10 trials, keep the result with lowest SSE                             |
| `tol=1e-04`              | Convergence threshold — stop when centroid movement drops below 0.0001     |

---

## 6. Full Script

```python
# =============================================================================
# 11.Ü.01 - K-Means Clustering
# =============================================================================

import matplotlib.pyplot as plt
from sklearn.cluster import KMeans
from sklearn.datasets import make_blobs


# Step a) Create the dataset
X, y = make_blobs(
    n_samples=200,
    n_features=2,
    centers=4,
    cluster_std=0.60,
    random_state=42
)

# Step b) Visualize the raw dataset (before clustering)
plt.scatter(X[:, 0], X[:, 1], c="white", marker="o", edgecolors="black", s=50)
plt.title("Raw Dataset (before clustering)")
plt.grid()
plt.tight_layout()
plt.show()

# Step c) K-Means Clustering
km = KMeans(n_clusters=4, init="random", n_init=10, max_iter=300, tol=1e-04, random_state=0)
y_km = km.fit_predict(X)

# Step d) Visualize the cluster centers
plt.scatter(X[:, 0], X[:, 1], c="white", marker="o", edgecolors="black", s=50, label="Data points")
plt.scatter(km.cluster_centers_[:, 0], km.cluster_centers_[:, 1],
            s=100, marker="s", c="red", edgecolors="black", label="Cluster centers")
plt.title("K-Means Clustering — Cluster Centers")
plt.legend()
plt.grid()
plt.tight_layout()
plt.show()

# Step e) Calculate and output the SSE
print(f"Sum of squared deviations within the clusters (SSE): {km.inertia_}")
```

---

*Exercise 11.Ü.01 — K-Means Clustering | Course: velpTEC K4.0031 Machine Learning*