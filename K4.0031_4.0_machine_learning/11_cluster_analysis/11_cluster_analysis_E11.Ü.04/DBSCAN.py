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
    cluster_std=[0.2, 0.5, 1.5],  # high, medium, and low density
    random_state=42,
)


# =============================================================================
# Step 2 — Apply the DBSCAN algorithm
# =============================================================================
# eps:         the maximum distance between two points to be considered neighbours
# min_samples: minimum number of neighbours a point needs to form a cluster
# Points with too few neighbours are labelled -1 (noise)

dbscan_model = DBSCAN(eps=0.5, min_samples=5, metric="euclidean")
cluster_labels = dbscan_model.fit_predict(data_points)


# =============================================================================
# Step 3 — Visualise the clustering results
# =============================================================================
# Each cluster label gets its own scatter plot with a distinct colour and marker.
# Label -1 means DBSCAN could not assign the point to any cluster (noise).

plt.scatter(
    data_points[cluster_labels == 0, 0],
    data_points[cluster_labels == 0, 1],
    c="lightblue",
    edgecolor="black",
    marker="o",
    s=40,
    label="Cluster 1 (high density)",
)

plt.scatter(
    data_points[cluster_labels == 1, 0],
    data_points[cluster_labels == 1, 1],
    c="red",
    edgecolor="black",
    marker="s",
    s=40,
    label="Cluster 2 (medium density)",
)

plt.scatter(
    data_points[cluster_labels == -1, 0],
    data_points[cluster_labels == -1, 1],
    c="yellow",
    edgecolor="black",
    marker="^",
    s=60,
    label="Noise (low density / unassigned)",
)

plt.legend()
plt.title("DBSCAN Clustering — Three Density Groups")
plt.xlabel("Feature 1")
plt.ylabel("Feature 2")
plt.tight_layout()
plt.show()
