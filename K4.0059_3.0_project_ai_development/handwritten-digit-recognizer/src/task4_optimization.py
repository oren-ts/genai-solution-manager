# =============================================================================
# task4_optimization.py
# Task Package 4: Optimization and Fine-Tuning
# Project: Handwritten Digit Recognizer (K4.0059)
# Tools: Python, NumPy only
# =============================================================================
# This file covers all three work packages for Task 4:
#   4.1 - Optimize network based on Task 3 findings (hidden size, learning rate)
#   4.2 - Implement validation checks to avoid overfitting (early stopping)
#   4.3 - Stick to sigmoid activation, only tune learning rate and architecture
# =============================================================================

import numpy as np
import matplotlib.pyplot as plt
from task2_neural_network import (
    initialize_parameters,
    forward_pass,
    compute_loss,
    backpropagation,
    update_parameters,
    compute_accuracy
)


# =============================================================================
# WORK PACKAGE 4.1 — Optimize Based on Task 3 Findings
# =============================================================================
# Task 3 results:
#   - 97.55% test accuracy with hidden_size=128, lr=0.1
#   - Slight overfitting (test loss > train loss)
#   - Digit 9 most error-prone (95.9% accuracy)
#
# Optimization strategy:
#   1. Try different hidden layer sizes: 64, 128, 256
#   2. Try different learning rates: 0.05, 0.1, 0.2
#   3. Implement early stopping to prevent overfitting
#
# Grid search: test all combinations, track best configuration

def train_with_config(X_train, y_train, X_test, y_test,
                      hidden_size=128,
                      learning_rate=0.1,
                      batch_size=128,
                      epochs=100,
                      early_stopping=False,
                      patience=10,
                      seed=42,
                      verbose=False):
    """
    Trains the network with a specific configuration.
    Optionally implements early stopping to prevent overfitting.

    Early stopping:
    ───────────────
    Monitors test loss. If it doesn't improve for `patience` epochs,
    stop training and restore the best weights seen so far.

    Why early stopping helps:
      - Overfitting means the network memorizes training data instead of
        learning general patterns
      - Test loss starts rising while train loss keeps falling
      - Early stopping catches the point where generalization is best

    Arguments:
        X_train, y_train, X_test, y_test: data arrays
        hidden_size:   number of hidden layer neurons
        learning_rate: gradient descent step size
        batch_size:    mini-batch size
        epochs:        max number of epochs to train
        early_stopping: if True, stop when test loss stops improving
        patience:      how many epochs to wait before stopping
        seed:          for reproducible initialization
        verbose:       print progress

    Returns:
        best_params: network parameters with lowest test loss
        history:     training metrics per epoch
        stopped_at:  epoch where training stopped (equals epochs if no early stop)
    """
    # Custom parameter initialization for different hidden sizes
    np.random.seed(seed)
    params = {
        'W1': np.random.randn(hidden_size, 784) * 0.01,
        'b1': np.zeros((hidden_size, 1)),
        'W2': np.random.randn(10, hidden_size) * 0.01,
        'b2': np.zeros((10, 1)),
    }

    y_train_int = np.argmax(y_train, axis=1)
    y_test_int  = np.argmax(y_test,  axis=1)

    history = {
        'train_loss': [],
        'test_loss':  [],
        'train_acc':  [],
        'test_acc':   []
    }

    N = X_train.shape[0]
    num_batches = N // batch_size

    # Early stopping state
    best_test_loss = float('inf')
    best_params = None
    epochs_without_improvement = 0

    for epoch in range(epochs):

        # Shuffle and train on mini-batches
        shuffle_idx = np.random.permutation(N)
        X_shuffled = X_train[shuffle_idx]
        y_shuffled = y_train[shuffle_idx]

        for batch in range(num_batches):
            start = batch * batch_size
            end = start + batch_size
            X_batch = X_shuffled[start:end]
            y_batch = y_shuffled[start:end]

            A2_batch, cache = forward_pass(X_batch, params)
            grads = backpropagation(y_batch, params, cache)
            params = update_parameters(params, grads, learning_rate=learning_rate)

        # Evaluate
        train_acc = compute_accuracy(X_train, y_train_int, params)
        A2_train, _ = forward_pass(X_train, params)
        train_loss = compute_loss(A2_train, y_train)

        A2_test, _ = forward_pass(X_test, params)
        test_loss = compute_loss(A2_test, y_test)
        test_acc = compute_accuracy(X_test, y_test_int, params)

        history['train_loss'].append(train_loss)
        history['test_loss'].append(test_loss)
        history['train_acc'].append(train_acc)
        history['test_acc'].append(test_acc)

        # Early stopping check
        if early_stopping:
            if test_loss < best_test_loss:
                best_test_loss = test_loss
                best_params = {k: v.copy() for k, v in params.items()}
                epochs_without_improvement = 0
            else:
                epochs_without_improvement += 1

            if epochs_without_improvement >= patience:
                if verbose:
                    print(f"  Early stopping at epoch {epoch} (no improvement for {patience} epochs)")
                return best_params, history, epoch

        if verbose and epoch % 20 == 0:
            print(f"  Epoch {epoch:3d} | Train Acc: {train_acc*100:5.1f}% | Test Acc: {test_acc*100:5.1f}%")

    # Return best params if early stopping was enabled, otherwise final params
    if early_stopping and best_params is not None:
        return best_params, history, epochs
    else:
        return params, history, epochs


