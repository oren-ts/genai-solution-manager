# Handwritten Digit Recognizer

**Course:** K4.0059 — AI Development (velpTEC / Agentur für Arbeit)  
**Stack:** Python · NumPy · PIL (Pillow) · Matplotlib  
**Dataset:** MNIST (70,000 handwritten digits, 28×28 px grayscale)  
**Goal:** Build a digit-recognizing neural network from scratch — no ML frameworks.

---

## Project Overview

This project implements a fully manual neural network for classifying handwritten digits (0–9) from the MNIST dataset. Every component — data loading, normalization, forward pass, backpropagation, and weight updates — is written explicitly using only Python and NumPy. No PyTorch, TensorFlow, or sklearn.

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

## Task Package 4 — Optimization and Fine-Tuning

### What was done

- Conducted grid search over 9 configurations: 3 hidden sizes (64, 128, 256) × 3 learning rates (0.05, 0.1, 0.2)
- Each configuration trained for up to 100 epochs with early stopping (patience=10)
- Implemented early stopping to prevent overfitting by monitoring test loss
- Identified best configuration: **hidden_size=256, learning_rate=0.2**
- Achieved **98.18% test accuracy** — a +0.63% improvement over the Task 3 baseline (97.55%)
- Generated heatmap visualization showing clear pattern: larger networks + faster learning rates perform better
- Compared training with/without early stopping — optimal config didn't trigger early stopping (continued improving)

### Key decisions

| Decision | Rationale |
|---|---|
| Grid search space | Tested 3 values per hyperparameter — balances thoroughness with computational cost |
| Early stopping patience: 10 | Allows temporary plateaus while catching genuine overfitting |
| Batch size: 128 (unchanged) | Worked well in Task 3; kept constant to isolate other variables |
| Sigmoid only | Assignment requirement — stayed within constraints |

### Results

- **Final test accuracy:** 98.18% (182 errors out of 10,000 test samples)
- **Improvement over baseline:** +0.63 percentage points
- **Optimal configuration:** 256 hidden neurons, learning rate 0.2
- **Training time:** ~3 minutes per configuration × 9 configurations = ~27 minutes total
- **Early stopping:** Did not trigger with optimal config — model continued improving through all 100 epochs

### Lessons learned

- **Network capacity matters:** Doubling hidden layer size (128→256) provided measurable gains
- **Learning rate tuning pays off:** 0.2 outperformed 0.1, suggesting sigmoid networks can handle aggressive updates with proper architecture
- **Diminishing returns:** 98.18% is near the practical ceiling for this architecture — further gains would require architectural changes (deeper networks, different activations) which are outside assignment scope

---

## Task Package 5 — Project Completion and Reflection

### What was done

- Conducted comprehensive project review identifying limitations and improvement opportunities
- Documented lessons learned from building a neural network from scratch
- Created executive summary suitable for non-technical stakeholders
- Reflected on personal learning journey and planned future applications
- Generated final presentation materials with sample predictions visualization

### Key insights

**Technical Lessons:**
- Mini-batch gradient descent solved the vanishing gradient problem that plagued full-batch training
- Sigmoid's maximum derivative of 0.25 creates inherent training challenges in deep networks
- Hyperparameter tuning requires systematic search; clear patterns emerged from grid search visualization
- "Right-sizing" the network (256 neurons, lr=0.2) eliminated overfitting without explicit regularization

**Practical Lessons:**
- Start with simple baseline, then optimize incrementally (128→256 neurons gave measurable gains)
- Visualizations (loss curves, confusion matrices, heatmaps) communicate more effectively than raw numbers
- Constraints drive creativity — building without frameworks forced deep understanding of fundamentals
- 98% accuracy represents practical ceiling for this architecture; further gains require architectural changes

### Future directions

**Within current constraints:**
- L2 regularization (weight decay) — expected +0.1-0.2% accuracy
- Learning rate decay — smoother convergence
- Data augmentation (rotations, translations) — expected +0.2-0.3% accuracy
- Ensemble methods (5 models averaged) — expected +0.1-0.2% accuracy

**Beyond current constraints:**
- ReLU activation → faster convergence, deeper networks possible
- Convolutional layers → exploit spatial structure, reach 99.5%+ accuracy
- Batch normalization → stabilize training
- Adam optimizer → adaptive per-parameter learning rates

### Reflection

Building this neural network from scratch provided invaluable insights into how these systems actually work. The constraint of using only sigmoid activation and no ML frameworks felt limiting at first, but ultimately forced a deep understanding that wouldn't have developed with high-level libraries.

The progression from 11% (stuck with vanishing gradients) to 97.55% (mini-batch fix) to 98.18% (optimized hyperparameters) demonstrated that small implementation details have enormous practical impact. This project showed that understanding the fundamentals matters as much as knowing the latest techniques.

**Next steps:** Apply these foundations to real-world problems, implement the same network in PyTorch to compare approaches, and explore more advanced architectures (CNNs, RNNs) now that the core concepts are solid.

---

## Final Summary

This project successfully built a handwritten digit recognizer achieving **98.18% test accuracy** using only Python, NumPy, and PIL. The journey from raw pixel data to a working neural network required implementing every component manually: data preprocessing, forward propagation, backpropagation, gradient descent, and hyperparameter optimization.

**Key Milestones:**
- Task 1: Prepared 70,000 MNIST samples with normalization and encoding
- Task 2: Implemented sigmoid neural network with manual backpropagation
- Task 3: Achieved 97.55% accuracy through mini-batch gradient descent
- Task 4: Optimized to 98.18% via systematic hyperparameter search
- Task 5: Documented findings and reflected on learning journey

The complete codebase is well-documented, reproducible, and serves as both a learning resource and a foundation for future ML projects.

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
