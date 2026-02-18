# Handwritten Digit Recognizer
  
**Stack:** Python · NumPy · PIL (Pillow) · Matplotlib  
**Dataset:** MNIST (70,000 handwritten digits, 28×28 px grayscale)  
**Goal:** Build a digit-recognizing neural network from scratch —> no ML frameworks.

---

## Project Overview

This project implements a fully manual neural network for classifying handwritten digits (0–9) from the MNIST dataset. Every component: data loading, normalization, forward pass, backpropagation, and weight updates — is written explicitly using only Python and NumPy. No PyTorch, TensorFlow, or sklearn.

The network architecture uses a single hidden layer with sigmoid activations throughout, trained with gradient descent and binary cross-entropy loss.

---

## Repository Structure

```
handwritten-digit-recognizer/
├── README.md
├── .gitignore
├── notebooks/
│   └── full_walkthrough.ipynb     ← complete project walkthrough
├── src/
│   ├── task1_data_prep.py         ← data loading, normalization, array prep
│   ├── task2_neural_network.py    ← network architecture, forward pass, backprop
│   ├── task3_training.py          ← full training loop, evaluation
│   ├── task4_optimization.py      ← hyperparameter tuning, overfitting checks
│   └── task5_reflection.py        ← results summary, reflection
└── data/                          ← gitignored — download locally via task1_data_prep.py
```

---

## Task Package 1 — Data Preparation and Understanding

### What was done

- Explored core NumPy operations: array creation, reshaping, broadcasting, normalization
- Explored core PIL operations: creating images from arrays, pixel inspection, image compositing
- Downloaded MNIST in raw IDX binary format using `urllib` and parsed it manually with `struct`
- Normalized pixel values from `uint8 [0, 255]` to `float32 [0.0, 1.0]`
- Flattened 2D images `(28, 28)` → 1D vectors `(784,)` for network input
- One-hot encoded integer labels `[0–9]` → binary vectors `(10,)` for loss computation
- Verified final shapes: `X_train (60000, 784)`, `y_train (60000, 10)`, `X_test (10000, 784)`, `y_test (10000, 10)`
- Saved prepared arrays as `.npy` files for use in subsequent task packages

### Key decisions

| Decision | Rationale |
|---|---|
| Parse IDX binary manually | No ML libraries allowed — uses `struct` + `np.frombuffer` |
| Normalize to [0, 1] | Keeps sigmoid inputs in the responsive region of the activation function |
| One-hot encode labels | Required to compute per-class gradients in backpropagation |
| Save as `.npy` | Fast binary format — loads in milliseconds; kept out of git via `.gitignore` |

---

## Task Package 2 — Neural Network Design and Implementation

### What was done

- Implemented the sigmoid activation function and its derivative from scratch using NumPy
- Designed a three-layer architecture: 784 → 128 → 10 (input → hidden → output)
- Initialized weights with small random values (×0.01) to break symmetry; biases initialized to zero
- Chose binary cross-entropy as the loss function — pairs cleanly with sigmoid outputs
- Set learning rate to 0.1 — standard starting point for sigmoid networks
- Coded the forward pass manually: weighted sums + sigmoid activations, with intermediate values cached for backprop
- Implemented backpropagation from scratch using the chain rule across both layers
- Verified the full training loop: forward pass → loss → gradients → weight update → loss decreases

### Key decisions

| Decision | Rationale |
|---|---|
| Hidden size: 128 neurons | Large enough to learn digit features; small enough to train on CPU |
| Weights ×0.01 | Keeps initial sigmoid inputs near zero where gradient is steepest |
| Cross-entropy loss | Gradient simplifies to (ŷ - y) with sigmoid — avoids vanishing gradients |
| Learning rate 0.1 | Standard starting point; tuned in Task Package 4 |

---

## Task Package 3 — Training and Model Evaluation

### What was done

- Implemented mini-batch gradient descent (batch_size=128) to solve vanishing gradient problem from full-batch training
- Trained on 60,000 MNIST samples for 100 epochs with learning rate 0.1
- Achieved **97.55% test accuracy** (9,755 / 10,000 correct predictions)
- Generated training curves showing smooth loss decrease and accuracy increase
- Created confusion matrix identifying most common error patterns: 4↔9, 5→3, 7→2
- Analyzed per-digit accuracy — digit 9 has lowest accuracy at 95.9% (41 errors)
- Visualized 20 misclassified samples to understand failure modes
- Identified slight overfitting (test loss 0.017 vs train loss 0.012)

### Key decisions

| Decision | Rationale |
|---|---|
| Mini-batch size: 128 | Balances gradient noise (helps escape local minima) with computational efficiency |
| Shuffle each epoch | Prevents the network from memorizing batch order; improves generalization |
| 100 epochs | Loss plateaus around epoch 60; running to 100 ensures convergence |
| Evaluate on full sets | Per-epoch evaluation on 60K train + 10K test gives accurate loss/accuracy tracking |

### Results

- **Final test accuracy:** 97.55%
- **Training time:** ~3 minutes on CPU (100 epochs × 468 batches)
- **Most confused pairs:** 4↔9 (13 errors each direction), 5→3 (12 errors), 7→2 (11 errors)
- **Best performing digit:** 0 (99.0% accuracy)
- **Worst performing digit:** 9 (95.9% accuracy)

---

## Tech Stack

| Tool | Version | Purpose |
|---|---|---|
| Python | 3.x | Core language |
| NumPy | latest | Array math, matrix operations |
| PIL / Pillow | latest | Image loading and visualization |
| Matplotlib | latest | Training curves, result plots |

---

## How to Run

```bash
# 1. Install dependencies
pip install numpy pillow matplotlib

# 2. Run data preparation (downloads MNIST automatically)
python src/task1_data_prep.py

# 3. Open the full walkthrough notebook
pip install notebook
jupyter notebook notebooks/full_walkthrough.ipynb
```

---

## Author

Oren · velpTEC K4.0059 · 2025
