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
