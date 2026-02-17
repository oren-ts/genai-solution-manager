# =============================================================================
# task1_data_prep.py
# Task Package 1: Data Preparation and Understanding
# Project: Handwritten Digit Recognizer (K4.0059)
# Tools: Python, NumPy, PIL (Pillow) only
# =============================================================================
# This file covers all three work packages for Task 1:
#   1.1 - PIL and NumPy basics
#   1.2 - MNIST download, PIL visualization, normalization
#   1.3 - NumPy array preparation and train/test split
# =============================================================================

import os
import struct
import urllib.request

import numpy as np
from PIL import Image

# We use matplotlib only for visualization — it is not used in the neural network
import matplotlib.pyplot as plt


# =============================================================================
# WORK PACKAGE 1.1 — PIL and NumPy Basics
# =============================================================================
# Before working with MNIST, we establish fluency with the two core tools.
# PIL handles images as objects; NumPy handles them as numerical arrays.
# The bridge between them is np.array(pil_image) and Image.fromarray(np_array).

def demo_numpy_basics():
    """
    Demonstrates the NumPy operations we will rely on throughout the project:
    - Creating and reshaping arrays
    - Slicing and indexing
    - Element-wise math (the basis of all neural network operations)
    - Broadcasting (applying an operation to every element efficiently)
    """
    print("=" * 50)
    print("NumPy Basics Demo")
    print("=" * 50)

    # A 1D array — this is the shape a single flattened MNIST image will have
    # MNIST images are 28x28 pixels = 784 values
    pixel_values = np.array([0, 64, 128, 192, 255], dtype=np.float32)
    print(f"1D array: {pixel_values}")
    print(f"Shape: {pixel_values.shape}")  # (5,) — a vector with 5 elements

    # A 2D array — this represents a tiny 2x3 grayscale image
    tiny_image = np.array([
        [10, 20, 30],
        [40, 50, 60]
    ], dtype=np.float32)
    print(f"\n2D array (tiny image):\n{tiny_image}")
    print(f"Shape: {tiny_image.shape}")    # (2, 3) — 2 rows, 3 columns

    # Flattening: converting a 2D image into a 1D vector
    # This is exactly what we do to each MNIST image before feeding it to the network
    flat = tiny_image.flatten()
    print(f"\nFlattened: {flat}")
    print(f"Shape after flatten: {flat.shape}")  # (6,) — all values in one row

    # Normalization: scaling pixel values from [0, 255] to [0.0, 1.0]
    # Neural networks train faster and more stably with small input values
    normalized = pixel_values / 255.0
    print(f"\nOriginal pixels:    {pixel_values}")
    print(f"Normalized [0,1]:   {normalized}")

    # Broadcasting: NumPy applies the division to every element automatically
    # No need for a loop — this is both cleaner and much faster

    # Stacking: combining multiple 1D vectors into a 2D matrix
    # This is how we build a batch of training examples
    vec_a = np.array([1.0, 2.0, 3.0])
    vec_b = np.array([4.0, 5.0, 6.0])
    matrix = np.vstack([vec_a, vec_b])
    print(f"\nStacked matrix:\n{matrix}")
    print(f"Shape: {matrix.shape}")  # (2, 3) — 2 samples, 3 features each

    # Indexing: accessing rows and columns
    print(f"\nFirst row (sample 0):   {matrix[0]}")
    print(f"Second column:          {matrix[:, 1]}")  # all rows, column index 1