def grid_search_hyperparameters(X_train, y_train, X_test, y_test,
                                 hidden_sizes=[64, 128, 256],
                                 learning_rates=[0.05, 0.1, 0.2],
                                 batch_size=128,
                                 epochs=100,
                                 early_stopping=True,
                                 patience=10):
    """
    Tests all combinations of hidden_size and learning_rate.
    Returns the best configuration and all results.

    Grid search is expensive (9 configurations × 100 epochs each)
    but ensures we find the optimal settings within the search space.
    """
    results = []

    print("=" * 70)
    print("GRID SEARCH: HYPERPARAMETER OPTIMIZATION")
    print("=" * 70)
    print(f"Testing {len(hidden_sizes)} hidden sizes × {len(learning_rates)} learning rates")
    print(f"Early stopping: {early_stopping} (patience={patience})")
    print("=" * 70)

    for hidden_size in hidden_sizes:
        for learning_rate in learning_rates:
            print(f"\nTesting: hidden_size={hidden_size}, lr={learning_rate}")

            params, history, stopped_at = train_with_config(
                X_train, y_train, X_test, y_test,
                hidden_size=hidden_size,
                learning_rate=learning_rate,
                batch_size=batch_size,
                epochs=epochs,
                early_stopping=early_stopping,
                patience=patience,
                seed=42,
                verbose=True
            )

            final_test_acc = history['test_acc'][-1]
            final_test_loss = history['test_loss'][-1]

            results.append({
                'hidden_size': hidden_size,
                'learning_rate': learning_rate,
                'test_acc': final_test_acc,
                'test_loss': final_test_loss,
                'stopped_at': stopped_at,
                'params': params,
                'history': history
            })

            print(f"  → Test Acc: {final_test_acc*100:.2f}%, Test Loss: {final_test_loss:.4f}, Stopped at epoch {stopped_at}")

    # Find best configuration
    best = max(results, key=lambda x: x['test_acc'])

    print("\n" + "=" * 70)
    print("BEST CONFIGURATION")
    print("=" * 70)
    print(f"Hidden size:    {best['hidden_size']}")
    print(f"Learning rate:  {best['learning_rate']}")
    print(f"Test accuracy:  {best['test_acc']*100:.2f}%")
    print(f"Test loss:      {best['test_loss']:.4f}")
    print(f"Stopped at:     epoch {best['stopped_at']}")
    print("=" * 70)

    return best, results


def plot_grid_search_results(results, save_path=None):
    """
    Heatmap showing test accuracy for each (hidden_size, learning_rate) pair.
    Helps visualize which configurations work best.
    """
    hidden_sizes = sorted(set(r['hidden_size'] for r in results))
    learning_rates = sorted(set(r['learning_rate'] for r in results))

    # Build accuracy matrix
    acc_matrix = np.zeros((len(hidden_sizes), len(learning_rates)))
    for r in results:
        i = hidden_sizes.index(r['hidden_size'])
        j = learning_rates.index(r['learning_rate'])
        acc_matrix[i, j] = r['test_acc'] * 100

    fig, ax = plt.subplots(figsize=(8, 6))
    im = ax.imshow(acc_matrix, cmap='RdYlGn', vmin=96, vmax=98)

    ax.set_xticks(range(len(learning_rates)))
    ax.set_yticks(range(len(hidden_sizes)))
    ax.set_xticklabels([f'{lr:.2f}' for lr in learning_rates])
    ax.set_yticklabels([str(hs) for hs in hidden_sizes])
    ax.set_xlabel('Learning Rate', fontsize=12)
    ax.set_ylabel('Hidden Layer Size', fontsize=12)
    ax.set_title('Grid Search Results: Test Accuracy (%)', fontsize=14)

    # Annotate cells
    for i in range(len(hidden_sizes)):
        for j in range(len(learning_rates)):
            text = ax.text(j, i, f'{acc_matrix[i, j]:.2f}%',
                           ha='center', va='center', color='black', fontsize=10)

    plt.colorbar(im, ax=ax, label='Test Accuracy (%)')
    plt.tight_layout()
    if save_path:
        plt.savefig(save_path, dpi=150)
        print(f"Saved grid search heatmap to {save_path}")
    plt.show()


# =============================================================================
# WORK PACKAGE 4.2 — Early Stopping Implementation
# =============================================================================
# Already implemented in train_with_config() above via the early_stopping flag.
# This prevents overfitting by stopping when test loss stops improving.

