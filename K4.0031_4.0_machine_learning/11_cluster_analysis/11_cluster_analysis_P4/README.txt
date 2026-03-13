Partial Exam 4 — K-Means Clustering
========================================

THEORY
------
K-Means is an unsupervised machine learning algorithm that groups data points
into k clusters based on similarity. Unlike supervised algorithms, K-Means has
no labels — it discovers structure in the data on its own.

The algorithm works in 4 steps:
1. Place k centroids randomly in the data space
2. Assign each data point to the nearest centroid
3. Recalculate each centroid as the mean of its assigned points
4. Repeat steps 2-3 until the centroids stop moving (convergence)


IMPLEMENTATION
--------------

a) Import Libraries

    import numpy as np
    import matplotlib.pyplot as plt
    from sklearn.cluster import KMeans

b) Create the NumPy Array

    # Each row is one data point: [X-value, Y-value]
    data_points = np.array([
        [1.5, 2.4], [3.5, 4.2], [5.1, 5.8],
        [6.2, 7.4], [7.9, 8.2], [2.3, 3.5],
        [4.6, 4.9], [6.3, 6.1], [7.5, 7.9],
        [3.4, 4.0],
    ])

c) Apply K-Means

    # n_clusters=3: split into 3 groups
    # random_state=42: ensures reproducible results
    kmeans_model = KMeans(n_clusters=3, random_state=42)

    # fit_predict: trains the model and returns a cluster label per point
    cluster_labels = kmeans_model.fit_predict(data_points)

d) Plot Clusters and Centroids

    # Data points colored by cluster
    plt.scatter(data_points[:, 0], data_points[:, 1],
                c=cluster_labels, cmap="viridis", label="Data Points")

    # Centroids as large red X markers
    plt.scatter(kmeans_model.cluster_centers_[:, 0],
                kmeans_model.cluster_centers_[:, 1],
                c="red", marker="X", s=200, label="Centroids")

    plt.title("K-Means Clustering (k=3)")
    plt.xlabel("X Value")
    plt.ylabel("Y Value")
    plt.legend()
    plt.show()


RESULT
------
The plot shows 3 color-coded clusters with a red X centroid at the center of
each group. The data follows a natural diagonal trend and K-Means correctly
identifies three distinct regions along it.