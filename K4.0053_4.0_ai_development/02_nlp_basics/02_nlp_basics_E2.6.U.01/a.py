"""
Ubung 2.6.U.01
Task (DE): Entwickle ein Python-Skript, das folgende Aufgaben ausführt:
           a) Lies einen gegebenen deutschen Text ein. Der Text sollte mindestens drei Sätze enthalten,
           die verschiedene Emotionen ausdrücken. Zum Beispiel: “Ich liebe es, im Herbst spazieren zu gehen.
           Es regnet schon wieder, wie deprimierend. Heute ist ein großartiger Tag!”
           b) Verwende NLTK für die deutsche Sprache, um den Text in Sätze und anschließend in Wörter zu tokenisieren.
           c) Führe eine Sentiment-Analyse mit einem einfachen Ansatz durch: Erstelle eine Liste von positiven
           und negativen Wörtern. Zähle, wie viele positive und negative Wörter in dem Text vorkommen.
           Du kannst für den Anfang jeweils fünf beispielhafte positive und negative Wörter definieren.
           d) Verwende spaCy, um die Lemmatisierung der tokenisierten Wörter durchzuführen.
           Gib für jedes Wort im Text das Lemma aus.
           e) Analysiere den Text auf Emotionen basierend auf der Anzahl der positiven und negativen Wörter und gib aus,
           ob der Text insgesamt eine positive, negative oder neutrale Stimmung hat. 
Task (EN): Develop a Python script that performs the following tasks:
           a) Read in a given German text. The text should contain at least three sentences
           that express different emotions. For example: “I love going for walks in autumn.
           It is raining again, how depressing. Today is a wonderful day!”
           b) Use NLTK for the German language to tokenize the text into sentences and then into words.
           c) Perform a sentiment analysis using a simple approach: Create a list of positive
           and negative words. Count how many positive and negative words occur in the text.
           For a start, you can define five example positive and five negative words each.
           d) Use spaCy to perform lemmatization of the tokenized words. Output the lemma for each word in the text.
           e) Analyze the text for emotions based on the number of positive and negative words and output
           whether the text overall has a positive, negative, or neutral mood.
"""

# =============================================================================
# Part a: Define German Text Sample
# =============================================================================
# Text must contain at least 3 sentences expressing different emotions
TEXT = ("Ich liebe es, im Herbst spazieren zu gehen.""Es regnet schon wieder, wie deprimierend.""Heute ist ein großartiger Tag!")

# =============================================================================
# Part b: Tokenization with NLTK
# =============================================================================
import nltk
from nltk.tokenize import sent_tokenize, word_tokenize

# Download required NLTK data package for German tokenization
nltk.download('punkt_tab')

# Tokenize text into individual sentences
sentences = sent_tokenize(TEXT, language="german")

# Tokenize each sentence into individual words (including punctuation)
words = []
for sentence in sentences:
    tokenized_sentence = word_tokenize(sentence, language="german")
    words.append(tokenized_sentence)

# Display tokenization results
print(f"Sentences: {sentences}")
print(f"Words (per sentence): {words}")

# =============================================================================
# Part c: Sentiment Analysis Using Word Lists
# =============================================================================
# Define lists of positive and negative sentiment words
# Note: This is a simple approach with only 5 example words per category
positive_words = ["liebe", "großartig", "freude", "glücklich", "begeistert"]
negative_words = ["deprimierend", "schlecht", "traurig", "regnet", "schlimm"]

# Initialize counters for sentiment words
positive_count = 0
negative_count = 0

# Count occurrences of positive and negative words in the text
# Iterate through each sentence (outer loop) and each word (inner loop)
for sentence in words:
    for word in sentence:
        # Convert to lowercase for case-insensitive matching
        lowercase_word = word.lower()

        # Check if word matches positive or negative word lists
        if lowercase_word in positive_words:
            positive_count += 1
        elif lowercase_word in negative_words:
            negative_count += 1

# Display sentiment analysis results
print(f"Positive words found: {positive_count}")
print(f"Negative words found: {negative_count}")

# =============================================================================
# Part d: Lemmatization with spaCy
# =============================================================================
import spacy

# Load German language model for spaCy
# Note: Model must be installed via: python -m spacy download de_core_news_sm
nlp = spacy.load("de_core_news_sm")

# Process the text through spaCy's NLP pipeline
doc = nlp(TEXT)

# Display lemma (base form) for each token in the text
# Lemmatization reduces words to their dictionary form (e.g., "liebe" -> "lieben")
for token in doc:
    print(f"{token.text} -> {token.lemma_}")

# =============================================================================
# Part e: Overall Sentiment Classification
# =============================================================================
# Determine overall sentiment by comparing positive and negative word counts
if positive_count > negative_count:
    sentiment = "positive"
elif negative_count > positive_count:
    sentiment = "negative"
else:
    # Equal counts or both zero result in neutral sentiment
    sentiment = "neutral"

# Display final sentiment classification
print(f"The text has an overall {sentiment} sentiment based on the number of positive and negative words.")