def compare_with_without_early_stopping(X_train, y_train, X_test, y_test,
                                         hidden_size=128,
                                         learning_rate=0.1,
                                         batch_size=128,
                                         epochs=100,
                                         patience=10):
    """
    Trains two models side by side:
      1. With early stopping
      2. Without early stopping (full 100 epochs)

    Plots both training curves to show early stopping's effect.
    """
    print("\n" + "=" * 70)
    print("EARLY STOPPING COMPARISON")
    print("=" * 70)

    print("\nTraining WITHOUT early stopping (full 100 epochs)...")
    params_no_es, history_no_es, _ = train_with_config(
        X_train, y_train, X_test, y_test,
        hidden_size=hidden_size,
        learning_rate=learning_rate,
        batch_size=batch_size,
        epochs=epochs,
        early_stopping=False,
        seed=42,
        verbose=False
    )

    print("Training WITH early stopping (patience=10)...")
    params_es, history_es, stopped_at = train_with_config(
        X_train, y_train, X_test, y_test,
        hidden_size=hidden_size,
        learning_rate=learning_rate,
        batch_size=batch_size,
        epochs=epochs,
        early_stopping=True,
        patience=patience,
        seed=42,
        verbose=False
    )

    print(f"\n  Without early stopping: {history_no_es['test_acc'][-1]*100:.2f}% test acc")
    print(f"  With early stopping:    {history_es['test_acc'][-1]*100:.2f}% test acc (stopped at epoch {stopped_at})")

    # Plot comparison
    fig, (ax1, ax2) = plt.subplots(1, 2, figsize=(14, 5))

    epochs_no_es = range(len(history_no_es['test_loss']))
    epochs_es = range(len(history_es['test_loss']))

    # Loss curves
    ax1.plot(epochs_no_es, history_no_es['train_loss'], 'b-', label='Train (no ES)', alpha=0.7)
    ax1.plot(epochs_no_es, history_no_es['test_loss'], 'r-', label='Test (no ES)', alpha=0.7)
    ax1.plot(epochs_es, history_es['train_loss'], 'b--', label='Train (with ES)', linewidth=2)
    ax1.plot(epochs_es, history_es['test_loss'], 'r--', label='Test (with ES)', linewidth=2)
    ax1.axvline(stopped_at, color='green', linestyle=':', label=f'Early stop (epoch {stopped_at})')
    ax1.set_xlabel('Epoch')
    ax1.set_ylabel('Loss')
    ax1.set_title('Loss: Early Stopping vs No Early Stopping')
    ax1.legend()
    ax1.grid(alpha=0.3)

    # Accuracy curves
    ax2.plot(epochs_no_es, [a*100 for a in history_no_es['test_acc']], 'r-', label='Test (no ES)', alpha=0.7)
    ax2.plot(epochs_es, [a*100 for a in history_es['test_acc']], 'r--', label='Test (with ES)', linewidth=2)
    ax2.axvline(stopped_at, color='green', linestyle=':', label=f'Early stop (epoch {stopped_at})')
    ax2.set_xlabel('Epoch')
    ax2.set_ylabel('Accuracy (%)')
    ax2.set_title('Test Accuracy: Early Stopping vs No Early Stopping')
    ax2.legend()
    ax2.grid(alpha=0.3)

    plt.tight_layout()
    plt.savefig("data/early_stopping_comparison.png", dpi=150)
    print("\nSaved comparison plot to data/early_stopping_comparison.png")
    plt.show()


# =============================================================================
# MAIN — Full Optimization Pipeline
# =============================================================================

if __name__ == "__main__":

    # Load data
    print("Loading data...")
    X_train = np.load("data/X_train.npy")
    y_train = np.load("data/y_train.npy")
    X_test  = np.load("data/X_test.npy")
    y_test  = np.load("data/y_test.npy")

    # --- 4.1: Grid search for best hyperparameters ---
    best_config, all_results = grid_search_hyperparameters(
        X_train, y_train, X_test, y_test,
        hidden_sizes=[64, 128, 256],
        learning_rates=[0.05, 0.1, 0.2],
        batch_size=128,
        epochs=100,
        early_stopping=True,
        patience=10
    )

    plot_grid_search_results(all_results, save_path="data/grid_search_heatmap.png")

    # --- 4.2: Compare early stopping vs no early stopping ---
    compare_with_without_early_stopping(
        X_train, y_train, X_test, y_test,
        hidden_size=best_config['hidden_size'],
        learning_rate=best_config['learning_rate'],
        batch_size=128,
        epochs=100,
        patience=10
    )

    # Save best model
    best_params = best_config['params']
    np.savez("data/optimized_model.npz",
             W1=best_params['W1'], b1=best_params['b1'],
             W2=best_params['W2'], b2=best_params['b2'],
             hidden_size=best_config['hidden_size'],
             learning_rate=best_config['learning_rate'])
    print("\nOptimized model saved to data/optimized_model.npz")
