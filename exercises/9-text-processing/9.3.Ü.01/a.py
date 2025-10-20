"""
Übung 9.3.Ü.01
Task (DE): Erstelle ein Python-Skript, das folgende Aufgaben ausführt:
           a) Definiere eine Variable text, die einen mehrzeiligen String speichert. Der String soll
           mindestens ein Unicode-Zeichen, eine Escape-Sequenz und variable Teile enthalten, die
           durch die format() Methode ersetzt werden. Verwende für das Unicode-Zeichen ein Emoji und
           für die Escape-Sequenz einen Zeilenumbruch.
           b) Verwende die print() Funktion, um den String auszugeben.
           c) Lese eine Textdatei namens beispiel.txt, die du zuvor selbst erstellen musst, mit der
           with-Anweisung und utf-8 Encoding. Speichere den Inhalt der Datei in einer Variablen und gib ihn aus.
           d) Schreibe eine Funktion speichere_json, die ein Python-Objekt (z.B. ein Dictionary mit
           einigen Schlüssel-Wert-Paaren) in eine Datei im JSON-Format speichert. Verwende dazu das Modul json.
           e) Verwende die try und except Blöcke, um Fehler beim Lesen einer nicht existierenden Datei zu behandeln.
           Gib eine benutzerfreundliche Nachricht aus, wenn die Datei nicht gefunden wird.
Task (EN): Create a Python script that performs the following tasks:
           a) Define a variable text that stores a multi-line string. The string should contain at least one
           Unicode character, an escape sequence, and variable parts that are replaced using the format() method.
           Use an emoji for the Unicode character and a line break for the escape sequence.
           b) Use the print() function to output the string.
           c) Read a text file named example.txt, which you must create yourself beforehand, using the with
           statement and UTF-8 encoding. Store the content of the file in a variable and print it.
           d) Write a function save_json that saves a Python object (e.g., a dictionary with some
           key-value pairs) to a file in JSON format. Use the json module for this.
           e) Use try and except blocks to handle errors when reading a non-existent file.
           Output a user-friendly message if the file is not found.
"""

import json

TEXT_FILE = "example.txt"
JSON_FILE = "example.json"


def main():
    # Part a: Define multiline string with Unicode emoji, escape sequence (\n for line break), and placeholder for format()
    text = """
    An example text with an empjie: \U0001f600
    An example of line break \n
    An example text that contains {0} different parts
    """
    # Part b: Print the formatted string (replaces {0} with a value)
    print(text.format("3"))

    # Part c: Read the pre-created text file with with-statement and UTF-8 encoding
    # Part e: Use try/except to handle if file doesn't exist, with user-friendly message
    try:
        with open(TEXT_FILE, "r", encoding="utf-8") as file:
            content = file.read()
            print(content)
    except FileNotFoundError:
        print(f"File {TEXT_FILE} not found. Please create it beforehand.")

    save_json()


def save_json():
    # Part d: Example Python object (a dictionary with key-value pairs
    library_books = [
        {"title": "The Midnight Library", "author": "Matt Haig", "year": 2020},
        {"title": "Project Hail Mary", "author": "Andy Weir", "year": 2021},
        {
            "title": "The Seven Husbands of Evelyn Hugo",
            "author": "Taylor Jenkins reid",
            "year": 2017,
        },
    ]

    with open(JSON_FILE, "w") as file:
        json.dump(library_books, file, indent=4)


if __name__ == "__main__":
    main()
