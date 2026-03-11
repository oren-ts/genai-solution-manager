# =============================================================================
# 11.Ü.02 - Elbow Method
# Find the optimal number of clusters (k) using SSE (Sum of Squared Errors)
# =============================================================================

from sklearn.datasets import make_blobs
from sklearn.cluster import KMeans
import matplotlib.pyplot as plt


# =============================================================================
# a) Create synthetic dataset with 3 clusters
# =============================================================================

# Generate 300 data points spread across 3 clusters
# random_state=0 ensures we get the same data every time we run the script
data_points, _ = make_blobs(
    n_samples=300,
    n_features=2,
    centers=3,
    cluster_std=0.5,
    random_state=0,
)

# Plot the raw data before clustering — points are white so we can see the structure
plt.figure(figsize=(8, 5))
plt.scatter(
    data_points[:, 0],
    data_points[:, 1],
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


# =============================================================================
# b) Calculate SSE for k = 1 to 10
# =============================================================================

# SSE (inertia) measures how tightly packed each cluster is.
# Lower SSE = more compact clusters, but adding more clusters always reduces SSE.
# The "elbow" is where the improvement starts to flatten out.

sse_values = []

for k in range(1, 11):
    # Fit a KMeans model with k clusters
    # k-means++ initialisation spreads starting centroids out for better results
    kmeans_model = KMeans(
        n_clusters=k,
        init="k-means++",
        n_init=10,
        max_iter=300,
        random_state=0,
    )
    kmeans_model.fit(data_points)

    # inertia_ is sklearn's name for SSE — total squared distance to cluster centres
    sse_values.append(kmeans_model.inertia_)


# =============================================================================
# c) Plot the SSE curve — look for the "elbow"
# =============================================================================

# The elbow is the point where adding more clusters stops helping much.
# In this dataset it should appear clearly at k=3.

plt.figure(figsize=(8, 5))
plt.plot(
    range(1, 11),
    sse_values,
    marker="o",
    color="steelblue",
    linewidth=2,
    markersize=7,
)
plt.title("Elbow Method — Finding the Optimal Number of Clusters")
plt.xlabel("Number of Clusters (k)")
plt.ylabel("SSE (Inertia)")
plt.xticks(range(1, 11))
plt.grid(True)
plt.tight_layout()
plt.show()
