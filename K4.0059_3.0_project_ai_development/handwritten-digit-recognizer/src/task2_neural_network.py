# =============================================================================
# task2_neural_network.py
# Task Package 2: Design and Implementation of the Neural Network
# Project: Handwritten Digit Recognizer (K4.0059)
# Tools: Python, NumPy only
# =============================================================================
# This file covers all three work packages for Task 2:
#   2.1 - Network architecture: input, hidden, output layers with sigmoid
#   2.2 - Parameter initialization, learning rate, loss function
#   2.3 - Forward pass and backpropagation on a subset of the dataset
# =============================================================================

import numpy as np


# =============================================================================
# WORK PACKAGE 2.1 — Network Architecture
# =============================================================================
# Architecture: 784 → 128 → 10
#
#   Input layer:   784 neurons  (one per pixel in the flattened 28x28 image)
#   Hidden layer:  128 neurons  (learns intermediate features like edges, curves)
#   Output layer:  10 neurons   (one per digit class 0–9)
#
# Why 128 hidden neurons?
#   - Large enough to capture meaningful patterns in the data
#   - Small enough to train in reasonable time without GPU
#   - A power of 2 — efficient for NumPy's memory alignment
#
# Why sigmoid everywhere?
#   - Assignment requirement
#   - Sigmoid maps any real number to (0, 1), which works for both
#     hidden activations and output probabilities
#   - Note: in practice ReLU is preferred for hidden layers due to
#     faster training, but sigmoid is perfectly valid for a learning project

INPUT_SIZE  = 784   # 28 * 28 pixels
HIDDEN_SIZE = 128   # hidden layer neurons
OUTPUT_SIZE = 10    # digit classes 0–9


def sigmoid(z):
    """
    The sigmoid activation function: σ(z) = 1 / (1 + e^(-z))

    Maps any real number to the open interval (0, 1).
    - Large positive z → output close to 1 (strongly activated)
    - Large negative z → output close to 0 (not activated)
    - z = 0 → output = 0.5 (neutral)

    Applied element-wise to NumPy arrays — no loop needed.
    """
    return 1.0 / (1.0 + np.exp(-z))


def sigmoid_derivative(a):
    """
    Derivative of sigmoid in terms of its own output: σ'(z) = σ(z) * (1 - σ(z))

    We pass in `a` (the already-computed sigmoid output) rather than `z`,
    which avoids recomputing sigmoid during backpropagation.

    This derivative tells us how much the sigmoid output changes with
    respect to its input — essential for computing gradients in backprop.
    """
    return a * (1.0 - a)


# =============================================================================
# WORK PACKAGE 2.2 — Parameter Initialization, Learning Rate, Loss Function
# =============================================================================

def initialize_parameters(input_size=INPUT_SIZE,
                           hidden_size=HIDDEN_SIZE,
                           output_size=OUTPUT_SIZE,
                           seed=42):
    """
    Initializes weights and biases for both layers.

    Weight initialization strategy: small random values scaled by 0.01
    ─────────────────────────────────────────────────────────────────────
    Why not zeros?
      If all weights start at zero, every neuron computes the same output
      and receives the same gradient — the network never learns distinct
      features. This is called the "symmetry problem."

    Why small random values?
      - Random breaks symmetry: each neuron starts different, so they
        learn different features.
      - Small (×0.01) keeps the initial weighted sums near zero, which
        puts sigmoid in its most responsive region (slope ≈ 0.25 at z=0).
      - Large initial weights push sigmoid into saturation (slope ≈ 0),
        causing vanishing gradients where learning effectively stops.

    Shapes:
      W1: (hidden_size, input_size)  = (128, 784)  — input → hidden weights
      b1: (hidden_size, 1)           = (128, 1)    — hidden layer biases
      W2: (output_size, hidden_size) = (10, 128)   — hidden → output weights
      b2: (output_size, 1)           = (10, 1)     — output layer biases

    Returns a dict so we can pass all parameters around as a single object.
    """
    np.random.seed(seed)  # reproducibility — same init every run

    params = {
        'W1': np.random.randn(hidden_size, input_size)  * 0.01,
        'b1': np.zeros((hidden_size, 1)),
        'W2': np.random.randn(output_size, hidden_size) * 0.01,
        'b2': np.zeros((output_size, 1)),
    }

    print("Parameter shapes:")
    for name, arr in params.items():
        print(f"  {name}: {arr.shape}")

    return params


# Learning rate: controls the step size during gradient descent
# ─────────────────────────────────────────────────────────────
# Too large → overshoots the minimum, loss oscillates or diverges
# Too small → converges very slowly
# 0.1 is a standard starting point for sigmoid networks
LEARNING_RATE = 0.1