def demo_pil_basics():
    """
    Demonstrates the PIL operations we will use to handle MNIST images:
    - Creating an image from a NumPy array
    - Reading pixel values back
    - Resizing (not needed for MNIST, but good to know)
    - Converting to grayscale mode
    """
    print("\n" + "=" * 50)
    print("PIL Basics Demo")
    print("=" * 50)

    # Create a simple 8x8 gradient image using NumPy, then hand it to PIL
    # np.linspace generates 64 evenly spaced values between 0 and 255
    gradient_pixels = np.linspace(0, 255, 64, dtype=np.uint8).reshape(8, 8)
    print(f"NumPy pixel array:\n{gradient_pixels}")

    # PIL expects uint8 (integers 0–255) for a standard grayscale image
    # Mode 'L' = 8-bit grayscale (L stands for Luminance)
    pil_img = Image.fromarray(gradient_pixels, mode='L')
    print(f"\nPIL Image: {pil_img}")
    print(f"Size (width x height): {pil_img.size}")
    print(f"Mode: {pil_img.mode}")

    # Round-trip: convert PIL image back to NumPy for computation
    # This is the standard workflow — PIL for I/O, NumPy for math
    back_to_numpy = np.array(pil_img)
    print(f"\nBack to NumPy shape: {back_to_numpy.shape}")

    # Save the demo image so we can inspect it visually
    os.makedirs("data", exist_ok=True)
    pil_img.save("data/demo_gradient.png")
    print("Saved demo image to data/demo_gradient.png")

    # Show pixel statistics — useful for verifying normalization later
    print(f"\nPixel stats:")
    print(f"  min = {back_to_numpy.min()}")
    print(f"  max = {back_to_numpy.max()}")
    print(f"  mean = {back_to_numpy.mean():.2f}")


# =============================================================================
# WORK PACKAGE 1.2 — Download MNIST, Visualize with PIL, Normalize
# =============================================================================
# MNIST is distributed in a custom binary format (.idx). We parse it manually
# using Python's struct module — no sklearn or external loaders.
#
# The files are available from Yann LeCun's site (now mirrored on ossci-datasets).
# Each file contains a header (magic number + dimensions) followed by raw bytes.

MNIST_URL_BASE = "https://ossci-datasets.s3.amazonaws.com/mnist/"

MNIST_FILES = {
    "train_images": "train-images-idx3-ubyte.gz",
    "train_labels": "train-labels-idx1-ubyte.gz",
    "test_images":  "t10k-images-idx3-ubyte.gz",
    "test_labels":  "t10k-labels-idx1-ubyte.gz",
}


def download_mnist(data_dir="data/mnist"):
    """
    Downloads the four MNIST files from the ossci-datasets mirror.
    Skips files that already exist — safe to call repeatedly.
    """
    import gzip
    import shutil

    os.makedirs(data_dir, exist_ok=True)

    for key, filename in MNIST_FILES.items():
        gz_path = os.path.join(data_dir, filename)
        raw_path = gz_path.replace(".gz", "")

        # Skip if already downloaded and decompressed
        if os.path.exists(raw_path):
            print(f"Already exists: {raw_path}")
            continue

        url = MNIST_URL_BASE + filename
        print(f"Downloading {filename} ...")
        urllib.request.urlretrieve(url, gz_path)

        # Decompress the .gz file into a plain binary file
        print(f"Decompressing {filename} ...")
        with gzip.open(gz_path, 'rb') as f_in:
            with open(raw_path, 'wb') as f_out:
                shutil.copyfileobj(f_in, f_out)

        # Remove the .gz file to save space
        os.remove(gz_path)
        print(f"Ready: {raw_path}")


def load_mnist_images(filepath):
    """
    Parses an MNIST image file in idx3-ubyte format.

    IDX3 file layout:
      - 4 bytes: magic number (0x00000803)
      - 4 bytes: number of images
      - 4 bytes: number of rows (28)
      - 4 bytes: number of columns (28)
      - Remaining bytes: pixel data (one byte per pixel, row-major order)

    Returns a NumPy array of shape (N, 28, 28) with dtype uint8.
    """
    with open(filepath, 'rb') as f:
        # struct.unpack reads binary data; '>IIII' = 4 big-endian unsigned ints
        magic, num_images, rows, cols = struct.unpack('>IIII', f.read(16))

        # Verify we opened the right file type
        assert magic == 2051, f"Invalid magic number {magic} — expected 2051 for images"

        # Read all remaining bytes as a flat NumPy array, then reshape
        raw = np.frombuffer(f.read(), dtype=np.uint8)
        images = raw.reshape(num_images, rows, cols)

    print(f"Loaded images: {images.shape} | dtype: {images.dtype}")
    return images


