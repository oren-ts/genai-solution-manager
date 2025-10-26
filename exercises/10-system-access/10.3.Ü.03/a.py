"""
Übung 10.3.Ü.03
Task (DE): a) Verwende das Modul os und json, um ein Verzeichnis namens meine_daten zu erstellen, falls es noch nicht existiert.
           Speichere in diesem Verzeichnis eine Datei namens daten.json, die eine Liste von Wörterbüchern (Dictionaries) enthält.
           Jedes Wörterbuch soll die Schlüssel name, alter und beruf mit entsprechenden Werten für drei fiktive Personen enthalten.
           b) Lese die Datei daten.json aus dem Verzeichnis meine_daten und gib die Inhalte auf der Konsole aus.
           Verwende dazu die with-Anweisung und behandele mögliche Ausnahmen mit try und except.
           c) Erweitere das Skript um eine Funktion aktualisiere_daten, die einen neuen Eintrag zu der Liste in daten.json hinzufügt.
           Der neue Eintrag soll durch Benutzereingabe über die Konsole gesammelt werden. Nutze dafür die Funktion input()
           für die Schlüssel name, alter, und beruf. Speichere die aktualisierten Daten wieder in daten.json.
Task (EN): a) Use the os and json modules to create a directory named **my_data** if it does not already exist. Save a file named
           data.json in this directory that contains a list of dictionaries. Each dictionary should have the keys name, age, and
           profession with corresponding values for three fictional people.
           b) Read the data.json file from the **my_data** directory and print its contents to the console. Use the with
           statement and handle possible exceptions with try and except.
           c) Extend the script with a function **update_data** that adds a new entry to the list in data.json.
           The new entry should be collected from user input via the console. Use the input() function for the keys name, age,
           and profession. Save the updated data back into data.json.
"""

"""
Übung 10.3.Ü.03 - Your Solution with Corrections
Changes are marked with comments explaining what was changed and why.
"""
import os
import json


def create_directory(dirname: str) -> None:
    if os.path.isdir(dirname):
        print(f"Directory {dirname} already exists.")
    else:
        os.makedirs(dirname, exist_ok=True)
        print(f"Directory {dirname} created.")


def save_list_to_file(filepath: str, data: list) -> None:
    with open(filepath, "w", encoding="utf-8") as f:
        json.dump(data, f, ensure_ascii=False, indent=4)
    print(f"Saved list to {filepath}")


def read_file(filepath: str) -> list:
    try:
        with open(filepath, "r", encoding="utf-8") as f:
            people = json.load(f)
        return people
    except FileNotFoundError:
        print(f"Error: file not found -> {filepath}")
        # CHANGE: Return empty list instead of None to avoid errors when appending
        return []  # Was: nothing (implicit None)
        # WHY: Prevents TypeError when calling people.append() later
    except OSError as e:
        print(f"Error reading file: {filepath} - {e}")
        # CHANGE: Return empty list for consistency
        return []  # Was: nothing (implicit None)
        # WHY: Makes function behavior predictable


