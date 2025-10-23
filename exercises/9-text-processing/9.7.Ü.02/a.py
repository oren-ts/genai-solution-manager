"""
Übung 9.7.Ü.02
Task (DE): a) Definiere eine Variable, die einen Text in Form eines Strings speichert. Dieser Text soll
           mindestensein Unicode-Zeichen enthalten, welches nicht auf einer normalen Tastatur zu finden ist.
           Verwende dazu die Funktion chr() mit einer Unicode-Nummer deiner Wahl.
           b) Füge dem Text eine Escape-Sequenz hinzu, die einen Zeilenumbruch darstellt.
           c) Verwende eine Stringmethode, um zu zählen, wie oft ein bestimmtes Zeichen in deinem Text vorkommt.
           d) Erstelle eine Liste mit mehreren Strings. Verwende die Methode .join(), um einen neuen String
           zu erstellen, der die Elemente der Liste durch ein Komma getrennt enthält.
           e) Speichere den Text aus a) in einer Datei. Verwende dazu die with-Anweisung und den
           Modus 'w' für das Schreiben in Dateien.
           f) Lies den Text aus der Datei, die du in e) erstellt hast, und gib ihn auf der Konsole aus.
           Verwende dazu ebenfalls die with-Anweisung, diesmal mit dem Modus 'r' für das Lesen aus Dateien.
           g) Fange mögliche Ausnahmen, die beim Lesen der Datei auftreten können, mit try und except ab.
           h) Verwende das JSON-Format, um eine einfache Datenstruktur (z.B. ein Dictionary mit einigen
           Schlüssel-Wert-Paaren) in einer Datei zu speichern und wieder zu laden.
Task (EN): a) Define a variable that stores a text as a string. This text should include at least one Unicode character
           that cannot be typed on a regular keyboard. Use the chr() function with a Unicode number of your choice for this.
           b) Add an escape sequence to the text that represents a line break.
           c) Use a string method to count how many times a specific character appears in your text.
           d) Create a list containing several strings. Use the .join() method to create a new string that joins the
           list elements separated by commas.
           e) Save the text from (a) to a file. Use the with statement and the mode 'w' to write to the file.
           f) Read the text from the file you created in (e) and display it in the console. Again, use the with statement,
           this time with the mode 'r' to read from the file.
           g) Catch any exceptions that might occur while reading the file using try and except.
           h) Use the JSON format to save and load a simple data structure (for example, a dictionary with
           some key-value pairs) to and from a file.
"""

import json

# a) Define a string with a Unicode character using chr()
# chr(9786) is the Unicode number for ☺
text = "Hello, this is a happy face " + chr(9786)

# b) Add a line break using an escape sequence \n
text += "\nThis is the second line."

# c) Count how many times a certain character appears
count_l = text.count("l")
print("The letter 'l' appears", count_l, "times in the text.\n")

# d) Create a list of strings and join them with commas
words = ["apple", "banana", "cherry"]
joined_text = ", ".join(words)
print("Joined list:", joined_text, "\n")

# e) Save the text to a file
try:
    with open("my_text.txt", "w", encoding="utf-8") as file:
        file.write(text)
    print("Text saved to file successfully!\n")
except Exception as e:
    print("Error while writing to file:", e)

# f) Read the text back from the file
try:
    with open("my_text.txt", "r", encoding="utf-8") as file:
        content = file.read()
        print("Content read from file:")
        print(content, "\n")
# g) Handle possible exceptions
except FileNotFoundError:
    print("Error: The file was not found.")
except Exception as e:
    print("An unexpected error occurred:", e)

# h) Save and load a dictionary in JSON format
data = {"name": "Alice", "age": 25, "city": "Berlin"}

# Save dictionary to JSON file
with open("data.json", "w", encoding="utf-8") as json_file:
    json.dump(data, json_file)

# Load it back
with open("data.json", "r", encoding="utf-8") as json_file:
    loaded_data = json.load(json_file)

print("Loaded JSON data:", loaded_data)