def compute_loss(y_pred, y_true):
    """
    Binary cross-entropy loss, averaged over all samples in the batch.

    Formula (per sample, per output neuron):
        L = -[ y * log(ŷ) + (1 - y) * log(1 - ŷ) ]

    Why cross-entropy and not mean squared error?
    ─────────────────────────────────────────────
    With sigmoid outputs and MSE, gradients become very small when the
    network is confidently wrong (sigmoid saturated). Cross-entropy loss
    fixes this: its gradient with respect to the output is simply (ŷ - y),
    which is large when the prediction is far from the target.

    Arguments:
        y_pred: network output after sigmoid, shape (N, 10)
        y_true: one-hot encoded labels,       shape (N, 10)

    Returns:
        scalar loss value (float)
    """
    N = y_true.shape[0]

    # Clip predictions to avoid log(0) which would give -infinity
    # 1e-8 is small enough not to affect the math meaningfully
    y_pred_clipped = np.clip(y_pred, 1e-8, 1 - 1e-8)

    # Compute per-element loss, then average over all N samples and 10 outputs
    loss = -np.mean(
        y_true * np.log(y_pred_clipped) + (1 - y_true) * np.log(1 - y_pred_clipped)
    )
    return loss


# =============================================================================
# WORK PACKAGE 2.3 — Forward Pass and Backpropagation
# =============================================================================

def forward_pass(X, params):
    """
    Computes the network output for a batch of inputs.

    For each layer:
      1. Compute the weighted sum (linear combination): Z = W·X + b
      2. Apply sigmoid activation:                      A = σ(Z)

    Shapes (for a batch of N samples):
      X:   (N, 784)   — input batch
      W1:  (128, 784) — transposed to (784, 128) for the dot product
      Z1:  (N, 128)   — hidden layer pre-activation
      A1:  (N, 128)   — hidden layer post-activation
      W2:  (10, 128)  — transposed to (128, 10) for the dot product
      Z2:  (N, 10)    — output layer pre-activation
      A2:  (N, 10)    — output layer post-activation = final predictions

    We cache Z1, A1, Z2, A2 because backpropagation needs them to
    compute gradients — we don't want to recompute them.

    Arguments:
        X:      input batch,    shape (N, 784)
        params: dict with W1, b1, W2, b2

    Returns:
        A2:   output predictions, shape (N, 10)
        cache: dict of intermediate values needed for backprop
    """
    W1, b1 = params['W1'], params['b1']
    W2, b2 = params['W2'], params['b2']

    # --- Hidden layer ---
    # X @ W1.T gives (N, 128): each sample dot-producted with each hidden neuron
    # b1.T broadcasts the bias across all N samples
    Z1 = X @ W1.T + b1.T   # shape: (N, 128)
    A1 = sigmoid(Z1)        # shape: (N, 128)

    # --- Output layer ---
    Z2 = A1 @ W2.T + b2.T  # shape: (N, 10)
    A2 = sigmoid(Z2)        # shape: (N, 10)

    cache = {'Z1': Z1, 'A1': A1, 'Z2': Z2, 'A2': A2, 'X': X}
    return A2, cache


def backpropagation(y_true, params, cache):
    """
    Computes gradients of the loss with respect to all parameters.

    Backpropagation applies the chain rule to propagate the error signal
    from the output layer back through the network to each weight.

    The key insight: to know how much weight W contributed to the loss,
    we multiply the gradients of each function in the chain:
        dL/dW = dL/dA2 · dA2/dZ2 · dZ2/dW

    Step by step (output layer first, then hidden layer):

    Output layer:
      dL/dA2 = -(y/ŷ - (1-y)/(1-ŷ))       ← derivative of cross-entropy
      dA2/dZ2 = A2 * (1 - A2)              ← derivative of sigmoid
      Combined: dZ2 = A2 - y_true           ← simplifies cleanly with cross-entropy + sigmoid
      dW2 = dZ2.T @ A1 / N
      db2 = mean(dZ2, over samples)

    Hidden layer:
      dA1 = dZ2 @ W2                        ← error propagated back through W2
      dZ1 = dA1 * sigmoid_derivative(A1)    ← through the hidden sigmoid
      dW1 = dZ1.T @ X / N
      db1 = mean(dZ1, over samples)

    Arguments:
        y_true: one-hot labels, shape (N, 10)
        params: dict with current weights
        cache:  dict of intermediate values from forward pass

    Returns:
        grads: dict of gradients for W1, b1, W2, b2
    """
    N  = y_true.shape[0]
    A1 = cache['A1']
    A2 = cache['A2']
    X  = cache['X']
    W2 = params['W2']

    # --- Output layer gradients ---
    # With cross-entropy loss + sigmoid output, the combined gradient simplifies to (A2 - y)
    # This is one of the elegant results in neural network math
    dZ2 = A2 - y_true                           # shape: (N, 10)
    dW2 = (dZ2.T @ A1) / N                      # shape: (10, 128)
    db2 = np.mean(dZ2, axis=0, keepdims=True).T # shape: (10, 1)

    # --- Hidden layer gradients ---
    # Propagate error back through W2, then through the sigmoid derivative
    dA1 = dZ2 @ W2                              # shape: (N, 128)
    dZ1 = dA1 * sigmoid_derivative(A1)          # shape: (N, 128) — element-wise
    dW1 = (dZ1.T @ X) / N                       # shape: (128, 784)
    db1 = np.mean(dZ1, axis=0, keepdims=True).T # shape: (128, 1)

    grads = {'dW1': dW1, 'db1': db1, 'dW2': dW2, 'db2': db2}
    return grads


