"""
Ubung 3.2.U.01
Task (EN): Develop a simple Python script that demonstrates the basics of text processing
           and sentiment analysis. Your script should perform the following tasks:
           a) Use spaCy to tokenize a German text and output the tokens. Choose a short text of your choice.
           b) Perform a simple sentiment analysis on a given sentence using NLTK's VADER module. Since VADER
           was primarily developed for English texts, translate the German sentence into English first. You can use any translation tool of your choice.
           c) Briefly explain the differences between a rule-based and an AI-based chatbot. Develop a small example (pseudocode or description) that shows
           how both types of chatbots could react to the question "What time is it?".
           Note: For sentiment analysis with NLTK, it is necessary to download the VADER lexicon, if not already done, as well as install the googletrans library for translation.
"""

# =============================================================================
# Task A: German Text Tokenization using spaCy
# =============================================================================
# Purpose: Demonstrate tokenization by splitting German text into individual
#          tokens (words, punctuation, numbers) using spaCy's German model.
# =============================================================================

import spacy

# Define test data: German text with variety (words, punctuation, time format)
german_text = "Heute ist ein wunderschöner Tag! Die Sonne scheint, und ich gehe um 15:30 Uhr spazieren."

# Load spaCy's German language model (small version)
# This model contains German tokenization rules, POS tagging, etc.
nlp = spacy.load("de_core_news_sm")

# Process the text through spaCy pipeline
# Creates a Doc object containing tokens and linguistic annotations
doc = nlp(german_text)

# Output: Display each token on a separate line
print("=== Task A: Tokenization Output ===")
for token in doc:
    print(token.text)

# =============================================================================
# Task B: Sentiment Analysis using VADER
# =============================================================================

# Define German sentence with positive sentiment
german_sentence_negative = (
    "Dieser Film war schrecklich und langweilig. Ich bin sehr enttäuscht."
)

# Import translation library
from googletrans import Translator

# Initialize translator
translator = Translator()

# Translate German → English (VADER works best with English)
english_sentence_negative = translator.translate(
    german_sentence_negative, src="de", dest="en"
)
print(f"Translation: {english_sentence_negative.text}")

# Import VADER sentiment analyzer
from vaderSentiment.vaderSentiment import SentimentIntensityAnalyzer

# Initialize analyzer
analyzer = SentimentIntensityAnalyzer()

# Run sentiment analysis
scores = analyzer.polarity_scores(english_sentence_negative.text)

print("\n=== Task B: Sentiment Analysis Results ===")
print(f"Original (DE): {german_sentence_negative}")
print(f"Translation (EN): {english_sentence_negative.text}")
print(f"\nSentiment Scores:")
print(f"  Positive: {scores['pos']:.2%}")
print(f"  Negative: {scores['neg']:.2%}")
print(f"  Neutral: {scores['neu']:.2%}")
print(f"  Compound: {scores['compound']:.4f}")

# Interpret compound score
if scores["compound"] >= 0.05:
    sentiment = "POSITIVE"
elif scores["compound"] <= -0.05:
    sentiment = "NEGATIVE"
else:
    sentiment = "NEUTRAL"

print(f"\nOverall Sentiment: {sentiment}")
