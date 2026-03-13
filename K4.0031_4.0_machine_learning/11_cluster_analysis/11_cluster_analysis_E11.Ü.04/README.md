# Exercise 11.Ü.04 — DBSCAN Clustering

> **Course:** velpTEC K4.0031 — Machine Learning  
> **Chapter:** 11 — Clustering  
> **Algorithm:** DBSCAN (Density-Based Spatial Clustering of Applications with Noise)  
> **Libraries:** scikit-learn, NumPy, Matplotlib

---

## 1. What Problem Does DBSCAN Solve?

K-Means assumes all clusters are **round and roughly equal in size**. It forces every single point into a cluster — even points that are clearly outliers.

DBSCAN takes a completely different approach: instead of asking *"how far are you from the centre?"*, it asks *"how many neighbours do you have nearby?"*

This makes DBSCAN well-suited for:
- Datasets with **irregular or non-spherical cluster shapes**
- Datasets where some points are simply **noise** (outliers) and should not be assigned to any cluster
- Situations where **you do not know how many clusters** exist in advance

---

## 2. Core Concepts

### 2.1 The Two Key Parameters

| Parameter | Name | Meaning |
|-----------|------|---------|
| `eps` (ε) | Epsilon / neighbourhood radius | The maximum distance between two points for them to be considered neighbours |
| `min_samples` | MinObj | The minimum number of neighbours a point needs within radius ε to be classified as a **core point** |

### 2.2 The Three Point Types

Every point in the dataset gets one of three labels:

**Core Point**  
A point that has at least `min_samples` neighbours within radius `eps`.  
These are the "anchors" of a cluster.

**Border Point (Edge Point)**  
A point that has fewer than `min_samples` neighbours within `eps`, but lies within the `eps` radius of a core point.  
These are on the outer edge of a cluster — members, but not anchors.

**Noise Point**  
Any point that is neither a core point nor a border point.  
DBSCAN labels these as `-1`. They belong to no cluster.

```
         eps radius
        ┌─────────┐
   ●────●────●────●    ← Core points (many neighbours inside radius)
        └────●────┘
              ○        ← Border point (within radius of core, but not core itself)

   △                   ← Noise point (isolated, no nearby core)
```

---

## 3. The DBSCAN Algorithm — Step by Step

Once every point has been classified, DBSCAN builds clusters in two steps:

**Step 1:** Create a separate cluster for each core point (or group of connected core points). Two core points are connected if they are within `eps` distance of each other.

**Step 2:** Assign all border points to the cluster of their nearest core point.

Any point that remains unassigned after both steps is labelled as **noise** (`-1`).

---

## 4. The Math

### 4.1 Distance Metric — Euclidean Distance

DBSCAN uses a **distance metric** to determine whether two points are within `eps` of each other. The default metric is **Euclidean distance**.

For two points $p = (p_1, p_2)$ and $q = (q_1, q_2)$ in 2D space:

$$d(p, q) = \sqrt{(p_1 - q_1)^2 + (p_2 - q_2)^2}$$

More generally in $n$ dimensions:

$$d(p, q) = \sqrt{\sum_{i=1}^{n} (p_i - q_i)^2}$$

Two points are **neighbours** if their distance satisfies:

$$d(p, q) \leq \varepsilon$$

### 4.2 Core Point Condition

A point $p$ is a **core point** if the number of points within its ε-neighbourhood (including itself) is at least `min_samples`:

$$|N_\varepsilon(p)| \geq \text{MinObj}$$

Where $N_\varepsilon(p)$ is the set of all points within radius ε of point $p$:

$$N_\varepsilon(p) = \{ q \in D \mid d(p, q) \leq \varepsilon \}$$

### 4.3 What the Parameters Control

| Parameter | Too small | Too large |
|-----------|-----------|-----------|
| `eps` | Too many noise points, clusters split apart | Everything merges into one giant cluster |
| `min_samples` | Too many core points, noise gets absorbed | Too many noise points, real clusters get missed |

---

## 5. DBSCAN vs K-Means

| Property | K-Means | DBSCAN |
|----------|---------|--------|
| Number of clusters | Must be specified in advance | Discovered automatically |
| Cluster shape | Assumes spherical (round) clusters | Any shape |
| Outliers | Forces every point into a cluster | Labels outliers as noise (-1) |
| Sensitivity | Sensitive to initial centroid placement | Sensitive to `eps` and `min_samples` |
| Best for | Clean, round, well-separated clusters | Irregular shapes, noisy data |

