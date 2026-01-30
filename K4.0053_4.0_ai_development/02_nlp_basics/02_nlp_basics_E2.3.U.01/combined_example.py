"""
Combined Stemming vs. Lemmatization Example
Exercise 02.3.Ü.01 - Stemming vs. Lemmatization

This script demonstrates both stemming (NLTK) and lemmatization (spaCy)
side-by-side for direct comparison.

Requirements:
    pip install nltk spacy
    python -m spacy download en_core_web_sm
"""

from nltk.stem import PorterStemmer
import spacy


def compare_techniques():
    """
    Compare stemming and lemmatization on the same word set.
    
    Highlights key differences:
    - Regular forms: Both handle well
    - Irregular verbs: Only lemmatization normalizes correctly
    - Irregular plurals: Only lemmatization normalizes correctly
    - Comparatives/superlatives: Only lemmatization captures meaning
    """
    # Fictitious (self-created) word set using real English words
    words = ["running", "ran", "runs", "better", "best", "mice", "cats"]
    
    print("=" * 70)
    print("STEMMING vs. LEMMATIZATION: Direct Comparison")
    print("=" * 70)
    print()
    
    # === STEMMING (NLTK) ===
    print("1. STEMMING (NLTK PorterStemmer)")
    print("-" * 70)
    
    stemmer = PorterStemmer()
    
    print("Original     | Stem")
    print("-" * 26)
    
    stems = {}
    for word in words:
        stem = stemmer.stem(word)
        stems[word] = stem
        print(f"{word:12} | {stem}")
    
    print()
    print()
    
    # === LEMMATIZATION (spaCy) ===
    print("2. LEMMATIZATION (spaCy)")
    print("-" * 70)
    
    # Provide sentence context for accurate POS tagging
    text = "I run, I runs, I ran, and I am running. These are better and best examples. I see mice and cats."
    
    nlp = spacy.load("en_core_web_sm")
    doc = nlp(text)
    
    print("Original     | Lemma    | POS")
    print("-" * 45)
    
    lemmas = {}
    targets = set(words)
    for token in doc:
        if token.text.lower() in targets:
            lemmas[token.text] = (token.lemma_, token.pos_)
            print(f"{token.text:12} | {token.lemma_:8} | {token.pos_}")
    
    print()
    print()
    
    # === COMPARISON ===
    print("3. SIDE-BY-SIDE COMPARISON")
    print("-" * 70)
    print("Word         | Stem (NLTK) | Lemma (spaCy) | Winner")
    print("-" * 70)
    
    # Sort by word order in original list for consistency
    for word in words:
        stem = stems.get(word, "N/A")
        lemma_info = lemmas.get(word, ("N/A", "N/A"))
        lemma = lemma_info[0]
        
        # Determine "winner" based on linguistic correctness
        winner = determine_winner(word, stem, lemma)
        
        print(f"{word:12} | {stem:11} | {lemma:13} | {winner}")
    
    print()
    print()
    
    # === KEY INSIGHTS ===
    print("4. KEY INSIGHTS")
    print("=" * 70)
    print()
    print("🔹 Proof Point 1: Irregular Verb (ran)")
    print("   Stemming:      ran → ran          ❌ Not normalized")
    print("   Lemmatization: ran → run (VERB)   ✅ Correctly unified")
    print()
    print("🔹 Proof Point 2: Irregular Plural (mice)")
    print("   Stemming:      mice → mice        ❌ Not normalized")
    print("   Lemmatization: mice → mouse       ✅ Correctly unified")
    print()
    print("🔹 Proof Point 3: Superlative (best)")
    print("   Stemming:      best → best        ❌ Not normalized")
    print("   Lemmatization: best → good        ✅ Semantic base captured")
    print()
    print("=" * 70)
    print("CONCLUSION:")
    print("=" * 70)
    print("Stemming: Fast, simple, but fails on irregular/semantic patterns")
    print("Lemmatization: Accurate, meaning-aware, but slower")
    print()
    print("Choose stemming for speed at scale.")
    print("Choose lemmatization for accuracy and semantic understanding.")
    print("=" * 70)


def determine_winner(word, stem, lemma):
    """
    Determine which technique produces a better normalization.
    
    "Better" means:
    - Produces a real dictionary word
    - Captures the correct base meaning
    - Unifies related forms appropriately
    """
    # Cases where lemmatization clearly wins
    if word in ["ran", "mice", "best"]:
        if stem == word and lemma != word:
            return "Lemma ✅"
        elif stem != word and lemma == word:
            return "Stem ✅"
        else:
            return "Both ≈"
    
    # Cases where both perform similarly
    if word in ["running", "runs", "cats"]:
        if stem == lemma:
            return "Both ✅"
        else:
            return "Stem ≈ Lemma"
    
    # Edge case: better (linguistic complexity)
    if word == "better":
        return "Lemma ✅*"  # * = linguistic nuance
    
    return "Both ≈"


if __name__ == "__main__":
    compare_techniques()
