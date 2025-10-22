"""
Transferaufgabe 9.7.A.01
Task (DE): a) Lese einen Text aus einer Datei, die Unicode-Zeichen enthält, und speichere den Text in
           einer Variablen. Verwende dazu die with-Anweisung und stelle sicher, dass die Datei korrekt
           geschlossen wird.
           b) Verwende reguläre Ausdrücke, um alle Wörter im Text zu finden, die mit einem Großbuchstaben
           beginnen, und speichere diese Wörter in einer Liste.
           c) Erstelle eine Funktion, die die Anzahl der Vorkommen jedes Wortes in der Liste aus b)
           zählt und diese in einem Dictionary speichert.
           d) Speichere das Dictionary aus c) in einer JSON-Datei. Stelle sicher, dass Umlaute und
           Sonderzeichen korrekt gespeichert werden.
           e) Lies die JSON-Datei, die du in d) erstellt hast, und gib den Inhalt in der Konsole aus.
           Verwende hierbei die richtige Kodierung, um Umlaute und Sonderzeichen korrekt darzustellen.
Task (EN): a) Read a text from a file that contains Unicode characters and store the text in a variable.
           Use the with statement for this and ensure that the file is properly closed.
           b) Use regular expressions to find all words in the text that start with a capital letter and
           store these words in a list.
           c) Create a function that counts the number of occurrences of each word in the list from b)
           and stores this in a dictionary.
           d) Save the dictionary from c) in a JSON file. Ensure that umlauts and special characters
           are saved correctly.
           e) Read the JSON file that you created in d) and output the content to the console.
           Use the correct encoding to display umlauts and special characters correctly.
"""

import re
import json

FILE_TXT = "example.txt"
FILE_JSN = "example.json"


def read_text(file_name):
    # Read file with UTF-8 encoding
    with open(file_name, "r", encoding="utf-8") as file:
        return file.read()


def find_word(content):
    # Find words starting with capital letter
    return re.findall("[A-Z]\w*", content)


def count_words(words_list):
    # Count occurrences of each word
    counts = {}
    for word in words_list:
        if word in counts:
            counts[word] += 1
        else:
            counts[word] = 1
    return counts


def save_to_json(words_dict, file_name):
    # Save dict to JSON with UTF-8
    with open(file_name, "w", encoding="utf-8") as file:
        json.dump(words_dict, file, ensure_ascii=False, indent=4)


def read_json(file_name):
    # Load and print JSON with UTF-8
    with open(file_name, "r", encoding="utf-8") as file:
        content = json.load(file)
        print(content)


content = read_text(FILE_TXT)
capital_words = find_word(content)
words_count = count_words(capital_words)
save_to_json(words_count, FILE_JSN)
read_json(FILE_JSN)
