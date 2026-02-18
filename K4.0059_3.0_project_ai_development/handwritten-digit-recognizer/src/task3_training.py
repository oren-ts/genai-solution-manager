# =============================================================================
# task3_training.py
# Task Package 3: Training and Model Evaluation
# Project: Handwritten Digit Recognizer (K4.0059)
# Tools: Python, NumPy only
# =============================================================================
# This file covers all three work packages for Task 3:
#   3.1 - Train the model on the full dataset over multiple epochs
#   3.2 - Evaluate performance on test set with visualizations
#   3.3 - Analyze errors and identify improvement opportunities
# =============================================================================

import numpy as np
import matplotlib.pyplot as plt
from task2_neural_network import (
    initialize_parameters,
    forward_pass,
    compute_loss,
    backpropagation,
    update_parameters,
    predict,
    compute_accuracy
)


# =============================================================================
# WORK PACKAGE 3.1 — Train on Full Dataset Over Multiple Epochs
# =============================================================================
# An epoch is one complete pass through the entire training set.
# After each epoch, we evaluate on both train and test sets to monitor:
#   - Training loss: should decrease steadily
#   - Test loss: should decrease — if it starts rising, we're overfitting
#   - Train accuracy: should increase
#   - Test accuracy: should increase — this is our real performance metric

def train_model(X_train, y_train, X_test, y_test,
                epochs=100,
                learning_rate=0.1,
                batch_size=128,
                seed=42,
                verbose=True):
    """
    Trains the neural network using mini-batch gradient descent.

    Why mini-batches instead of full-batch?
    ────────────────────────────────────────
    With 60,000 samples, full-batch gradients are extremely small due to
    averaging. This causes vanishing gradients with sigmoid, where the network
    gets stuck predicting the most common class for everything.

    Mini-batches (128 samples) provide:
      - Stronger, noisier gradients that help escape local minima
      - Faster weight updates (469 updates per epoch vs 1)
      - Better generalization due to the noise

    Training loop (per epoch):
      1. Shuffle training set
      2. Split into mini-batches
      3. For each batch: forward → loss → backprop → update
      4. Evaluate on full train and test sets → track metrics

    Arguments:
        X_train:       training inputs,  shape (60000, 784)
        y_train:       training labels,  shape (60000, 10)
        X_test:        test inputs,      shape (10000, 784)
        y_test:        test labels,      shape (10000, 10)
        epochs:        number of full passes through the training set
        learning_rate: step size for gradient descent
        batch_size:    number of samples per mini-batch
        seed:          for reproducible weight initialization
        verbose:       print progress every 10 epochs

    Returns:
        params:  trained network parameters
        history: dict with train_loss, test_loss, train_acc, test_acc per epoch
    """
    # Initialize network
    params = initialize_parameters(seed=seed)

    # Integer labels for accuracy computation
    y_train_int = np.argmax(y_train, axis=1)
    y_test_int  = np.argmax(y_test,  axis=1)

    # Track metrics across epochs
    history = {
        'train_loss': [],
        'test_loss':  [],
        'train_acc':  [],
        'test_acc':   []
    }

    N = X_train.shape[0]
    num_batches = N // batch_size

    print(f"Starting training: {epochs} epochs, learning rate = {learning_rate}, batch size = {batch_size}")
    print(f"Batches per epoch: {num_batches}")
    print("=" * 70)

    np.random.seed(seed)

    for epoch in range(epochs):

        # --- Shuffle training data each epoch ---
        # This ensures each batch sees different samples, reducing overfitting
        shuffle_idx = np.random.permutation(N)
        X_shuffled = X_train[shuffle_idx]
        y_shuffled = y_train[shuffle_idx]

        # --- Mini-batch training ---
        for batch in range(num_batches):
            start = batch * batch_size
            end = start + batch_size

            X_batch = X_shuffled[start:end]
            y_batch = y_shuffled[start:end]

            # Forward pass on mini-batch
            A2_batch, cache = forward_pass(X_batch, params)

            # Backpropagation and weight update
            grads = backpropagation(y_batch, params, cache)
            params = update_parameters(params, grads, learning_rate=learning_rate)

        # --- Evaluation step (once per epoch on full sets) ---
        train_acc = compute_accuracy(X_train, y_train_int, params)

        A2_train, _ = forward_pass(X_train, params)
        train_loss = compute_loss(A2_train, y_train)

        A2_test, _ = forward_pass(X_test, params)
        test_loss = compute_loss(A2_test, y_test)
        test_acc = compute_accuracy(X_test, y_test_int, params)

        # Record metrics
        history['train_loss'].append(train_loss)
        history['test_loss'].append(test_loss)
        history['train_acc'].append(train_acc)
        history['test_acc'].append(test_acc)

        # Print progress
        if verbose and (epoch % 10 == 0 or epoch == epochs - 1):
            print(f"Epoch {epoch:3d} | "
                  f"Train Loss: {train_loss:.4f} | Train Acc: {train_acc*100:5.1f}% | "
                  f"Test Loss: {test_loss:.4f} | Test Acc: {test_acc*100:5.1f}%")

    print("=" * 70)
    print("Training complete.")
    return params, history


