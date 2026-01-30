"""
spaCy Lemmatization Example
Exercise 02.3.Ü.01 - Stemming vs. Lemmatization

This script demonstrates lemmatization using spaCy.
Lemmatization reduces words to their dictionary base form (lemma)
using linguistic analysis and part-of-speech tagging.

Key characteristics:
- Always produces real dictionary words
- Handles irregular forms (ran → run, mice → mouse)
- Context-aware via POS tagging
- More accurate but slower than stemming

Requirements:
    pip install spacy
    python -m spacy download en_core_web_sm
"""

import spacy


def demonstrate_lemmatization():
    """
    Demonstrate spaCy lemmatization with a test word set.
    
    The word set includes:
    - Regular verbs (running, runs)
    - Irregular verb (ran)
    - Comparative/superlative adjectives (better, best)
    - Irregular plural (mice)
    - Regular plural (cats)
    
    Minimal sentence context is provided to improve POS tagging accuracy.
    Without context, spaCy may assign incorrect POS tags, leading to
    unexpected lemmas.
    """
    # Fictitious (self-created) word set using real English words
    words = ["running", "ran", "runs", "better", "best", "mice", "cats"]
    
    # Provide minimal sentence context for better POS tagging
    # Without context, words like "ran" may be tagged as NOUN instead of VERB
    text = "I run, I runs, I ran, and I am running. These are better and best examples. I see mice and cats."
    
    # Load spaCy English model
    nlp = spacy.load("en_core_web_sm")
    
    # Process text
    doc = nlp(text)
    
    # Display results
    print("=" * 60)
    print("spaCy Lemmatization (with sentence context)")
    print("=" * 60)
    print()
    print("Original     | Lemma    | POS   | Explanation")
    print("-" * 60)
    
    targets = set(words)
    for token in doc:
        if token.text.lower() in targets:
            explanation = get_explanation(token.text, token.lemma_, token.pos_)
            print(f"{token.text:12} | {token.lemma_:8} | {token.pos_:5} | {explanation}")
    
    print()
    print("=" * 60)
    print("Key Observations:")
    print("=" * 60)
    print("✓ Irregular verb unified: ran → run (VERB)")
    print("✓ Irregular plural unified: mice → mouse (NOUN)")
    print("✓ Superlative normalized: best → good (ADJ)")
    print("✓ All forms are real dictionary words")
    print()
    print("Note: 'better → well' reflects spaCy's linguistic model")
    print("where 'better' is treated as comparative of 'well' (ADV).")
    print("This demonstrates lemmatization's meaning-aware approach.")
    print("=" * 60)


def get_explanation(word, lemma, pos):
    """Provide brief explanation for each lemmatization result."""
    explanations = {
        "running": "Gerund/verb -ing form",
        "runs": "3rd person singular verb",
        "ran": "Irregular past tense → base",
        "better": "Comparative → base (linguistic)",
        "best": "Superlative → base adjective",
        "mice": "Irregular plural → singular",
        "cats": "Regular plural → singular"
    }
    return explanations.get(word, "")


if __name__ == "__main__":
    demonstrate_lemmatization()
