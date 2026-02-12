import json
import numpy as np
from sklearn.model_selection import train_test_split
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.linear_model import LogisticRegression
from sklearn.metrics import classification_report, confusion_matrix, accuracy_score
from typing import List, Dict, Tuple

# ==========================================
# 1. Load Dataset
# ==========================================


def load_dataset(filename: str = "dataset.json") -> Tuple[List[str], List[str]]:
    """Load texts and labels from JSON dataset."""
    with open(filename, "r") as f:
        data = json.load(f)

    texts = [entry["text"] for entry in data]
    labels = [entry["label"] for entry in data]

    print(f"Loaded {len(texts)} samples")
    print(f"Label distribution: {set(labels)}")
    return texts, labels


# ==========================================
# 2. Train-Test Split
# ==========================================


def prepare_data(
    texts: List[str], labels: List[str], test_size: float = 0.2, random_state: int = 42
):
    """Split data with stratification to maintain class balance."""
    X_train, X_test, y_train, y_test = train_test_split(
        texts,
        labels,
        test_size=test_size,
        random_state=random_state,
        stratify=labels,  # Maintains class balance in both sets
    )

    print(f"\nTrain set: {len(X_train)} samples")
    print(f"Test set: {len(X_test)} samples")

    return X_train, X_test, y_train, y_test


# ==========================================
# 3. Model Training Function
# ==========================================


def train_model(
    X_train,
    y_train,
    X_test,
    y_test,
    config_name: str,
    ngram_range: Tuple[int, int],
    C: float,
):
    """Train TF-IDF + Logistic Regression with given hyperparameters."""

    print(f"\n{'='*60}")
    print(f"🔬 Training: {config_name}")
    print(f"   Hyperparameters: ngram_range={ngram_range}, C={C}")
    print(f"{'='*60}")

    # 1. Vectorization
    vectorizer = TfidfVectorizer(ngram_range=ngram_range)
    X_train_vec = vectorizer.fit_transform(X_train)
    X_test_vec = vectorizer.transform(X_test)

    print(f"Feature dimensions: {X_train_vec.shape[1]} features")

    # 2. Training
    model = LogisticRegression(C=C, max_iter=1000, random_state=42)
    model.fit(X_train_vec, y_train)

    # 3. Evaluation
    train_pred = model.predict(X_train_vec)
    test_pred = model.predict(X_test_vec)

    train_acc = accuracy_score(y_train, train_pred)
    test_acc = accuracy_score(y_test, test_pred)

    print(f"\n📊 Results:")
    print(f"   Train Accuracy: {train_acc:.3f}")
    print(f"   Test Accuracy:  {test_acc:.3f}")
    print(f"   Overfitting Gap: {(train_acc - test_acc):.3f}")

    if train_acc - test_acc > 0.15:
        print("   ⚠️  WARNING: Possible overfitting detected (gap > 0.15)")
    elif train_acc - test_acc < 0.05:
        print("   ✅ Good generalization (gap < 0.05)")
    else:
        print("   ✅ Acceptable generalization")

    # 4. Detailed Classification Report
    print(f"\n📋 Classification Report:")
    print(classification_report(y_test, test_pred, digits=3))

    # 5. Confusion Matrix
    print(f"🔢 Confusion Matrix:")
    cm = confusion_matrix(y_test, test_pred, labels=sorted(set(y_test)))
    print(f"   Labels: {sorted(set(y_test))}")
    print(cm)

    return {
        "config_name": config_name,
        "train_acc": train_acc,
        "test_acc": test_acc,
        "vectorizer": vectorizer,
        "model": model,
    }


# ==========================================
# 4. Main Execution
# ==========================================

if __name__ == "__main__":
    # Load data
    texts, labels = load_dataset()
    X_train, X_test, y_train, y_test = prepare_data(texts, labels)

    # Experiment 1: Unigrams only, standard regularization
    result1 = train_model(
        X_train,
        y_train,
        X_test,
        y_test,
        config_name="Config 1: Unigrams + C=1.0",
        ngram_range=(1, 1),
        C=1.0,
    )

    # Experiment 2: Unigrams + Bigrams, stronger regularization
    result2 = train_model(
        X_train,
        y_train,
        X_test,
        y_test,
        config_name="Config 2: Unigrams+Bigrams + C=0.1",
        ngram_range=(1, 2),
        C=0.1,
    )

    # Summary Comparison
    print(f"\n{'='*60}")
    print("📊 FINAL COMPARISON")
    print(f"{'='*60}")
    print(f"{result1['config_name']:40} Test Acc: {result1['test_acc']:.3f}")
    print(f"{result2['config_name']:40} Test Acc: {result2['test_acc']:.3f}")

    if result2["test_acc"] > result1["test_acc"]:
        print(f"\n🏆 Winner: Config 2 (Bigrams help capture phrase patterns)")
    elif result1["test_acc"] > result2["test_acc"]:
        print(f"\n🏆 Winner: Config 1 (Simpler features generalize better)")
    else:
        print(f"\n🤝 Tie: Both configurations perform equally")

    print(f"\n✅ Baseline model training complete!")
