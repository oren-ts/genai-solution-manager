import random
import json
import os
from typing import List, Dict, Set

# ==========================================
# 1. Configuration: Templates & Synonyms
# ==========================================

DATA_CONFIG = {
    "shipping": {
        "templates": [
            "Where is my {item}?",
            "When will my {item} arrive?",
            "Can you track my {item}?",
            "My {item} hasn't arrived yet.",
            "What is the status of my {item}?",
            "I'm waiting for my {item}, is it {status}?",
            "Has my {item} been shipped?",
            "Do you know where my {item} is?",
            "Check the delivery status of my {item}.",
            "My {item} is {status}, what should I do?",
        ],
        "synonyms": {
            "item": [
                "package",
                "order",
                "shipment",
                "parcel",
                "delivery",
                "box",
                "purchase",
                "item",
            ],
            "status": ["late", "delayed", "lost", "stuck", "missing"],
        },
    },
    "products": {
        "templates": [
            "Do you use {material} for your products?",
            "Is the {product} available in {color}?",
            "Do you have {product} in stock?",
            "Can I pre-order the {product}?",
            "What sizes do you have for the {product}?",
            "Is the {product} made of {material}?",
            "I'm looking for a {color} {product}.",
            "Show me your {material} {product} collection.",
            "Do you sell {product}?",
            "When will the {product} be back in stock?",
        ],
        "synonyms": {
            "product": [
                "shirt",
                "jeans",
                "jacket",
                "shoes",
                "bag",
                "hat",
                "dress",
                "sweater",
            ],
            "color": ["blue", "red", "black", "white", "green", "yellow"],
            "material": ["cotton", "leather", "denim", "wool", "silk", "polyester"],
        },
    },
    "returns": {
        "templates": [
            "I want to return my {item}.",
            "How do I exchange a {item}?",
            "Can I get a refund for this {item}?",
            "What is your return policy for {item}?",
            "I received the wrong {item}, can I return it?",
            "My {item} is damaged, I need a refund.",
            "Is it possible to send back my {item}?",
            "Do you offer free returns on {item}?",
            "The {item} doesn't fit, how do I return it?",
            "I changed my mind about the {item}.",
        ],
        "synonyms": {
            "item": [
                "order",
                "purchase",
                "product",
                "item",
                "package",
                "shirt",
                "shoes",
                "jacket",
            ]
        },
    },
}

# ==========================================
# 2. Generation Logic (Balanced)
# ==========================================


def generate_sentence(template: str, synonyms: Dict[str, List[str]]) -> str:
    """Fills a template with random synonyms."""
    for key, values in synonyms.items():
        placeholder = "{" + key + "}"
        if placeholder in template:
            replacement = random.choice(values)
            template = template.replace(placeholder, replacement)
    return template


def generate_dataset(target_total: int = 150) -> List[Dict[str, str]]:
    """Generates a balanced dataset of unique dialogs."""
    dataset = []
    unique_sentences: Set[str] = set()

    categories = list(DATA_CONFIG.keys())
    target_per_category = target_total // len(categories)

    print(
        f"Generating data... Target: {target_total} total ({target_per_category} per category)"
    )

    for category in categories:
        config = DATA_CONFIG[category]
        templates = config["templates"]
        synonyms = config["synonyms"]

        count = 0
        attempts = 0
        max_attempts = target_per_category * 50  # Prevent infinite loops

        while count < target_per_category and attempts < max_attempts:
            attempts += 1

            # 1. Pick Random Template
            template = random.choice(templates)

            # 2. Fill Template
            try:
                sentence = generate_sentence(template, synonyms)
            except Exception as e:
                print(f"Error generating sentence for {category}: {e}")
                continue

            # 3. Check Uniqueness
            if sentence not in unique_sentences:
                unique_sentences.add(sentence)
                dataset.append({"text": sentence, "label": category})
                count += 1

        print(f"  - {category.capitalize()}: Generated {count} unique dialogs.")

    random.shuffle(dataset)
    return dataset


# ==========================================
# 3. Main Execution
# ==========================================


def save_dataset(data: List[Dict], filename: str = "dataset.json"):
    with open(filename, "w") as f:
        json.dump(data, f, indent=2)
    print(f"Dataset saved to {filename} with {len(data)} records.")


if __name__ == "__main__":
    # Generate ~150 examples (50 per class) to be safe above 100
    data = generate_dataset(150)
    save_dataset(data)