# CHANGE: Simplified function signature - removed unnecessary parameters
# Old: def update_list_in_directory(oldpath: str, newpath: str, dirname: str) -> None:
def update_data(filepath: str) -> None:
    """
    Add new entry to the JSON file and save back to the SAME file.

    WHY CHANGED:
    - Removed 'oldpath', 'newpath', 'dirname' parameters
    - Now takes only 'filepath' (single responsibility)
    - Updates the SAME file instead of creating a new one (matches requirement)
    """

    # CHANGE: Removed unnecessary directory check
    # Old: if not os.path.isdir(dirname):
    # Old:     print(f"Error: directory {dirname} not found")
    # Old:     return
    # WHY: We already have the filepath, no need to check directory separately

    # CHANGE: Check if FILE exists instead of directory
    if not os.path.exists(filepath):  # NEW
        print(f"Error: file {filepath} not found")  # NEW
        return  # NEW
    # WHY: More appropriate check - we need the file, not just the directory

    name = input("Enter name: ")

    # CHANGE: Convert age to integer and add validation
    # Old: age = input("Enter age: ")
    while True:  # NEW: Validation loop
        age_input = input("Enter age: ")
        try:
            age = int(age_input)  # CHANGED: Convert string to int
            # WHY: Maintains type consistency with initial data

            if age < 0 or age > 150:  # NEW: Range validation
                print("Please enter a realistic age (0-150).")
                continue
            break  # NEW: Exit loop on valid input
        except ValueError:  # NEW: Handle non-numeric input
            print("Please enter a valid number for age.")
    # WHY: Original code stored age as string, but initial data uses integers

    profession = input("Enter profession: ")

    # CHANGE: age is now int instead of string
    new_person = {"name": name, "age": age, "profession": profession}
    # Old: new_person = {"name": name, "age": age, "profession": profession}
    # The key difference: age variable is now int, not string

    # CHANGE: Read from filepath (not oldpath)
    people = read_file(filepath)  # CHANGED: was oldpath
    # WHY: Simplified - we only work with one file now

    people.append(new_person)

    # CHANGE: Save to the SAME file (filepath), not a different file (newpath)
    # Old: with open(newpath, "w", encoding="utf-8") as f:
    with open(filepath, "w", encoding="utf-8") as f:  # CHANGED: newpath → filepath
        json.dump(people, f, ensure_ascii=False, indent=4)
    # WHY: Requirement says to update daten.json, not create updated.json

    # CHANGE: Updated success message
    # Old: print(f"Saved list to {newpath}")
    print(f"Successfully added '{name}' to {filepath}")  # CHANGED
    # WHY: More informative feedback


def main():
    # CHANGE: Use German names as specified in requirements
    # Old: base = "MyData"
    base = "meine_daten"  # CHANGED: MyData → meine_daten
    # WHY: Task specifically asks for "meine_daten" directory

    # CHANGE: Use German filenames as specified
    filename = "daten.json"  # NEW: define filename separately
    filepath = os.path.join(base, filename)  # NEW: cleaner

    people = [
        # CHANGE: Use German keys as specified in requirements
        # Old: {"name": "Lena Carter", "age": 29, "profession": "Graphic Designer"},
        {"name": "Lena Carter", "alter": 29, "beruf": "Graphic Designer"},  # CHANGED
        {"name": "Ethan Brooks", "alter": 35, "beruf": "Software Engineer"},  # CHANGED
        {"name": "Maya Lopez", "alter": 42, "beruf": "Architect"},  # CHANGED
    ]
    # WHY: Requirements specify German keys: "alter" and "beruf" (not "age", "profession")
    # NOTE: Keeping English names is fine - task only specifies keys must be German

    create_directory(base)

    # CHANGE: Use single filepath variable
    # Old: save_list_to_file(os.path.join(base, "data.json"), people)
    save_list_to_file(filepath, people)  # CHANGED

    # CHANGE: Use single filepath variable
    # Old: output = read_file(os.path.join(base, "data.json"))
    output = read_file(filepath)  # CHANGED
    print(output)

    # CHANGE: Simplified function call - now only needs filepath
    # Old: update_list_in_directory(
    # Old:     os.path.join(base, "data.json"),
    # Old:     os.path.join(base, "updated.json"),
    # Old:     base
    # Old: )
    update_data(filepath)  # CHANGED: Simple single parameter
    # WHY: Function is now simpler and updates the same file

    # NEW: Display updated data to verify the update worked
    print("\n--- Updated Data ---")  # NEW
    updated_output = read_file(filepath)  # NEW
    print(updated_output)  # NEW
    # WHY: Good practice to show the result of the update operation


if __name__ == "__main__":
    main()


# ============================================================================
# SUMMARY OF ALL CHANGES:
# ============================================================================
# 1. ✅ Directory name: "MyData" → "meine_daten" (requirement)
# 2. ✅ File name: "data.json" → "daten.json" (requirement)
# 3. ✅ Dictionary keys: "age"/"profession" → "alter"/"beruf" (requirement)
# 4. ✅ Function name: update_list_in_directory() → update_data() (clarity)
# 5. ✅ Function parameters: (oldpath, newpath, dirname) → (filepath) (simplification)
# 6. ✅ File update: Creates new file → Updates same file (requirement fix)
# 7. ✅ Age type: string → integer with validation (type consistency)
# 8. ✅ Error handling: Added file existence check (robustness)
# 9. ✅ Return values: None → [] in read_file exceptions (safety)
# 10. ✅ Added final output display (user feedback)
# ============================================================================
