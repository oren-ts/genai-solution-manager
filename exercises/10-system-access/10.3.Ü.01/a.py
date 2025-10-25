"""
Übung 10.3.Ü.01
Task (DE): a) Erstelle eine Funktion erstelle_verzeichnis, die als Argument einen Verzeichnisnamen (String) nimmt.
           Die Funktion soll mithilfe des os-Moduls überprüfen, ob das Verzeichnis bereits existiert.
           Falls nicht, soll das Verzeichnis erstellt werden. Gib eine Bestätigung aus, dass das Verzeichnis erstellt
           wurde oder bereits existiert.
           b) Erstelle eine Funktion speichere_text_in_datei, die zwei Argumente nimmt: den Dateinamen (String) und
           den zu speichernden Text (String). Die Funktion soll den Text in der angegebenen Datei speichern.
           Verwende die with-Anweisung, um die Datei zu öffnen und sicherzustellen, dass sie korrekt geschlossen wird.
           c) Erstelle eine Funktion lese_datei, die als Argument einen Dateinamen (String) nimmt und den Inhalt der
           Datei ausgibt. Fange mögliche Ausnahmen ab, die beim Versuch, die Datei zu lesen, auftreten können
           (z.B. wenn die Datei nicht existiert), und gib eine entsprechende Fehlermeldung aus.
           d) Erstelle eine Funktion liste_dateien_in_verzeichnis, die als Argument einen Verzeichnisnamen (String)
           nimmt und alle Dateien in diesem Verzeichnis auflistet. Verwende das os-Modul, um auf das Dateisystem zuzugreifen.
           e) Schreibe ein Hauptprogramm, das die Funktionen in folgender Reihenfolge aufruft: erstelle_verzeichnis mit
           dem Verzeichnisnamen "MeineDaten", speichere_text_in_datei mit einem beliebigen Text in einer Datei namens
           "beispiel.txt" im Verzeichnis "MeineDaten", lese_datei für "beispiel.txt" und liste_dateien_in_verzeichnis
           für das Verzeichnis "MeineDaten".
Task (EN): a) Create a function **`create_directory`** that takes a directory name (string) as an argument.
           The function should use the **`os`** module to check whether the directory already exists.
           If it does not exist, the directory should be created. Print a confirmation message stating whether the
           directory was created or already exists.
           b) Create a function **`save_text_to_file`** that takes two arguments: the file name (string) and the text to be saved (string).
           The function should save the text in the specified file. Use the **`with`** statement to open the file and ensure it is
           properly closed afterward.
           c) Create a function **`read_file`** that takes a file name (string) as an argument and prints the contents of the file.
           Catch possible exceptions that might occur when trying to read the file (for example, if the file does not exist),
           and print an appropriate error message.
           d) Create a function **`list_files_in_directory`** that takes a directory name (string) as an argument and lists all
           files in that directory. Use the **`os`** module to access the file system.
           e) Write a **main program** that calls the functions in the following order:
           1. Call **`create_directory`** with the directory name `"MyData"`.
           2. Call **`save_text_to_file`** with any text in a file named `"example.txt"` inside the `"MyData"` directory.
           3. Call **`read_file`** for `"example.txt"`.
           4. Call **`list_files_in_directory`** for the `"MyData"` directory.
"""

import os  # Import operating system module for file and directory operations


def create_directory(dirname: str) -> None:
    """Create dirname if it does not exist. Print whether it was created or already existed."""
    if os.path.isdir(dirname):
        print(f"Directory alrerady exist: {dirname}")
    else:
        os.mkdir(dirname)  # Create a single directory (no nested folders)
        print(f"Directory created: {dirname}")


def save_text_to_file(filepath: str, text: str) -> None:
    """Write text to filepath using UTF-8 and a context manager (with)."""
    with open(filepath, "w", encoding="utf-8") as f:
        f.write(text)
    print(f"Saved text to: {filepath}")


def read_file(filepath: str) -> None:
    """Print the contents of filepath. Print a clear error if the file is missing or unreadable."""
    try:
        with open(filepath, "r", encoding="utf-8") as f:
            print(f.read())
    # Handle specific errors to prevent program crash and give friendly messages
    except FileNotFoundError:
        print(f"Error: file not found -> {filepath}")
    except PermissionError:
        print(f"Error: permission denied -> {filepath}")
    except OSError as e:
        print(f"Error reading file: {filepath} - {e}")


def list_files_in_directory(dirname: str) -> None:
    """Print all file names (not directories) inside dirname, one per line."""
    if not os.path.isdir(dirname):
        print(f"Error: directory not found -> {dirname}")
        return
    # Iterate over all items in directory and show only files (ignore subfolders)
    for name in os.listdir(dirname):
        path = os.path.join(dirname, name)
        if os.path.isfile(path):
            print(name)


def main():
    """Orchestrate the required call order."""
    base = "MyData"  # Folder name for all file operations
    create_directory(base)
    file_path = os.path.join(base, "example.txt")  # Build full path safely
    save_text_to_file(file_path, "Hello from Python Übung 10.3.Ü.01")
    read_file(file_path)
    list_files_in_directory(base)


if __name__ == "__main__":
    main()  # Run only when executed directly (not imported)