# =============================================================================
# WORK PACKAGE 3.2 — Evaluate Performance with Visualizations
# =============================================================================

def plot_training_curves(history, save_path=None):
    """
    Plots loss and accuracy curves over training epochs.

    What to look for:
      - Loss curves should decrease smoothly
      - Train and test curves should track each other closely
      - If test loss rises while train loss falls → overfitting
      - If both curves plateau early → underfitting (need more capacity or epochs)
    """
    epochs = range(len(history['train_loss']))

    fig, (ax1, ax2) = plt.subplots(1, 2, figsize=(14, 5))

    # Loss curves
    ax1.plot(epochs, history['train_loss'], label='Train Loss', color='steelblue', linewidth=2)
    ax1.plot(epochs, history['test_loss'],  label='Test Loss',  color='coral', linewidth=2)
    ax1.set_xlabel('Epoch')
    ax1.set_ylabel('Loss')
    ax1.set_title('Loss Over Training')
    ax1.legend()
    ax1.grid(alpha=0.3)

    # Accuracy curves
    ax2.plot(epochs, [a*100 for a in history['train_acc']], label='Train Accuracy', color='steelblue', linewidth=2)
    ax2.plot(epochs, [a*100 for a in history['test_acc']],  label='Test Accuracy',  color='coral', linewidth=2)
    ax2.set_xlabel('Epoch')
    ax2.set_ylabel('Accuracy (%)')
    ax2.set_title('Accuracy Over Training')
    ax2.legend()
    ax2.grid(alpha=0.3)

    plt.tight_layout()
    if save_path:
        plt.savefig(save_path, dpi=150)
        print(f"Saved training curves to {save_path}")
    plt.show()


def evaluate_final_performance(X_test, y_test, params):
    """
    Computes and prints final test set metrics.
    """
    y_test_int = np.argmax(y_test, axis=1)
    y_pred = predict(X_test, params)

    accuracy = np.mean(y_pred == y_test_int)
    print("\n" + "=" * 70)
    print("FINAL TEST SET PERFORMANCE")
    print("=" * 70)
    print(f"Test Accuracy: {accuracy * 100:.2f}%")
    print(f"Correct predictions: {np.sum(y_pred == y_test_int)} / {len(y_test_int)}")
    print("=" * 70)

    return accuracy


