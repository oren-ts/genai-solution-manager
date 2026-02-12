import json
import numpy as np
import torch
from sklearn.model_selection import train_test_split
from sklearn.metrics import classification_report, confusion_matrix, accuracy_score
from transformers import (
    DistilBertTokenizer,
    DistilBertForSequenceClassification,
    Trainer,
    TrainingArguments,
)
from torch.utils.data import Dataset
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
    return texts, labels


# ==========================================
# 2. Prepare Data
# ==========================================


def prepare_data(texts: List[str], labels: List[str], test_size: float = 0.2):
    """Split and encode labels."""
    # Create label mapping
    unique_labels = sorted(set(labels))
    label2id = {label: idx for idx, label in enumerate(unique_labels)}
    id2label = {idx: label for label, idx in label2id.items()}

    print(f"Label mapping: {label2id}")

    # Encode labels
    encoded_labels = [label2id[label] for label in labels]

    # Split data
    X_train, X_test, y_train, y_test = train_test_split(
        texts,
        encoded_labels,
        test_size=test_size,
        random_state=42,
        stratify=encoded_labels,
    )

    print(f"\nTrain set: {len(X_train)} samples")
    print(f"Test set: {len(X_test)} samples")

    return X_train, X_test, y_train, y_test, label2id, id2label


# ==========================================
# 3. Custom Dataset Class
# ==========================================


class ChatbotDataset(Dataset):
    """PyTorch Dataset for chatbot queries."""

    def __init__(self, texts, labels, tokenizer, max_length=64):
        self.texts = texts
        self.labels = labels
        self.tokenizer = tokenizer
        self.max_length = max_length

    def __len__(self):
        return len(self.texts)

    def __getitem__(self, idx):
        text = self.texts[idx]
        label = self.labels[idx]

        # Tokenize
        encoding = self.tokenizer(
            text,
            truncation=True,
            padding="max_length",
            max_length=self.max_length,
            return_tensors="pt",
        )

        return {
            "input_ids": encoding["input_ids"].flatten(),
            "attention_mask": encoding["attention_mask"].flatten(),
            "labels": torch.tensor(label, dtype=torch.long),
        }


# ==========================================
# 4. Training & Evaluation
# ==========================================


def train_distilbert(X_train, y_train, X_test, y_test, label2id, id2label):
    """Fine-tune DistilBERT on chatbot data."""

    print(f"\n{'='*60}")
    print("🤖 Training: DistilBERT Transfer Learning")
    print(f"{'='*60}")

    # 1. Load tokenizer and model
    model_name = "distilbert-base-uncased"
    tokenizer = DistilBertTokenizer.from_pretrained(model_name)
    model = DistilBertForSequenceClassification.from_pretrained(
        model_name, num_labels=len(label2id), id2label=id2label, label2id=label2id
    )

    print(f"Loaded pre-trained model: {model_name}")
    print(f"Number of classes: {len(label2id)}")

    # 2. Create datasets
    train_dataset = ChatbotDataset(X_train, y_train, tokenizer)
    test_dataset = ChatbotDataset(X_test, y_test, tokenizer)

    # 3. Training arguments
    training_args = TrainingArguments(
        output_dir="./results",
        num_train_epochs=3,
        per_device_train_batch_size=8,
        per_device_eval_batch_size=8,
        warmup_steps=10,
        weight_decay=0.01,
        logging_dir="./logs",
        logging_steps=10,
        eval_strategy="epoch",
        save_strategy="epoch",
        load_best_model_at_end=True,
    )

    # 4. Create Trainer
    trainer = Trainer(
        model=model,
        args=training_args,
        train_dataset=train_dataset,
        eval_dataset=test_dataset,
    )

    # 5. Train
    print("\n🚀 Starting fine-tuning...")
    trainer.train()

    # 6. Evaluate on test set
    print(f"\n{'='*60}")
    print("📊 Evaluation Results")
    print(f"{'='*60}")

    # Get predictions
    predictions = trainer.predict(test_dataset)
    pred_labels = np.argmax(predictions.predictions, axis=1)
    true_labels = y_test

    # Calculate accuracy
    test_acc = accuracy_score(true_labels, pred_labels)
    print(f"\n✅ Test Accuracy: {test_acc:.3f}")

    # Classification report
    print(f"\n📋 Classification Report:")
    target_names = [id2label[i] for i in sorted(id2label.keys())]
    print(
        classification_report(
            true_labels, pred_labels, target_names=target_names, digits=3
        )
    )

    # Confusion matrix
    print(f"\n🔢 Confusion Matrix:")
    cm = confusion_matrix(true_labels, pred_labels)
    print(f"   Labels: {target_names}")
    print(cm)

    return test_acc


# ==========================================
# 5. Comparison with Baseline
# ==========================================


def compare_with_baseline(transfer_acc: float, baseline_acc: float = 1.0):
    """Compare transfer learning with baseline results."""

    print(f"\n{'='*60}")
    print("🏆 FINAL COMPARISON: Transfer Learning vs Baseline")
    print(f"{'='*60}")
    print(f"Baseline (TF-IDF + Logistic Regression): {baseline_acc:.3f}")
    print(f"Transfer Learning (DistilBERT):          {transfer_acc:.3f}")

    diff = transfer_acc - baseline_acc

    if abs(diff) < 0.01:
        print(f"\n🤝 Both models perform equally well!")
        print(f"   → The task is well-suited for both approaches")
    elif transfer_acc > baseline_acc:
        print(f"\n🏆 Transfer Learning WINS by {diff:.3f}!")
        print(f"   → Pre-trained knowledge helps with this task")
    else:
        print(f"\n🏆 Baseline WINS by {abs(diff):.3f}!")
        print(f"   → Simple features are sufficient for this task")

    print(f"\n💡 Key Insight:")
    if baseline_acc >= 0.95 and transfer_acc >= 0.95:
        print(f"   Both models achieve excellent accuracy (>95%).")
        print(f"   This indicates:")
        print(f"   • High-quality, well-separated training data")
        print(f"   • Clear distinctions between categories")
        print(f"   • Template-based generation created distinctive patterns")


# ==========================================
# 6. Main Execution
# ==========================================

if __name__ == "__main__":
    # Load data
    texts, labels = load_dataset()
    X_train, X_test, y_train, y_test, label2id, id2label = prepare_data(texts, labels)

    # Train DistilBERT
    transfer_acc = train_distilbert(
        X_train, y_train, X_test, y_test, label2id, id2label
    )

    # Compare with baseline
    compare_with_baseline(transfer_acc, baseline_acc=1.0)

    print(f"\n✅ Transfer learning complete!")
