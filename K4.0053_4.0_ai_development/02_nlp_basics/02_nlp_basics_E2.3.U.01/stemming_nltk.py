"""
NLTK Stemming Example
Exercise 02.3.Ü.01 - Stemming vs. Lemmatization

This script demonstrates stemming using NLTK's PorterStemmer.
Stemming reduces words to their stems using rule-based suffix removal.

Key characteristics:
- Fast and simple
- May produce non-words
- Fails on irregular forms
- Context-blind
"""

from nltk.stem import PorterStemmer


def demonstrate_stemming():
    """
    Demonstrate NLTK stemming with a test word set.
    
    The word set includes:
    - Regular verbs (running, runs)
    - Irregular verb (ran)
    - Comparative/superlative adjectives (better, best)
    - Irregular plural (mice)
    - Regular plural (cats)
    """
    # Fictitious (self-created) word set using real English words
    words = ["running", "ran", "runs", "better", "best", "mice", "cats"]
    
    # Initialize Porter Stemmer
    stemmer = PorterStemmer()
    
    # Display results
    print("=" * 50)
    print("NLTK Stemming with PorterStemmer")
    print("=" * 50)
    print()
    print("Original     | Stem")
    print("-" * 26)
    
    for word in words:
        stem = stemmer.stem(word)
        print(f"{word:12} | {stem}")
    
    print()
    print("=" * 50)
    print("Key Observations:")
    print("=" * 50)
    print("✓ Regular forms normalized: running/runs → run")
    print("✓ Regular plural normalized: cats → cat")
    print("✗ Irregular verb NOT unified: ran → ran (not 'run')")
    print("✗ Comparatives NOT normalized: better/best unchanged")
    print("✗ Irregular plural NOT unified: mice → mice (not 'mouse')")
    print()
    print("Stemming is fast but misses irregular and semantic patterns.")
    print("=" * 50)


if __name__ == "__main__":
    demonstrate_stemming()