def plot_confusion_matrix(y_true, y_pred, save_path=None):
    """
    Confusion matrix: rows = true labels, columns = predicted labels
    Diagonal = correct predictions, off-diagonal = errors

    Useful for identifying which digits the network confuses with each other.
    Common confusions: 4↔9, 3↔8, 5↔6, 7↔1
    """
    # Build the 10×10 confusion matrix manually
    confusion = np.zeros((10, 10), dtype=int)
    for true, pred in zip(y_true, y_pred):
        confusion[true, pred] += 1

    # Normalize by row (true label) to get percentages
    confusion_pct = confusion.astype(float) / confusion.sum(axis=1, keepdims=True) * 100

    fig, ax = plt.subplots(figsize=(10, 8))
    im = ax.imshow(confusion_pct, cmap='Blues', vmin=0, vmax=100)

    # Annotate cells with both count and percentage
    for i in range(10):
        for j in range(10):
            count = confusion[i, j]
            pct = confusion_pct[i, j]
            color = 'white' if pct > 50 else 'black'
            ax.text(j, i, f'{count}\n({pct:.1f}%)', ha='center', va='center',
                    color=color, fontsize=9)

    ax.set_xticks(range(10))
    ax.set_yticks(range(10))
    ax.set_xlabel('Predicted Label', fontsize=12)
    ax.set_ylabel('True Label', fontsize=12)
    ax.set_title('Confusion Matrix (% of true label)', fontsize=14)
    plt.colorbar(im, ax=ax, label='Percentage')

    plt.tight_layout()
    if save_path:
        plt.savefig(save_path, dpi=150)
        print(f"Saved confusion matrix to {save_path}")
    plt.show()


def plot_per_digit_accuracy(y_true, y_pred, save_path=None):
    """
    Bar chart showing accuracy for each digit class individually.
    Identifies which digits the network struggles with most.
    """
    accuracies = []
    for digit in range(10):
        mask = (y_true == digit)
        if np.sum(mask) > 0:
            acc = np.mean(y_pred[mask] == y_true[mask])
            accuracies.append(acc * 100)
        else:
            accuracies.append(0)

    fig, ax = plt.subplots(figsize=(10, 5))
    bars = ax.bar(range(10), accuracies, color='steelblue', edgecolor='black')

    # Highlight the weakest digit
    min_idx = np.argmin(accuracies)
    bars[min_idx].set_color('coral')

    ax.set_xlabel('Digit Class', fontsize=12)
    ax.set_ylabel('Accuracy (%)', fontsize=12)
    ax.set_title('Per-Digit Accuracy', fontsize=14)
    ax.set_xticks(range(10))
    ax.set_ylim(0, 100)
    ax.grid(axis='y', alpha=0.3)

    for i, acc in enumerate(accuracies):
        ax.text(i, acc + 1, f'{acc:.1f}%', ha='center', fontsize=9)

    plt.tight_layout()
    if save_path:
        plt.savefig(save_path, dpi=150)
        print(f"Saved per-digit accuracy to {save_path}")
    plt.show()


# =============================================================================
# WORK PACKAGE 3.3 — Analyze Errors and Identify Improvement Opportunities
# =============================================================================

def visualize_misclassifications(X_test, y_test, params, num_examples=20, save_path=None):
    """
    Displays a grid of misclassified test samples.

    Shows the actual digit image, the true label, and the (wrong) predicted label.
    Helps identify patterns: are the errors ambiguous digits? systematic confusion?
    """
    y_test_int = np.argmax(y_test, axis=1)
    y_pred = predict(X_test, params)

    # Find all misclassified indices
    errors = np.where(y_pred != y_test_int)[0]

    if len(errors) == 0:
        print("No misclassifications found — perfect test accuracy!")
        return

    # Sample up to num_examples errors
    sample_errors = np.random.choice(errors, size=min(num_examples, len(errors)), replace=False)

    rows = 4
    cols = 5
    fig, axes = plt.subplots(rows, cols, figsize=(12, 10))
    axes = axes.flatten()

    for i, idx in enumerate(sample_errors):
        img = X_test[idx].reshape(28, 28)
        true_label = y_test_int[idx]
        pred_label = y_pred[idx]

        axes[i].imshow(img, cmap='gray')
        axes[i].set_title(f'True: {true_label}, Pred: {pred_label}', fontsize=10, color='red')
        axes[i].axis('off')

    # Hide unused subplots
    for i in range(len(sample_errors), rows * cols):
        axes[i].axis('off')

    plt.suptitle('Misclassified Test Samples', fontsize=14, y=0.98)
    plt.tight_layout()
    if save_path:
        plt.savefig(save_path, dpi=150)
        print(f"Saved misclassification examples to {save_path}")
    plt.show()