def load_mnist_labels(filepath):
    """
    Parses an MNIST label file in idx1-ubyte format.

    IDX1 file layout:
      - 4 bytes: magic number (0x00000801)
      - 4 bytes: number of labels
      - Remaining bytes: label data (one byte per label, value 0–9)

    Returns a NumPy array of shape (N,) with dtype uint8.
    """
    with open(filepath, 'rb') as f:
        magic, num_labels = struct.unpack('>II', f.read(8))
        assert magic == 2049, f"Invalid magic number {magic} — expected 2049 for labels"

        labels = np.frombuffer(f.read(), dtype=np.uint8)

    print(f"Loaded labels: {labels.shape} | dtype: {labels.dtype}")
    return labels


def visualize_samples_with_pil(images, labels, num_samples=10, save_path="data/sample_digits.png"):
    """
    Creates a single image strip showing `num_samples` digits side by side.
    Each digit is loaded as a PIL Image, then composited into one canvas.

    This demonstrates PIL's role: we use it to inspect what the data looks like
    before converting everything to floats for computation.
    """
    # Each MNIST image is 28x28; we lay them out in a row with 4px gaps
    gap = 4
    canvas_w = num_samples * 28 + (num_samples - 1) * gap
    canvas_h = 28
    canvas = Image.new('L', (canvas_w, canvas_h), color=240)  # light gray background

    for i in range(num_samples):
        # images[i] is a (28, 28) uint8 array — PIL accepts this directly
        digit_img = Image.fromarray(images[i], mode='L')
        x_offset = i * (28 + gap)
        canvas.paste(digit_img, (x_offset, 0))

    canvas.save(save_path)
    print(f"Saved {num_samples} sample digits to {save_path}")
    print(f"Labels: {labels[:num_samples]}")

    return canvas


def normalize_images(images):
    """
    Converts pixel values from uint8 [0, 255] to float32 [0.0, 1.0].

    Why normalize?
    - Neural network weights are initialized near zero.
    - With raw pixel values (0–255), the weighted sums would be enormous,
      pushing the sigmoid function into its flat saturation regions.
    - Normalized inputs keep activations in a useful range and make
      gradient descent converge much faster.
    """
    # Convert to float32 first, then divide — integer division would give all zeros
    normalized = images.astype(np.float32) / 255.0
    print(f"Normalized: min={normalized.min():.3f}, max={normalized.max():.3f}, "
          f"mean={normalized.mean():.3f}")
    return normalized


# =============================================================================
# WORK PACKAGE 1.3 — Prepare Arrays and Split Train/Test
# =============================================================================
# The neural network expects:
#   - Inputs as flat 1D vectors: shape (784,) per sample → batch: (N, 784)
#   - Labels as one-hot encoded vectors: shape (10,) per sample
#     e.g. digit 3 → [0, 0, 0, 1, 0, 0, 0, 0, 0, 0]

def flatten_images(images):
    """
    Reshapes (N, 28, 28) → (N, 784).

    The network has no concept of 2D spatial structure — it sees each image
    as a flat list of 784 pixel intensities (28*28 = 784).
    """
    N = images.shape[0]
    flat = images.reshape(N, 784)
    print(f"Flattened: {images.shape} → {flat.shape}")
    return flat


def one_hot_encode(labels, num_classes=10):
    """
    Converts integer labels [0–9] into one-hot encoded vectors.

    Why one-hot?
    - Our network outputs 10 values (one per digit class) via sigmoid.
    - To compute loss and gradients, we need the target in the same format:
      a vector of 0s with a single 1 at the correct class position.
    - If we used raw integers, the math would incorrectly imply that
      digit '9' is 'larger' or 'more correct' than digit '1'.

    Example: label 3 → [0, 0, 0, 1, 0, 0, 0, 0, 0, 0]
    """
    N = len(labels)
    one_hot = np.zeros((N, num_classes), dtype=np.float32)

    # For each sample i, set the column equal to its label to 1.0
    # np.arange(N) gives [0, 1, 2, ..., N-1] — we use it to index all rows at once
    one_hot[np.arange(N), labels] = 1.0

    print(f"One-hot encoded: {labels.shape} → {one_hot.shape}")
    print(f"Example — label {labels[0]} → {one_hot[0]}")
    return one_hot