def update_parameters(params, grads, learning_rate=LEARNING_RATE):
    """
    Applies gradient descent: moves each parameter slightly in the direction
    that reduces the loss.

    Update rule: W = W - α * dW
      α (alpha) is the learning rate — controls the step size
      dW is the gradient — points in the direction of steepest ascent
      Subtracting moves us toward lower loss (descending the gradient)
    """
    params['W1'] -= learning_rate * grads['dW1']
    params['b1'] -= learning_rate * grads['db1']
    params['W2'] -= learning_rate * grads['dW2']
    params['b2'] -= learning_rate * grads['db2']
    return params


def predict(X, params):
    """
    Runs a forward pass and returns the predicted digit class for each sample.
    The predicted class is the output neuron with the highest activation.
    """
    A2, _ = forward_pass(X, params)
    return np.argmax(A2, axis=1)  # index of max value across the 10 output neurons


def compute_accuracy(X, y_true_int, params):
    """
    Computes classification accuracy: fraction of correctly predicted samples.

    Arguments:
        X:          input array,          shape (N, 784)
        y_true_int: integer labels [0–9], shape (N,)
        params:     current network parameters
    """
    predictions = predict(X, params)
    accuracy = np.mean(predictions == y_true_int)
    return accuracy


# =============================================================================
# MAIN — Smoke test on a small subset before full training in Task 3
# =============================================================================

if __name__ == "__main__":

    # Load the prepared arrays from Task 1
    print("Loading data prepared in Task 1...")
    X_train = np.load("data/X_train.npy")
    y_train = np.load("data/y_train.npy")
    X_test  = np.load("data/X_test.npy")
    y_test  = np.load("data/y_test.npy")

    # Integer labels for accuracy computation (argmax reverses one-hot)
    y_train_int = np.argmax(y_train, axis=1)
    y_test_int  = np.argmax(y_test,  axis=1)

    # Use a small subset for this smoke test — full training is Task 3
    SUBSET_SIZE = 1000
    X_sub = X_train[:SUBSET_SIZE]
    y_sub = y_train[:SUBSET_SIZE]
    y_sub_int = y_train_int[:SUBSET_SIZE]

    # Initialize parameters
    print("\nInitializing network parameters...")
    params = initialize_parameters()

    # Verify forward pass output shape and value range
    print("\nRunning forward pass on subset...")
    A2, cache = forward_pass(X_sub, params)
    print(f"Output shape: {A2.shape}")           # should be (1000, 10)
    print(f"Output range: [{A2.min():.4f}, {A2.max():.4f}]")  # should be near (0, 1)
    print(f"Sample prediction (first 5): {np.argmax(A2[:5], axis=1)}")

    # Compute initial loss — should be around log(10) ≈ 2.303 for random weights
    # (random guessing across 10 classes gives ~10% accuracy → loss ≈ 2.3)
    initial_loss = compute_loss(A2, y_sub)
    print(f"\nInitial loss: {initial_loss:.4f}  (expected ≈ 2.3 for random weights)")

    # Compute initial accuracy — should be around 10% (random chance)
    initial_acc = compute_accuracy(X_sub, y_sub_int, params)
    print(f"Initial accuracy: {initial_acc * 100:.1f}%  (expected ≈ 10% for random weights)")

    # Run one training step to verify backprop works without errors
    print("\nRunning one backpropagation step...")
    grads = backpropagation(y_sub, params, cache)
    print("Gradient shapes:")
    for name, g in grads.items():
        print(f"  {name}: {g.shape}")

    # Apply one gradient update
    params = update_parameters(params, grads)

    # Recompute loss — should be slightly lower after one update
    A2_after, _ = forward_pass(X_sub, params)
    loss_after = compute_loss(A2_after, y_sub)
    print(f"\nLoss after one update: {loss_after:.4f}  (should be slightly lower than {initial_loss:.4f})")

    # Quick training loop on subset — 50 epochs to verify learning happens
    print("\nRunning 50 epochs on subset to verify learning...")
    params = initialize_parameters()  # reset to fresh weights

    for epoch in range(50):
        A2, cache = forward_pass(X_sub, params)
        loss = compute_loss(A2, y_sub)
        grads = backpropagation(y_sub, params, cache)
        params = update_parameters(params, grads)

        if epoch % 10 == 0:
            acc = compute_accuracy(X_sub, y_sub_int, params)
            print(f"  Epoch {epoch:3d} | Loss: {loss:.4f} | Accuracy: {acc * 100:.1f}%")

    print("\nSmoke test complete. Full training in Task Package 3.")
