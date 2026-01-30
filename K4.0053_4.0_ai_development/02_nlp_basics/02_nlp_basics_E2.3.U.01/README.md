# Stemming vs. Lemmatization in NLP

**Exercise:** 02.3.Ü.01 - NLP Fundamentals  
**Topic:** Understanding the difference between stemming and lemmatization in Natural Language Processing

---

## Overview

This exercise explores two fundamental text normalization techniques in NLP: **stemming** and **lemmatization**. Both techniques reduce word variations to help NLP systems recognize that different forms represent the same underlying concept, but they use very different approaches.

---

## 1. Why NLP Uses Word Normalization

In natural language, the same underlying concept can appear in different word forms (e.g., *run, running, ran, runs*). **Word normalization** reduces these variations so NLP systems can treat related forms as the same concept, improving tasks like:

- **Search engines** - Find documents containing "running" when searching for "run"
- **Text classification** - Group related words for better pattern recognition  
- **Sentiment analysis** - Aggregate emotional signals across word variants
- **Analytics** - Count and cluster words by meaning, not surface form

Two common normalization techniques are **stemming** and **lemmatization**.

---

## 2. Stemming: Rule-Based Word Reduction

### How It Works

**Stemming** reduces a word to a shorter base form (a "stem") using **rule-based heuristics** - typically by removing or modifying suffixes. It does **not** use:
- A dictionary or lexicon
- Grammatical context
- Part-of-speech information

### Characteristics

✅ **Fast and simple** - Pure algorithmic approach  
❌ **May produce non-words** - e.g., "better" → "bett"  
❌ **Fails on irregular forms** - e.g., "ran" stays "ran" (not unified with "run")  
❌ **Context-blind** - Treats all instances of a word the same way

### Example: NLTK PorterStemmer

```python
from nltk.stem import PorterStemmer

words = ["running", "ran", "runs", "better", "best", "mice", "cats"]
stemmer = PorterStemmer()

print("=== NLTK Stemming (PorterStemmer) ===")
print("Original     | Stem")
print("-" * 26)

for w in words:
    print(f"{w:12} | {stemmer.stem(w)}")
```

**Output:**
```
Original     | Stem
--------------------------
running      | run
ran          | ran          ← Not unified with "run"
runs         | run
better       | better       ← Not normalized to "good"
best         | best         ← Not normalized to "good"
mice         | mice         ← Not normalized to "mouse"
cats         | cat
```

**Key Observation:** Stemming successfully handles regular forms (running/runs → run, cats → cat) but fails on irregular verbs, comparatives, and irregular plurals.

---

## 3. Lemmatization: Linguistic Normalization

### How It Works

**Lemmatization** maps a word to its **lemma** (dictionary/base form) using **linguistic analysis**:
- Vocabulary knowledge (lexicon lookup)
- Morphological rules (word formation patterns)
- **Part-of-speech (POS) tagging** - Critical for disambiguation
- Context awareness

### Characteristics

✅ **Always produces real words** - Returns valid dictionary entries  
✅ **Handles irregular forms** - e.g., "ran" → "run", "mice" → "mouse"  
✅ **Meaning-aware** - Uses grammar and context  
⚠️ **Slower** - More computational overhead  
⚠️ **Context-dependent** - Results depend on POS tagging accuracy

### Example: spaCy Lemmatization

```python
import spacy

words = ["running", "ran", "runs", "better", "best", "mice", "cats"]

# Provide sentence context for better POS tagging
text = "I run, I runs, I ran, and I am running. These are better and best examples. I see mice and cats."

nlp = spacy.load("en_core_web_sm")
doc = nlp(text)

print("=== spaCy Lemmatization (with sentence context) ===")
print("Original     | Lemma    | POS")
print("-" * 45)

targets = set(words)
for token in doc:
    if token.text.lower() in targets:
        print(f"{token.text:12} | {token.lemma_:8} | {token.pos_}")
```

**Output:**
```
Original     | Lemma    | POS
---------------------------------------------
run          | run      | VERB
runs         | run      | VERB
ran          | run      | VERB      ← Correctly unified!
running      | run      | VERB
better       | well     | ADJ       ← Linguistic lemma
best         | good     | ADJ       ← Correctly normalized!
mice         | mouse    | NOUN      ← Correctly unified!
cats         | cat      | NOUN
```

**Key Observation:** Lemmatization successfully normalizes irregular verbs (ran → run), irregular plurals (mice → mouse), and superlatives (best → good).

