import numpy as np
import matplotlib.pyplot as plt
from sklearn.svm import SVC

# ── Part c) Decision boundary visualisation function ──────────────────────────


def plot_decision_regions(data_points, class_labels, classifier, resolution=0.02):
    # Define marker shapes and a colormap for the two classes
    markers = ("s", "x", "o", "^", "v")
    cmap = plt.cm.brg

    # Find the min/max range of each feature to define the plot boundaries
    x1_min, x1_max = data_points[:, 0].min() - 1, data_points[:, 0].max() + 1
    x2_min, x2_max = data_points[:, 1].min() - 1, data_points[:, 1].max() + 1

    # Create a fine grid of points covering the entire plot area
    grid_x1, grid_x2 = np.meshgrid(
        np.arange(x1_min, x1_max, resolution), np.arange(x2_min, x2_max, resolution)
    )

    # Predict the class for every point on the grid to create the background regions
    grid_predictions = classifier.predict(
        np.array([grid_x1.ravel(), grid_x2.ravel()]).T
    )
    grid_predictions = grid_predictions.reshape(grid_x1.shape)

    # Draw the colored background regions
    plt.contourf(grid_x1, grid_x2, grid_predictions, alpha=0.4, cmap=cmap)
    plt.xlim(grid_x1.min(), grid_x1.max())
    plt.ylim(grid_x2.min(), grid_x2.max())

    # Plot each class's data points with a distinct marker and color
    for class_index, class_label in enumerate(np.unique(class_labels)):
        plt.scatter(
            x=data_points[class_labels == class_label, 0],
            y=data_points[class_labels == class_label, 1],
            alpha=0.8,
            c=[cmap(class_index)],
            marker=markers[class_index],
            label=class_label,
        )


# ── Part a) Generate XOR dataset ──────────────────────────────────────────────

np.random.seed(1)  # Fix random state so results are reproducible

xor_data_points = np.random.randn(200, 2)  # 200 random points with 2 features (x and y)

# XOR logic: a point is "true" if exactly one of its two features is positive
xor_boolean_labels = np.logical_xor(
    xor_data_points[:, 0] > 0, xor_data_points[:, 1] > 0
)

# Convert True/False to class labels 1 and -1
xor_class_labels = np.where(xor_boolean_labels, 1, -1)

# ── Part b) Train SVM with RBF kernel ─────────────────────────────────────────

# RBF kernel handles non-linear boundaries; C controls penalty, gamma controls reach
svm_classifier = SVC(kernel="rbf", random_state=1, gamma=0.10, C=10.0)
svm_classifier.fit(xor_data_points, xor_class_labels)

# ── Part c) Visualise decision boundary ───────────────────────────────────────

plot_decision_regions(xor_data_points, xor_class_labels, classifier=svm_classifier)
plt.legend(loc="upper left")
plt.tight_layout()
plt.show()
