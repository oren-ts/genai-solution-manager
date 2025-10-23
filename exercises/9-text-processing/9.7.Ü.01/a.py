"""
Übung 9.7.Ü.01
Task (DE): a) Definiere eine Variable text, die einen mehrzeiligen String speichert, welcher Sonderzeichen
           und Unicode-Zeichen enthält. Verwende mindestens drei verschiedene Escape-Sequenzen und zwei
           Unicode-Zeichen (z.B. ein Emoji und ein Zeichen aus einem anderen Schriftsystem).
           b) Zähle, wie oft ein bestimmtes Wort in text vorkommt. Das Wort soll als Eingabe über die Konsole
           gegeben werden.
           c) Ersetze in text alle Vorkommen eines bestimmten Wortes (ebenfalls über die Konsole eingegeben)
           durch ein anderes Wort (auch über die Konsole eingegeben) und gib den neuen Text aus.
           d) Speichere den modifizierten Text in einer Datei mit dem Namen modifizierter_text.txt unter
           Verwendung der with-Anweisung.
           e) Dies eine Datei namens daten.json, die eine Liste von Dictionaries enthält, ein.
           Verwende das JSON-Modul, um die Datei zu laden. Gib anschließend die Daten in der Konsole aus.
Task (EN): a) Define a variable text that stores a multi-line string containing special characters and Unicode
           characters. Use at least three different escape sequences and two Unicode characters
           (e.g., an emoji and a character from another writing system).
           b) Count how often a specific word appears in text. The word should be provided as input
           via the console.
           c) Replace all occurrences of a specific word in text (also provided via the console)
           with another word (also provided via the console) and output the new text.
           d) Save the modified text in a file named modified_text.txt using the with statement.
           e) Read a file named data.json that contains a list of dictionaries. Use the JSON module
           to load the file. Then output the data in the console.
"""

import json

# Part a) - Create text with special characters and escape sequences
text = "This is a test. Is this working? I think this is great!\nNew line here.\tTab character too.\nThe word 'is' appears in 'This' and 'is'.\n\\Backslash example\nRepeat: test test test.\nJapanese: こんにちは (Hello)\nEmoji time: \u2764\U0001f600\U0001f913\nMixed case: IS Is is iS\nPunctuation test: is, is. is! is? (is)\nNumbers: test123 123test test-123\nMultiple spaces:  is  is  is\nEnd with is"

# Part b) - Count word occurrences (with punctuation handling)
searched_word = input("Please enter the word to search for: ")

# Remove punctuation before counting
cleaned_text = text.lower()
for char in ".,!?():;-\"'":
    cleaned_text = cleaned_text.replace(char, " ")

words_list = cleaned_text.split()
word_count = words_list.count(searched_word.lower())
print(f"The word '{searched_word}' appears {word_count} times.")

# Part c) - Replace words (with punctuation handling)
word_to_replace = input("Please enter the word to be replaced: ")
replacement_word = input("Please enter the replacement word: ")
modified_text = text.replace(word_to_replace, replacement_word)
print("Modified Text:")
print(modified_text)

# Part d) - Save modified text to file
with open("modified_text.txt", "w", encoding="utf-8") as file:
    file.write(modified_text)

# Part e) - Read and display JSON file
try:
    with open("data.json", "r", encoding="utf-8") as file:
        data = json.load(file)
        print("Contents of 'data.json':")
        print(data)
except FileNotFoundError:
    print("The file 'data.json' was not found.")