---

## 6. The Dataset — `make_blobs`

The exercise uses `make_blobs` to generate a synthetic dataset with **three groups of different densities**. Density is controlled by `cluster_std` — the standard deviation of each blob.

```python
data_points, _ = make_blobs(
    n_samples=[100, 100, 100],       # 100 points per group = 300 total
    centers=[[-2, 0], [2, 2], [5, -2]],  # x,y coordinates of each group centre
    cluster_std=[0.2, 0.5, 1.5],    # high, medium, low density
    random_state=42                  # fix the random seed for reproducibility
)
```

| Group | Centre | `cluster_std` | Density | Expected DBSCAN result |
|-------|--------|---------------|---------|------------------------|
| 1 | `[-2, 0]` | `0.2` | High (tight) | Cluster 1 |
| 2 | `[2, 2]` | `0.5` | Medium | Cluster 2 |
| 3 | `[5, -2]` | `1.5` | Low (spread out) | Noise |

The `_` (underscore) discards the true group labels returned by `make_blobs` — we don't use them, because DBSCAN is **unsupervised** and finds its own labels.

---

## 7. Applying DBSCAN

```python
dbscan_model = DBSCAN(eps=0.5, min_samples=5, metric='euclidean')
cluster_labels = dbscan_model.fit_predict(data_points)
```

### What each parameter does

| Parameter | Value | Reason |
|-----------|-------|--------|
| `eps=0.5` | 0.5 units | Sets the neighbourhood radius. Tight enough to separate the dense group from noise. |
| `min_samples=5` | 5 points | A point needs at least 5 neighbours within ε to be a core point. |
| `metric='euclidean'` | Euclidean | Standard straight-line distance in 2D space. |

### `fit_predict` vs `fit` + `predict`

`fit_predict(X)` does both steps in one call:
1. **Fits** the model to the data (finds core/border/noise points)
2. **Returns** a label for every point in the array

The result `cluster_labels` is a 1D array of integers, one per data point:
- `0` → Cluster 1
- `1` → Cluster 2
- `-1` → Noise (not assigned to any cluster)

---

## 8. Visualising the Results

### 8.1 Boolean Masking

The key trick in the plotting code is **boolean masking**. When you write:

```python
data_points[cluster_labels == 0, 0]
```

This works in two steps:

1. `cluster_labels == 0` creates a boolean array: `[False, True, True, False, ...]`
2. `data_points[boolean_array, 0]` selects only the rows where the condition is True, and returns column `0` (Feature 1 / x-axis)

So `data_points[cluster_labels == 0, 1]` gives you the y-axis values for all points in Cluster 1.

### 8.2 The Full Plot Code

```python
# Cluster 1 — high density, label 0
plt.scatter(
    data_points[cluster_labels == 0, 0],   # x values of cluster 1
    data_points[cluster_labels == 0, 1],   # y values of cluster 1
    c='lightblue', edgecolor='black',
    marker='o', s=40,
    label='Cluster 1 (high density)'
)

# Cluster 2 — medium density, label 1
plt.scatter(
    data_points[cluster_labels == 1, 0],
    data_points[cluster_labels == 1, 1],
    c='red', edgecolor='black',
    marker='s', s=40,
    label='Cluster 2 (medium density)'
)

# Noise — low density, label -1
plt.scatter(
    data_points[cluster_labels == -1, 0],
    data_points[cluster_labels == -1, 1],
    c='yellow', edgecolor='black',
    marker='^', s=60,
    label='Noise (low density / unassigned)'
)

plt.legend()
plt.title('DBSCAN Clustering — Three Density Groups')
plt.xlabel('Feature 1')
plt.ylabel('Feature 2')
plt.tight_layout()   # prevents axis labels from being clipped
plt.show()
```

### 8.3 Reading the Plot

| Marker | Colour | Label | What it means |
|--------|--------|-------|---------------|
| Circle `o` | Light blue | Cluster 1 | Tight, high-density group — easily identified as a cluster |
| Square `s` | Red | Cluster 2 | Medium density — DBSCAN can still find enough neighbours |
| Triangle `^` | Yellow | Noise | Points too spread out — no single point has enough neighbours within ε=0.5 |

---

## 9. Why the Third Group Becomes Noise

