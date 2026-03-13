# --- a) Import necessary libraries ---
import numpy as np
import matplotlib.pyplot as plt
from sklearn.cluster import KMeans

# --- b) Create a NumPy array from the given dataset ---
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

# --- c) Apply K-Means algorithm to split data into 3 clusters ---
# n_clusters=3: we want 3 groups
# random_state=42: ensures reproducible results across runs
kmeans_model = KMeans(n_clusters=3, random_state=42)

# fit_predict: trains the model and returns a cluster label for each data point
cluster_labels = kmeans_model.fit_predict(data_points)

# --- d) Plot the resulting clusters and their centroids ---
# Plot data points, colored by their assigned cluster
plt.scatter(
    data_points[:, 0],  # all X values
    data_points[:, 1],  # all Y values
    c=cluster_labels,  # color each point by its cluster label
    cmap="viridis",  # color map for the 3 clusters
    label="Data Points",
)

# Plot the cluster centroids as large red X markers
plt.scatter(
    kmeans_model.cluster_centers_[:, 0],  # centroid X coordinates
    kmeans_model.cluster_centers_[:, 1],  # centroid Y coordinates
    c="red",
    marker="X",
    s=200,  # marker size — large enough to stand out
    label="Centroids",
)

plt.title("K-Means Clustering (k=3)")
plt.xlabel("X Value")
plt.ylabel("Y Value")
plt.legend()
plt.show()
