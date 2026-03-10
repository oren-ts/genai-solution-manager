# =============================================================================
# 11.Ü.01 - K-Means Clustering
# =============================================================================
# Unsupervised learning: group 200 randomly generated points into 4 clusters
# using the K-Means algorithm from scikit-learn.
# =============================================================================

import matplotlib.pyplot as plt
from sklearn.cluster import KMeans
from sklearn.datasets import make_blobs


# -----------------------------------------------------------------------------
# Step a) Create the dataset
# -----------------------------------------------------------------------------
# make_blobs generates synthetic clustered data — ideal for testing clustering
# algorithms because the groups are clearly separated and spherical.
# random_state=42 ensures we get the same dataset every time we run the script.

X, y = make_blobs(
    n_samples=200,  # total number of data points
    n_features=2,  # 2 features → can be plotted as x and y coordinates
    centers=4,  # generate 4 cluster groups
    cluster_std=0.60,  # how spread out points are around each center
    random_state=42,  # fix the random seed for reproducibility
)


# -----------------------------------------------------------------------------
# Step b) Visualize the raw dataset (before clustering)
# -----------------------------------------------------------------------------
# At this stage the algorithm has not run yet — all points look identical.
# We can already see 4 natural groups, which is what K-Means will discover.

plt.scatter(
    X[:, 0],  # x-axis: first feature (all rows, column 0)
    X[:, 1],  # y-axis: second feature (all rows, column 1)
    c="white",  # fill color: white
    marker="o",  # marker shape: circle
    edgecolors="black",  # border color: black
    s=50,  # marker size
)

plt.title("Raw Dataset (before clustering)")
plt.grid()
plt.tight_layout()
plt.show()


# -----------------------------------------------------------------------------
# Step c) K-Means Clustering
# -----------------------------------------------------------------------------
# KMeans finds k cluster centers and assigns every point to its nearest center.
# The algorithm repeats until the centers stop moving (convergence).
# n_init=10 means it runs 10 times with different starting centers and keeps
# the best result (lowest SSE), making the outcome more reliable.

km = KMeans(
    n_clusters=4,  # number of clusters to find (k = 4)
    init="random",  # choose initial cluster centers randomly
    n_init=10,  # run the algorithm 10 times, keep the best result
    max_iter=300,  # maximum number of update cycles per run
    tol=1e-04,  # stop early if improvement drops below this threshold
    random_state=0,  # fix the random seed for reproducibility
)

# fit_predict: runs the algorithm on X and returns a cluster ID for each point
# y_km[i] tells us which cluster point i was assigned to (0, 1, 2, or 3)
y_km = km.fit_predict(X)


# -----------------------------------------------------------------------------
# Step d) Visualize the cluster centers
# -----------------------------------------------------------------------------
# We re-draw the data points and add the 4 cluster centers on top.
# km.cluster_centers_ is a (4, 2) array: one row per center, two coordinates.
# The centers are drawn as large red squares so they stand out clearly.

plt.scatter(
    X[:, 0],
    X[:, 1],
    c="white",
    marker="o",
    edgecolors="black",
    s=50,
    label="Data points",
)

plt.scatter(
    km.cluster_centers_[:, 0],  # x-coordinates of all 4 cluster centers
    km.cluster_centers_[:, 1],  # y-coordinates of all 4 cluster centers
    s=100,  # large size so centers are clearly visible
    marker="s",  # square marker shape
    c="red",  # red fill to stand out
    edgecolors="black",  # black border for contrast
    label="Cluster centers",
)

plt.title("K-Means Clustering — Cluster Centers")
plt.legend()
plt.grid()
plt.tight_layout()
plt.show()


# -----------------------------------------------------------------------------
# Step e) Calculate and output the SSE
# -----------------------------------------------------------------------------
# SSE (Sum of Squared Errors) = sum of squared distances from each point
# to its assigned cluster center. Lower SSE = more compact clusters.
# scikit-learn stores this value in the km.inertia_ attribute after fitting.

print(f"Sum of squared deviations within the clusters (SSE): {km.inertia_}")