def verify_split(X_train, y_train, X_test, y_test):
    """
    Prints a summary of the final dataset split to verify everything is correct
    before we pass it to the neural network.
    """
    print("\n" + "=" * 50)
    print("Dataset Summary")
    print("=" * 50)
    print(f"X_train shape : {X_train.shape}")   # (60000, 784)
    print(f"y_train shape : {y_train.shape}")   # (60000, 10)
    print(f"X_test shape  : {X_test.shape}")    # (10000, 784)
    print(f"y_test shape  : {y_test.shape}")    # (10000, 10)
    print(f"X dtype       : {X_train.dtype}")   # float32
    print(f"y dtype       : {y_train.dtype}")   # float32
    print(f"X value range : [{X_train.min():.2f}, {X_train.max():.2f}]")
    print(f"Label sample  : {np.argmax(y_train[:5], axis=1)}")  # decode back to ints


def plot_label_distribution(labels_int, title="Label Distribution", save_path=None):
    """
    Bar chart of how many samples exist per digit class.
    MNIST is roughly balanced (~6000 per class in training set).
    Verifying balance matters: a heavily imbalanced dataset would bias the network.
    """
    counts = np.bincount(labels_int, minlength=10)
    plt.figure(figsize=(8, 4))
    plt.bar(range(10), counts, color='steelblue', edgecolor='black')
    plt.xlabel("Digit Class")
    plt.ylabel("Number of Samples")
    plt.title(title)
    plt.xticks(range(10))
    for i, c in enumerate(counts):
        plt.text(i, c + 50, str(c), ha='center', fontsize=8)
    plt.tight_layout()
    if save_path:
        plt.savefig(save_path)
        print(f"Saved plot to {save_path}")
    plt.show()


# =============================================================================
# MAIN — Run all three work packages in sequence
# =============================================================================

if __name__ == "__main__":

    # --- 1.1: PIL and NumPy Basics ---
    demo_numpy_basics()
    demo_pil_basics()

    # --- 1.2: Download and Load MNIST ---
    DATA_DIR = "data/mnist"
    download_mnist(DATA_DIR)

    train_images_raw = load_mnist_images(os.path.join(DATA_DIR, "train-images-idx3-ubyte"))
    train_labels_raw = load_mnist_labels(os.path.join(DATA_DIR, "train-labels-idx1-ubyte"))
    test_images_raw  = load_mnist_images(os.path.join(DATA_DIR, "t10k-images-idx3-ubyte"))
    test_labels_raw  = load_mnist_labels(os.path.join(DATA_DIR, "t10k-labels-idx1-ubyte"))

    # Visualize 10 samples using PIL before any processing
    visualize_samples_with_pil(train_images_raw, train_labels_raw,
                                num_samples=10, save_path="data/sample_digits.png")

    # Normalize pixel values from [0,255] to [0.0, 1.0]
    train_images_norm = normalize_images(train_images_raw)
    test_images_norm  = normalize_images(test_images_raw)

    # --- 1.3: Prepare Arrays for Training ---
    X_train = flatten_images(train_images_norm)  # (60000, 784)
    X_test  = flatten_images(test_images_norm)   # (10000, 784)

    y_train = one_hot_encode(train_labels_raw)   # (60000, 10)
    y_test  = one_hot_encode(test_labels_raw)    # (10000, 10)

    # Verify the final shapes and data types
    verify_split(X_train, y_train, X_test, y_test)

    # Visualize class distribution in training set
    plot_label_distribution(train_labels_raw, title="MNIST Training Set — Class Distribution",
                            save_path="data/label_distribution.png")

    # Save prepared arrays for use in Task 2
    # We save to data/ which is gitignored — dataset files never go into the repo
    np.save("data/X_train.npy", X_train)
    np.save("data/y_train.npy", y_train)
    np.save("data/X_test.npy",  X_test)
    np.save("data/y_test.npy",  y_test)
    print("\nArrays saved to data/ — ready for Task Package 2.")
