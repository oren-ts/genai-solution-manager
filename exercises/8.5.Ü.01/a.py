"""
Transferaufgabe 8.5.Ü.01
Task (DE): Entwickle ein Python-Skript, das folgende Aufgaben ausführt und dabei die genannten Themenbereiche abdeckt.
           Du hast 90 Minuten Zeit, um diese Übung zu bearbeiten.
           a) Definiere eine Funktion speichere_daten, die als Parameter eine Liste von Tupeln entgegennimmt.
           Jedes Tupel enthält zwei Werte: einen Namen (String) und ein Alter (Integer). Die Funktion soll diese Daten
           in einer Datei namens personen.txt speichern. Verwende dabei die with-Anweisung und den Modus 'w' zum Öffnen der Datei.
           Jedes Tupel soll in einer neuen Zeile in folgendem Format gespeichert werden: Name: Alter.
           b) Definiere eine weitere Funktion lade_daten, die die zuvor gespeicherten Daten aus der Datei personen.txt
           liest und als Liste von Dictionaries zurückgibt, wobei jedes Dictionary einen Namen und ein Alter enthält.
           c) Implementiere eine Fehlerbehandlung in beiden Funktionen, um mit möglichen Laufzeitfehlern umzugehen,
           z.B. wenn die Datei nicht existiert oder ein Schreib-/Lesefehler auftritt. Gib in solchen Fällen eine aussagekräftige Fehlermeldung aus.
           d) Schreibe eine Kontrollstruktur, die überprüft, ob die zurückgegebene Liste von lade_daten leer ist oder nicht.
           Wenn sie nicht leer ist, gib die geladenen Daten formatiert in der Konsole aus. Verwende dazu eine Schleife.
Task (EN): Develop a Python script that performs the following tasks and covers the mentioned topic areas.
           You have 90 minutes to complete this exercise.
           a) Define a function save_data that takes a list of tuples as a parameter.
           Each tuple contains two values: a name (string) and an age (integer). The function should save this data
           in a file named persons.txt. Use the with statement and the 'w' mode to open the file.
           Each tuple should be saved on a new line in the following format: Name: Age.
           b) Define another function load_data that reads the previously saved data from the file persons.txt
           and returns it as a list of dictionaries, where each dictionary contains a name and an age.
           c) Implement error handling in both functions to handle possible runtime errors,
           e.g., if the file does not exist or a write/read error occurs. In such cases, output a meaningful error message.
           d) Write a control structure that checks whether the returned list from load_data is empty or not.
           If it is not empty, output the loaded data formatted in the console. Use a loop for this.
"""


def save_data(data_list):
    try:
        with open("persons.txt", "w") as persons:
            for name, age in data_list:
                persons.write(f"{name}: {age}\n")
    except IOError:
        print("Error: An issue occurred while writing to the file.")
    except PermissionError:
        print("Error: Permission denied to write to the file.")


def load_data(path):
    data_list = []
    try:
        with open(path, "r") as persons:
            for line in persons:
                parts = line.strip().split(":")
                if len(parts) == 2:
                    name = parts[0].strip()
                    age = int(parts[1].strip())
                    person_dict = {"name": name, "age": age}
                    data_list.append(person_dict)
        return data_list
    except FileNotFoundError:
        print("Error: The file 'persons.txt' was not found.")
        return []
    except ValueError:
        print("Error: Invalid data format in the file (e.g., age is not a number).")
        return []
    except IOError:
        print("Error: An issue occurred while reading the file.")
        return []


def main():
    # Get user input for name and age
    name = input("Enter your name: ")
    age = int(input("Enter your age: "))

    # Create a list with one tuple containing name and age
    data_list = [(name, age)]

    # Call the save_data function with the list of tuples
    save_data(data_list)

    # Load the data and check if it's not empty
    loaded_data = load_data("persons.txt")
    if loaded_data:  # True if the list is not empty
        print("Loaded data:")
        for person in loaded_data:
            print(f"Name: {person['name']}, Age: {person['age']}")


main()