**Note on "better → well":** spaCy's lemmatizer treats "better" as the comparative form of "well" in its linguistic model. While intuitive expectation might be "good", this demonstrates that lemmatization is **meaning-driven and POS-aware**, not just intuitive pattern matching.

---

## 4. Direct Comparison: Proof Points

### Proof Point 1: Irregular Verb Normalization

| Technique | Input | Output | Analysis |
|-----------|-------|--------|----------|
| **Stemming** | ran | ran | ❌ Not unified - stays unchanged |
| **Lemmatization** | ran | run | ✅ Correctly maps to base verb |

**Meaning Captured:** Lemmatization unifies past tense with present, capturing the core action concept.

---

### Proof Point 2: Irregular Plural Normalization

| Technique | Input | Output | Analysis |
|-----------|-------|--------|----------|
| **Stemming** | mice | mice | ❌ Not unified - stays unchanged |
| **Lemmatization** | mice | mouse | ✅ Correctly maps to singular form |

**Meaning Captured:** Lemmatization connects irregular plural to singular dictionary form.

---

### Proof Point 3: Superlative Adjective Normalization

| Technique | Input | Output | Analysis |
|-----------|-------|--------|----------|
| **Stemming** | best | best | ❌ Not normalized |
| **Lemmatization** | best | good | ✅ Maps to base adjective |

**Meaning Captured:** Lemmatization reduces superlative back to base meaning.

---

## 5. Real-World Application: Search Engine Example

### Scenario
A **search engine** for sports articles receives the query:
> "How to run faster"

### Without Normalization
Documents are indexed with exact word forms:
- Document A: "running drills for beginners"
- Document B: "he ran daily marathons"  
- Document C: "she runs 5km every morning"

The system treats `run`, `running`, `ran`, and `runs` as **completely different words**, resulting in:
- ❌ Missed relevant results (poor recall)
- ❌ Diluted relevance signals
- ❌ Fragmented topic clustering

### With Normalization (Stemming or Lemmatization)
All variants map to the same base concept:
- ✅ All documents match the query
- ✅ Relevance signals are aggregated
- ✅ Improved ranking and recall

### Why Lemmatization Wins
For the query "best running shoes", stemming might produce:
- "best" → "best" (unchanged)
- "running" → "run"

But lemmatization produces:
- "best" → "good" (semantic base)
- "running" → "run" (verb base)

This allows matching with documents containing "good shoes for runners" through semantic connections.

---

## 6. When to Choose Each Technique

### Use Stemming When:
- ✅ Speed is critical (e.g., real-time processing of millions of documents)
- ✅ Rough grouping is sufficient (e.g., basic keyword matching)
- ✅ Limited computational resources
- ✅ Language lacks good lemmatization tools

### Use Lemmatization When:
- ✅ Accuracy matters more than speed
- ✅ Irregular forms are common (English has many!)
- ✅ Semantic precision is important (e.g., sentiment analysis, Q&A systems)
- ✅ You need human-readable normalized forms
- ✅ Sufficient computational resources available

---

## 7. Key Takeaways

1. **Stemming** = Fast, crude, rule-based suffix removal
   - Good for basic text preprocessing at scale
   - Fails on irregular forms and semantic relationships

2. **Lemmatization** = Slower, accurate, linguistically-informed normalization
   - Produces real dictionary words
   - Handles irregular forms through lexicon and grammar
   - Context-dependent via POS tagging

3. **Both techniques help NLP systems focus on meaning rather than surface variation**, improving:
   - Search recall and precision
   - Text classification accuracy
   - Analytics and clustering quality
   - Overall semantic understanding

4. **The choice depends on your use case:** Speed vs. accuracy, scale vs. precision, rough grouping vs. semantic understanding.

---

## Files in This Exercise

- **`stemming_nltk.py`** - Standalone NLTK stemming example
- **`lemmatization_spacy.py`** - Standalone spaCy lemmatization example
- **`combined_example.py`** - Side-by-side comparison of both techniques

---

## Requirements

### For Stemming (NLTK)
```bash
pip install nltk
```

### For Lemmatization (spaCy)
```bash
pip install spacy
python -m spacy download en_core_web_sm
```

---

## References

- NLTK Documentation: https://www.nltk.org/
- spaCy Documentation: https://spacy.io/
- Porter Stemmer Algorithm: https://tartarus.org/martin/PorterStemmer/

---

**Exercise Completed:** 2026-01-30  
**Author:** Oren  
**Course:** K4.0053_4.0 AI Development
