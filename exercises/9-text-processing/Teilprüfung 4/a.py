"""
Teilprüfung 4
Task (DE): Entwickle ein Python-Programm, das eine Textdatei mit Kundenfeedback aus verschiedenen Ländern analysiert.
           Das Programm soll folgende Funktionen umfassen:
           a) Lese die Textdatei feedback.txt, die Kundenkommentare in verschiedenen Sprachen enthält.
           Verwende die with-Anweisung und stelle sicher, dass die Datei korrekt geschlossen wird, nachdem sie gelesen wurde.
           b) Verwende reguläre Ausdrücke, um alle Datumsangaben im Format DD.MM.YYYY aus dem Text zu extrahieren
           und speichere diese in einer Liste.
           c) Zähle, wie oft jedes Datum vorkommt, und speichere die Ergebnisse in einem Dictionary,
           wobei das Datum der Schlüssel und die Anzahl der Vorkommen der Wert ist.
           d) Identifiziere alle Kommentare, die das Wort "exzellent" in beliebiger Groß- oder Kleinschreibung
           enthalten. Speichere diese Kommentare in einer separaten Liste.
           e) Nutze die json-Modul, um das Dictionary mit den Datumsvorkommen und die Liste der "exzellenten"
           Kommentare in zwei separaten Dateien (datums_vorkommen.json und exzellente_feedbacks.json) zu speichern.
           f) Implementiere eine Fehlerbehandlung mit try und except, um elegante Lösungen für mögliche I/O-Fehler
           und Probleme beim Arbeiten mit Dateien zu bieten.
           g) Verwende Unicode-Nummern, um spezielle Zeichen oder Emojis in die Ausgabe einzufügen, die den
           Erfolg der Operation signalisieren.
           h) Erstelle eine Textdatei entsprechend den obigen Punkten um deinen Code zu testen.
Task (EN): Develop a Python program that analyzes a text file containing customer feedback from different countries.
           The program should include the following functions:
           a) Read the text file `feedback.txt`, which contains customer comments in different languages.
           Use the `with` statement and make sure the file is properly closed after reading.
           b) Use regular expressions to extract all dates in the format `DD.MM.YYYY` from the text and store them in a list.
           c) Count how often each date appears and store the results in a dictionary, where the date is the
           key and the number of occurrences is the value.
           d) Identify all comments that contain the word **"exzellent"** (in any capitalization). Store these comments in a separate list.
           e) Use the `json` module to save the dictionary of date occurrences and the list of “excellent” comments into two separate files:
           * `date_occurrences.json`
           * `excellent_feedbacks.json`
           f) Implement error handling using `try` and `except` to gracefully handle possible I/O errors and file-related issues.
           g) Use Unicode numbers to include special characters or emojis in the output that signal successful operation.
           h) Create a text file according to the above points to test your code.
"""

import re
import json


# ======== File names (constants) ========
FILE_FDK = "feedback.txt"  # Input text file with feedback comments
FILE_DTE = "date_occurrences.json"  # Output JSON for counted dates
FILE_EXC = "excellent_feedbacks.json"  # Output JSON for "excellent" comments


# ======== a) Extract all dates from text ========
def get_dates(content):
    """
    Uses a regular expression to find all dates in the format DD.MM.YYYY.
    Example match: 01.02.2024
    Returns a list of all found dates.
    """
    return re.findall(r"(\d{1,2}\.\d{1,2}\.\d{2,4})", content)


# ======== b) Count occurrences of each date ========
def count_dates(dates):
    """
    Takes a list of dates and counts how many times each one appears.
    Returns a dictionary like: {'01.02.2024': 2, '05.02.2024': 1}
    """
    dict = {}
    for date in dates:
        if date in dict:
            dict[date] += 1  # Increment existing key
        else:
            dict[date] = 1  # Add new key
    return dict


# ======== c) Find all comments containing “exzellent” ========
def get_excellent(content):
    """
    Finds all text lines containing the word 'exzellent' in any capitalization.
    (?i) → makes the search case-insensitive
    [^:]* → ignores the text before the first colon (country name)
    [^\n]* → captures until the end of the line
    Returns a list of comments containing 'exzellent'.
    """
    return re.findall(r"(?i)([^:]*exzellent[^\n]*)", content)


# ======== d) Save data structures to JSON files ========
def save_to_json(file_name, data):
    """
    Saves any Python object (list or dict) to a JSON file.
    Uses UTF-8 and ensure_ascii=False to keep emojis readable.
    Includes basic error handling for I/O problems.
    """
    try:
        with open(file_name, "w", encoding="utf-8") as file:
            json.dump(data, file, ensure_ascii=False, indent=4)
            print("File saved successfully \U0001f600\n")  # 😀 success emoji
    except OSError:
        print("File cannot be saved.")  # Handles disk or permission errors


# ======== e–h) Main program flow ========
try:
    # --- Read file content safely ---
    with open(FILE_FDK, "r", encoding="utf-8") as file:
        content = file.read()
        print("File read successfuly \U0001f44d\n")  # 👍 emoji for success

        # --- Extract dates and count them ---
        dates_list = get_dates(content)
        dates_dict = count_dates(dates_list)

        # --- Find comments containing “exzellent” ---
        excellent_list = get_excellent(content)

        # --- Save both results as JSON ---
        save_to_json(FILE_DTE, dates_dict)
        save_to_json(FILE_EXC, excellent_list)

# --- Handle possible errors ---
except FileNotFoundError:
    print(f"File {FILE_FDK} not found.")
except OSError as err:
    print(f"An unexpected error: {err}.")