The third group (centre `[5, -2]`, `cluster_std=1.5`) is so spread out that for any given point, the distance to its nearest neighbours exceeds `eps=0.5`. This means no point in that group satisfies the core point condition:

$$|N_{0.5}(p)| < 5 \quad \text{for all points } p \text{ in group 3}$$

So every point in group 3 is labelled `-1` (noise). This is DBSCAN behaving correctly — it refuses to group sparse points just because they were generated from the same blob. **DBSCAN is honest about uncertainty.**

---

## 10. Advantages and Limitations of DBSCAN

### Advantages
- Does **not require specifying the number of clusters** in advance
- Can find clusters of **any shape** (not just round ones)
- Naturally **handles noise and outliers** by labelling them `-1`
- Works well when cluster density is relatively **uniform**

### Limitations
- Struggles when clusters have **very different densities** (a single `eps` cannot work well for both tight and loose clusters simultaneously)
- Performance degrades in **high-dimensional data** (the curse of dimensionality makes Euclidean distance less meaningful)
- Choosing the right `eps` and `min_samples` can require **experimentation**

---

## 11. Complete Script

```python
#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Exercise 11.Ü.04 — DBSCAN Clustering
======================================
Apply the DBSCAN algorithm to a generated dataset with three groups
of different densities and visualise the clustering results.
"""

import numpy as np
import matplotlib.pyplot as plt
from sklearn.datasets import make_blobs
from sklearn.cluster import DBSCAN


# =============================================================================
# Step 1 — Generate the dataset
# =============================================================================
# Create 300 points split into three groups of 100, each with a different
# density. cluster_std controls how spread out each group is:
# low value = tight/dense, high value = loose/sparse.

data_points, _ = make_blobs(
    n_samples=[100, 100, 100],
    centers=[[-2, 0], [2, 2], [5, -2]],
    cluster_std=[0.2, 0.5, 1.5],   # high, medium, and low density
    random_state=42
)


# =============================================================================
# Step 2 — Apply the DBSCAN algorithm
# =============================================================================
# eps:         the maximum distance between two points to be considered neighbours
# min_samples: minimum number of neighbours a point needs to form a cluster
# Points with too few neighbours are labelled -1 (noise)

dbscan_model = DBSCAN(eps=0.5, min_samples=5, metric='euclidean')
cluster_labels = dbscan_model.fit_predict(data_points)


# =============================================================================
# Step 3 — Visualise the clustering results
# =============================================================================
# Each cluster label gets its own scatter plot with a distinct colour and marker.
# Label -1 means DBSCAN could not assign the point to any cluster (noise).

plt.scatter(
    data_points[cluster_labels == 0, 0],
    data_points[cluster_labels == 0, 1],
    c='lightblue', edgecolor='black',
    marker='o', s=40,
    label='Cluster 1 (high density)'
)

plt.scatter(
    data_points[cluster_labels == 1, 0],
    data_points[cluster_labels == 1, 1],
    c='red', edgecolor='black',
    marker='s', s=40,
    label='Cluster 2 (medium density)'
)

plt.scatter(
    data_points[cluster_labels == -1, 0],
    data_points[cluster_labels == -1, 1],
    c='yellow', edgecolor='black',
    marker='^', s=60,
    label='Noise (low density / unassigned)'
)

plt.legend()
plt.title('DBSCAN Clustering — Three Density Groups')
plt.xlabel('Feature 1')
plt.ylabel('Feature 2')
plt.tight_layout()
plt.show()
```

---

## 12. Key Takeaways

| Concept | Summary |
|---------|---------|
| DBSCAN | Density-based clustering — groups points by how many neighbours they have nearby |
| `eps` (ε) | Neighbourhood radius — how close two points must be to be considered neighbours |
| `min_samples` | Minimum neighbours to be a core point |
| Core point | Has ≥ `min_samples` neighbours within `eps` |
| Border point | Within `eps` of a core point, but not core itself |
| Noise point | Neither core nor border — labelled `-1` |
| `fit_predict` | Fits the model and returns cluster labels in one call |
| Boolean masking | `data[labels == 0]` selects only the rows belonging to cluster 0 |
| `cluster_std` | Controls blob density in `make_blobs` — low = tight, high = spread out |
| No. of clusters | DBSCAN finds it automatically — no need to specify in advance |

---

*Exercise completed — velpTEC K4.0031 | Chapter 11 — Clustering*