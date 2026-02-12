# Exercise 05.5.A.01 - Training Chatbot Models

## Overview

This exercise demonstrates the complete pipeline for training chatbot models, from synthetic data generation through model evaluation. It compares a simple baseline approach (TF-IDF + Logistic Regression) against transfer learning with pre-trained DistilBERT.

## Project Structure
```
05_training_models_T05.5.A.01/
├── generate_data.py          # Part A: Synthetic data generation
├── evaluate_data.py           # Part B: Data quality evaluation
├── train_baseline.py          # Part C: Baseline model training
├── train_transfer.py          # Part D: Transfer learning
├── dataset.json               # Generated training data (150 samples)
├── README.md                  # This file
└── venv/                      # Virtual environment (not tracked)
```

## Exercise Parts

### Part A: Synthetic Data Generation (`generate_data.py`)

**Goal:** Create 100+ unique customer service dialogs using template-based generation.

**Implementation:**
- Template system with synonym replacement
- Three categories: Products, Shipping, Returns
- 10 templates per category with multi-slot placeholders
- Duplicate detection ensuring uniqueness
- Generated 150 dialogs (50 per category)

**Key Features:**
- Category-based structure prevents synonym leakage
- Balanced class distribution (50-50-50)
- Rich synonym sets (6-8 options per slot)

### Part B: Quality Evaluation (`evaluate_data.py`)

**Goal:** Assess dataset quality across three criteria.

**Evaluation Metrics:**
1. **Completeness:** ✅ PASS
   - No empty strings or leftover placeholders
   
2. **Class Balance:** ✅ PASS
   - Perfect distribution: 50 products, 50 returns, 50 shipping
   
3. **Variety:** ✅ PASS
   - 150/150 unique dialogs (0 duplicates)
   - Vocabulary: 151 unique words
   - Lexical diversity: 0.15 (exceeds 0.1 threshold)

### Part C: Baseline Model (`train_baseline.py`)

**Goal:** Train from scratch using traditional ML approach.

**Architecture:**
- TF-IDF vectorization
- Logistic Regression classifier
- 80/20 train-test split (120/30 samples)

**Experiments:**
| Config | N-grams | Regularization (C) | Features | Test Accuracy |
|--------|---------|-------------------|----------|---------------|
| 1      | (1,1)   | 1.0               | 99       | **100%**      |
| 2      | (1,2)   | 0.1               | 322      | **100%**      |

**Key Findings:**
- Zero overfitting (train-test gap = 0.000)
- Both configurations achieved perfect accuracy
- Simple unigrams sufficient for this task

### Part D: Transfer Learning (`train_transfer.py`)

**Goal:** Fine-tune pre-trained DistilBERT and compare with baseline.

**Architecture:**
- Pre-trained: `distilbert-base-uncased` (268MB)
- Fine-tuning: 3 epochs, batch size 8
- Optimizer: AdamW with warmup

**Training Progress:**
| Epoch | Train Loss | Eval Loss |
|-------|------------|-----------|
| 1     | 1.087      | 0.775     |
| 2     | 0.412      | 0.200     |
| 3     | 0.167      | 0.104     |

**Results:**
- Test Accuracy: **100%**
- Perfect confusion matrix (no misclassifications)
- Training time: ~15 seconds

## Final Comparison

| Approach | Model | Test Accuracy | Training Time | Model Size |
|----------|-------|---------------|---------------|------------|
| Baseline | TF-IDF + LogReg | 100% | <1 second | ~100 features |
| Transfer Learning | DistilBERT | 100% | ~15 seconds | 268MB |

**Conclusion:** Both approaches achieved perfect performance. The baseline model is more practical for this task due to faster training and lower resource requirements. The 100% accuracy indicates high-quality, well-separated training data with distinctive patterns per category.

## Key Learnings

### Data Quality Matters Most
- Template-based generation created clear category distinctions
- Rich vocabulary prevented overfitting
- Balanced classes ensured fair learning

### When to Use Each Approach

**Use Simple Models (TF-IDF) When:**
- Categories are well-separated with distinct keywords
- Training data is clean and structured
- Speed and resource efficiency matter
- Interpretability is important

**Use Transfer Learning (DistilBERT) When:**
- Natural language understanding is crucial
- Data has subtle linguistic patterns
- Categories overlap semantically
- You have sufficient compute resources

### Reality Check
This exercise achieved 100% accuracy because:
- ✅ Template-generated data is clean and consistent
- ✅ Categories have distinctive keywords
- ✅ No noise, typos, or ambiguous queries

Real-world performance would likely be lower due to:
- ❌ Typos and grammatical errors
- ❌ Ambiguous or multi-intent queries
- ❌ Slang and informal language
- ❌ Out-of-vocabulary words

## Requirements
```bash
# Core dependencies
pip install numpy scikit-learn

# For transfer learning (Part D)
pip install torch transformers accelerate
```

## Usage

### 1. Generate Training Data
```bash
python generate_data.py
# Output: dataset.json (150 samples)
```

### 2. Evaluate Data Quality
```bash
python evaluate_data.py
# Output: Quality report to console
```

### 3. Train Baseline Model
```bash
python train_baseline.py
# Output: Two model configurations with metrics
```

### 4. Train Transfer Learning Model
```bash
python train_transfer.py
# Output: Fine-tuned DistilBERT with comparison
```

## Technical Notes

### Virtual Environment Setup
```bash
python3 -m venv venv
source venv/bin/activate  # Mac/Linux
pip install -r requirements.txt
```

### Data Format
```json
[
  {
    "text": "Where is my package?",
    "label": "shipping"
  },
  {
    "text": "Do you have shirts in stock?",
    "label": "products"
  }
]
```

## Future Improvements

1. **Data Augmentation:** Add noise, typos, and variations to make data more realistic
2. **Class Expansion:** Add more categories (cancellations, complaints, feedback)
3. **Active Learning:** Collect real user queries to improve model
4. **Ensemble Methods:** Combine baseline and transfer learning predictions
5. **Error Analysis:** Analyze misclassifications on edge cases

## Author

Oren Tauber-Sharon  
Course: K4.0053_4.0 AI Development  
Date: February 2025
```

---

## Commit Message
```
feat: Complete chatbot training exercise with baseline and transfer learning

- Implement synthetic data generation with template system (150 samples)
- Add quality evaluation metrics (completeness, balance, variety)
- Train TF-IDF baseline achieving 100% test accuracy
- Fine-tune DistilBERT achieving 100% test accuracy
- Compare both approaches with detailed performance analysis

All parts A-D complete with comprehensive documentation.
