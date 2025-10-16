"""
Übung 8.5.Ü.02
Task (DE): Erstelle ein Python-Programm, das folgende Funktionen umsetzt:
           a) Definiere eine Funktion speichere_daten, die als Parameter eine Liste von Tupeln entgegennimmt.
           Jedes Tupel soll Daten eines Studenten repräsentieren, bestehend aus (Name, Matrikelnummer, Studiengang).
           Die Funktion soll diese Daten in einer Textdatei namens studentendaten.txt speichern. Verwende die with-Anweisung,
           um sicherzustellen, dass die Datei korrekt geöffnet und geschlossen wird. Jeder Student soll in einer neuen
           Zeile in folgendem Format gespeichert werden: "Name: [Name], Matrikelnummer: [Matrikelnummer], Studiengang: [Studiengang]".
           b) Definiere eine zweite Funktion lade_daten, die die gespeicherten Daten aus der Datei studentendaten.txt liest
           und als Liste von Dictionaries zurückgibt, wobei jedes Dictionary die Daten eines Studenten enthält.
           c) Implementiere eine einfache Fehlerbehandlung in beiden Funktionen, um den Fall zu behandeln,
           dass die Datei nicht geöffnet oder gefunden werden kann. Gib in diesem Fall eine entsprechende Fehlermeldung aus.
Task (EN): Create a Python program that implements the following functions:
           a) Define a function `speichere_daten` that takes a list of tuples as a parameter.
           Each tuple should represent the data of a student, consisting of (Name, Matriculation number, Course of study).
           The function should save these data in a text file named `studentendaten.txt`. Use the `with` statement
           to ensure that the file is opened and closed correctly. Each student should be saved in a new line
           in the following format: "Name: [Name], Matrikelnummer: [Matrikelnummer], Studiengang: [Studiengang]".
           b) Define a second function `lade_daten` that reads the saved data from the file `studentendaten.txt`
           and returns it as a list of dictionaries, where each dictionary contains the data of a student.
           c) Implement simple error handling in both functions to handle the case that the file cannot be opened or found.
           In this case, output a corresponding error message.
"""

student_list = [
    ("Anna Müller", 12345, "Computer Science"),
    ("Ben Schmidt", 12346, "Data Science"),
    ("Clara Weber", 12347, "Artificial Intelligence"),
    ("David Fischer", 12348, "Software Engineering"),
]


def save_data(data_list):
    try:
        with open("student_data.txt", "w") as students:
            for name, student_id, course in data_list:
                students.write(
                    f"Name: {name}, StudentID: {student_id}, Course: {course}\n"
                )
    except IOError:
        print("Error while saving data.")


def load_data():
    try:
        students_data = []
        with open("student_data.txt", "r") as students:
            for line in students:
                name, student_id, course = line.strip().split(", ")
                student = {
                    "Name": name.split(": ")[1],
                    "StudentID": student_id.split(": ")[1],
                    "Course": course.split(": ")[1],
                }
                students_data.append(student)
        return students_data
    except IOError:
        print("Error while uploading data.")
        return []


save_data(student_list)
uploaded_data = load_data()
print(uploaded_data)
