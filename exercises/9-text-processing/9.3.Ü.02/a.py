"""
Übung 9.3.Ü.02
Task (DE): a) Lese eine Textdatei namens "tagebuch.txt", die in UTF-8 kodiert ist, und speichere den Inhalt
           in einer Variablen. Verwende die with-answeisung und try-except-Blöcke, um Fehler beim Dateizugriff
           zu handhaben.
           b) Verwende eine Funktion, um alle Vorkommen eines bestimmten Wortes im Text zu zählen.
           Das Wort soll als Parameter an die Funktion übergeben werden.
           c) Ersetze in dem Text alle Vorkommen des Wortes "traurig" durch "glücklich" und speichere das
           Ergebnis in einer neuen Datei namens "tagebuch_neu.txt".
           d) Schreibe eine weitere Funktion, die den aktualisierten Text nimmt und eine Liste von Sätzen
           zurückgibt, wobei jeder Satz ein Element der Liste ist. Verwende dazu eine geeignete String-Methode.
           e) Konvertiere die Liste von Sätzen in ein JSON-Format und speichere diese Daten in einer Datei
           namens "tagebuch_saetze.json".
           Stelle sicher, dass dein Skript modular aufgebaut ist und du Import-Module für
           JSON-Funktionalitäten und andere benötigte Funktionen verwendest.
Task (EN): a) Read a text file named "diary.txt", which is encoded in UTF-8, and store the content in a variable.
           Use the with-statement and try-except blocks to handle errors when accessing the file.
           b) Use a function to count all occurrences of a specific word in the text. The word should be
           passed as a parameter to the function.
           c) Replace in the text all occurrences of the word "sad" with "happy" and save the result in a
           new file named "diary_new.txt".
           d) Write another function that takes the updated text and returns a list of sentences,
           where each sentence is an element of the list. Use an appropriate string method for this.
           e) Convert the list of sentences into JSON format and save this data in a file named
           "diary_sentences.json".
"""

import json

TEXT_FILE = "diary.txt"
TEXT_FILE_NEW = "diary_new.txt"
JSON_FILE = "diary_sentences.json"


# Function to count occurrences of a specific word in the text
def count_word(content, word):
    return content.lower().count(word.lower())


# Function to replace all occurrences of an old word with a new word
def replace_word(content, old, new):
    return content.replace(old, new)


# Function to split text into a list of sentences using period as delimiter
def split_to_sentence(new_content):
    return new_content.split(".")


# Function to save a list as a JSON file with proper formatting
def save_to_json(path, list):
    with open(path, "w", encoding="utf-8") as file:
        json.dump(list, file, ensure_ascii=False, indent=4)


try:
    with open(TEXT_FILE, "r", encoding="utf-8") as file:
        content = file.read()
except FileNotFoundError:
    print(f"The file {TEXT_FILE} could not been found.")
else:
    count_words = count_word(content, "sad")
    print(f"The word 'sad' appears {count_words} times.")

    updated_content = replace_word(content, "sad", "happy")

    with open(TEXT_FILE_NEW, "w", encoding="utf-8") as new_file:
        new_file.write(updated_content)

    sentences = split_to_sentence(updated_content)

    save_to_json(JSON_FILE, sentences)
