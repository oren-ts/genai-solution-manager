import json
import re
from collections import Counter
from typing import List, Dict, Any


def load_dataset(filename: str = "dataset.json") -> List[Dict]:
    try:
        with open(filename, "r") as f:
            return json.load(f)
    except FileNotFoundError:
        print(f"Error: {filename} not found. Please run generate_data.py first.")
        return []


def check_completeness(dataset: List[Dict]) -> Dict[str, Any]:
    """Checks for empty strings or leftover placeholders."""
    issues = []
    for i, entry in enumerate(dataset):
        text = entry.get("text", "")
        if not text.strip():
            issues.append(f"Row {i}: Empty text")
        if "{" in text or "}" in text:
            issues.append(f"Row {i}: Leftover placeholder in '{text}'")

    return {
        "status": "PASS" if not issues else "FAIL",
        "issues_count": len(issues),
        "issues": issues[:5],  # Show top 5
    }


def check_class_balance(dataset: List[Dict]) -> Dict[str, Any]:
    """Checks if categories are balanced."""
    labels = [entry.get("label") for entry in dataset]
    counts = Counter(labels)

    total = len(dataset)
    ideal = total / len(counts) if counts else 0

    # Calculate deviation
    imbalance_flags = []
    for label, count in counts.items():
        if abs(count - ideal) > (ideal * 0.2):  # >20% deviation
            imbalance_flags.append(f"{label}: {count} (Ideal: {ideal:.1f})")

    return {
        "counts": dict(counts),
        "is_balanced": len(imbalance_flags) == 0,
        "warnings": imbalance_flags,
    }


def check_variety(dataset: List[Dict]) -> Dict[str, Any]:
    """Calculates vocabulary richness and duplicate checks."""
    texts = [entry.get("text", "").lower() for entry in dataset]

    # 1. Duplicates
    unique_texts = set(texts)
    duplicates = len(texts) - len(unique_texts)

    # 2. Lexical Diversity (Type-Token Ratio)
    all_tokens = " ".join(texts).split()
    unique_tokens = set(all_tokens)
    ttr = len(unique_tokens) / len(all_tokens) if all_tokens else 0

    return {
        "total_dialogs": len(texts),
        "unique_dialogs": len(unique_texts),
        "duplicates": duplicates,
        "vocabulary_size": len(unique_tokens),
        "lexical_diversity": ttr,
    }


def generate_report():
    print("Loading dataset...")
    data = load_dataset()
    if not data:
        return

    print("\n" + "=" * 40)
    print("📊 DATASET EVALUATION REPORT")
    print("=" * 40)

    # 1. Completeness
    comp = check_completeness(data)
    print(f"\n1. COMPLETENESS CHECK: [{comp['status']}]")
    if comp["status"] == "FAIL":
        print(f"   Found {comp['issues_count']} issues. Examples: {comp['issues']}")
    else:
        print("   All records look complete.")

    # 2. Class Balance
    bal = check_class_balance(data)
    status = "PASS" if bal["is_balanced"] else "WARNING"
    print(f"\n2. CLASS BALANCE CHECK: [{status}]")
    print(f"   Counts: {bal['counts']}")
    if status == "WARNING":
        print(f"   Imbalance detected: {bal['warnings']}")

    # 3. Variety
    var = check_variety(data)
    print(f"\n3. VARIETY CHECK")
    print(f"   Unique Dialogs: {var['unique_dialogs']} / {var['total_dialogs']}")
    if var["duplicates"] == 0:
        print("   [PASS] No duplicates found.")
    else:
        print(f"   [FAIL] Found {var['duplicates']} duplicates!")

    print(f"   Vocabulary Size: {var['vocabulary_size']} words")
    print(f"   Lexical Diversity: {var['lexical_diversity']:.2f}")
    if var["lexical_diversity"] > 0.1:
        print("   [PASS] Good lexical diversity (> 0.1)")
    else:
        print("   [WARNING] Low lexical diversity. Templates might be too repetitive.")

    print("\n" + "=" * 40)


if __name__ == "__main__":
    generate_report()