def analyze_errors(y_true, y_pred):
    """
    Prints a summary of the most common error types.

    Identifies which digit pairs are most frequently confused.
    Example output: "4 misclassified as 9: 87 times"
    """
    print("\n" + "=" * 70)
    print("ERROR ANALYSIS")
    print("=" * 70)

    # Count all (true, pred) pairs where true != pred
    error_pairs = {}
    for true, pred in zip(y_true, y_pred):
        if true != pred:
            pair = (true, pred)
            error_pairs[pair] = error_pairs.get(pair, 0) + 1

    # Sort by frequency
    sorted_errors = sorted(error_pairs.items(), key=lambda x: x[1], reverse=True)

    print("Most common misclassifications:")
    for (true, pred), count in sorted_errors[:10]:
        print(f"  {true} → {pred}: {count} times")

    print("=" * 70)


def suggest_improvements(history, y_true, y_pred):
    """
    Analyzes training behavior and error patterns to suggest next steps.

    Checks for:
      - Overfitting: test loss rising while train loss falls
      - Underfitting: both losses plateau at high values
      - Class imbalance: certain digits perform much worse than others
    """
    print("\n" + "=" * 70)
    print("IMPROVEMENT OPPORTUNITIES")
    print("=" * 70)

    # Check for overfitting
    final_train_loss = history['train_loss'][-1]
    final_test_loss  = history['test_loss'][-1]
    if final_test_loss > final_train_loss * 1.2:
        print("⚠ Overfitting detected:")
        print("  - Test loss is significantly higher than train loss")
        print("  - Consider: early stopping, reduce epochs, or add regularization (Task 4)")

    # Check for underfitting
    final_test_acc = history['test_acc'][-1]
    if final_test_acc < 0.85:
        print("⚠ Underfitting detected:")
        print("  - Test accuracy is below 85%")
        print("  - Consider: increase hidden layer size, train longer, or tune learning rate")

    # Check for class imbalance in errors
    errors_by_digit = {}
    for true, pred in zip(y_true, y_pred):
        if true != pred:
            errors_by_digit[true] = errors_by_digit.get(true, 0) + 1

    if errors_by_digit:
        worst_digit = max(errors_by_digit, key=errors_by_digit.get)
        worst_count = errors_by_digit[worst_digit]
        print(f"⚠ Digit {worst_digit} has the most errors ({worst_count} misclassifications)")
        print("  - Inspect these samples visually to identify patterns")

    print("=" * 70)


# =============================================================================
# MAIN — Full Training and Evaluation Pipeline
# =============================================================================

if __name__ == "__main__":

    # Load prepared data
    print("Loading data...")
    X_train = np.load("data/X_train.npy")
    y_train = np.load("data/y_train.npy")
    X_test  = np.load("data/X_test.npy")
    y_test  = np.load("data/y_test.npy")

    y_train_int = np.argmax(y_train, axis=1)
    y_test_int  = np.argmax(y_test,  axis=1)

    # --- 3.1: Train on full dataset ---
    params, history = train_model(
        X_train, y_train, X_test, y_test,
        epochs=100,
        learning_rate=0.1,
        batch_size=128,
        seed=42,
        verbose=True
    )

    # --- 3.2: Evaluate and visualize ---
    plot_training_curves(history, save_path="data/training_curves.png")

    final_accuracy = evaluate_final_performance(X_test, y_test, params)

    y_pred = predict(X_test, params)

    plot_confusion_matrix(y_test_int, y_pred, save_path="data/confusion_matrix.png")
    plot_per_digit_accuracy(y_test_int, y_pred, save_path="data/per_digit_accuracy.png")

    # --- 3.3: Analyze errors and suggest improvements ---
    visualize_misclassifications(X_test, y_test, params, num_examples=20,
                                  save_path="data/misclassifications.png")
    analyze_errors(y_test_int, y_pred)
    suggest_improvements(history, y_test_int, y_pred)

    # Save trained model for Task 4
    np.savez("data/trained_model.npz",
             W1=params['W1'], b1=params['b1'],
             W2=params['W2'], b2=params['b2'])
    print("\nTrained model saved to data/trained_model.npz")
