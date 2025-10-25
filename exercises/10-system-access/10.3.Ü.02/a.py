"""
Übung 10.3.Ü.02
Task (DE): a) Erstelle eine Funktion erstelle_datei, die eine neue Textdatei mit einem vorgegebenen Namen
           und Inhalt in einem spezifischen Verzeichnis erstellt. Verwende dazu die with-Anweisung und stelle sicher,
           dass Fehler, wie z.B. fehlende Schreibberechtigungen, mit try und except abgefangen werden.
           b) Implementiere eine Funktion listdir_filter, die alle Dateien eines Verzeichnisses auflistet,
           die eine bestimmte Dateiendung haben (z.B. .txt). Nutze dazu das Modul os und eine List Comprehension.
           c) Schreibe eine Funktion umbenennen_dateien, die alle Dateien eines Verzeichnisses, die eine bestimmte
           Endung haben, umbenennt, indem sie ein Präfix hinzufügt. Verwende dazu das Modul os.
           d) Entwickle eine Funktion json_speichern, die eine Liste von Dictionaries in eine Datei im JSON-Format speichert.
           Verwende dazu das Modul json.
           e) Implementiere eine Funktion json_laden, die eine JSON-Datei liest und den Inhalt als Python-Objekt zurückgibt.
           f) Erstelle eine Funktion regex_suche, die in allen .txt-Dateien eines Verzeichnisses nach einem regulären
           Ausdruck sucht und die Namen der Dateien zurückgibt, in denen die Suche erfolgreich war.
           Für jede dieser Funktionen sollst du ein kurzes Beispiel für deren Aufruf und Verwendung schreiben.
Task (EN): a) Create a function **`erstelle_datei`** that creates a new text file with a given name and content in a specific directory.
           Use the `with` statement and make sure to catch errors such as missing write permissions with `try` and `except`.
           b) Implement a function **`listdir_filter`** that lists all files in a directory that have a specific file extension (e.g., `.txt`).
           Use the `os` module and a list comprehension.
           c) Write a function **`umbenennen_dateien`** that renames all files in a directory that have a specific extension by adding a prefix.
           Use the `os` module.
           d) Develop a function **`json_speichern`** that saves a list of dictionaries into a file in JSON format.
           Use the `json` module.
           e) Implement a function **`json_laden`** that reads a JSON file and returns the contents as a Python object.
           f) Create a function **`regex_suche`** that searches all `.txt` files in a directory for a given regular expression and returns
           the names of the files where a match was found.
           For each of these functions, write a short example of how to call and use them.
"""

import os
import json
import re


# a) Function: create_file
def create_file(filename, content, directory="."):
    """
    Creates a text file with the given name and content in the specified directory.
    Uses a 'with' statement and catches general exceptions.
    """
    full_path = os.path.join(directory, filename)
    try:
        with open(full_path, "w") as file:
            file.write(content)
        print(f"File '{filename}' was successfully created.")
    except Exception as e:
        print(f"Error creating file '{filename}': {e}")


# b) Function: listdir_filter
def listdir_filter(directory, extension):
    """
    Lists all files in 'directory' that end with the given 'extension'.
    Simple list comprehension as in the course example.
    """
    try:
        return [file for file in os.listdir(directory) if file.endswith(extension)]
    except Exception as e:
        print(f"Error listing directory '{directory}': {e}")
        return []


# c) Function: rename_files
def rename_files(directory, old_extension, prefix):
    """
    Renames all files in 'directory' with the specified extension by adding 'prefix' in front.
    Matches the simple renaming logic from the course example.
    """
    try:
        for file in os.listdir(directory):
            if file.endswith(old_extension):
                new_name = prefix + file
                os.rename(
                    os.path.join(directory, file), os.path.join(directory, new_name)
                )
        print("Files were renamed.")
    except Exception as e:
        print(f"Error renaming files in '{directory}': {e}")


# d) Function: save_json
def save_json(data, filename):
    """
    Saves a list of dictionaries as a JSON file.
    Uses json.dump without any formatting options (as in the course code).
    """
    try:
        with open(filename, "w") as file:
            json.dump(data, file)
        print(f"JSON data was saved to '{filename}'.")
    except Exception as e:
        print(f"Error saving JSON to '{filename}': {e}")


# e) Function: load_json
def load_json(filename):
    """
    Loads and returns the contents of a JSON file.
    No extra error handling (same as course code).
    """
    with open(filename, "r") as file:
        return json.load(file)


# f) Function: regex_search
def regex_search(directory, regex_pattern):
    """
    Searches all .txt files in a directory for a given regex pattern.
    Reads the whole file and checks for matches using re.search.
    """
    matching_files = []
    try:
        for file in os.listdir(directory):
            if file.endswith(".txt"):
                path = os.path.join(directory, file)
                with open(path, "r") as f:
                    content = f.read()
                    if re.search(regex_pattern, content):
                        matching_files.append(file)
    except Exception as e:
        print(f"Error during regex search in '{directory}': {e}")
    return matching_files


# ----------------------------------
# Example calls (same as course examples)
# ----------------------------------

if __name__ == "__main__":
    # a) create_file
    create_file("test.txt", "This is a test.", "myDirectory")

    # b) listdir_filter
    print(listdir_filter(".", ".txt"))

    # c) rename_files
    rename_files(".", ".txt", "new_")

    # d) save_json
    my_data = [{"name": "Anna", "age": 28}, {"name": "Bernard", "age": 35}]
    save_json(my_data, "data.json")

    # e) load_json
    loaded_data = load_json("data.json")
    print(loaded_data)

    # f) regex_search
    print(regex_search(".", r"\bTest\b"))
