"""
Teilprüfung 2
Task (DE): Du arbeitest für ein Unternehmen, das eine Software zur Verwaltung von Büchereien entwickelt. Deine Aufgabe ist es,
           ein Python-Programm zu schreiben, das folgende Funktionalitäten bietet:
           a) Buchsuche: Eine Funktion suche_buch(titel, autor=None), die Bücher nach Titel und optional nach Autor sucht.
           Die Funktion gibt eine Liste von Büchern zurück, die den Suchkriterien entsprechen. Wenn kein Autor angegeben ist,
           werden alle Bücher mit dem entsprechenden Titel zurückgegeben.
           b) Buch hinzufügen: Eine Funktion fuege_buch_hinzu(titel, autor, jahr), die ein neues Buch zur Bücherei-Datenbank hinzufügt.
           Die Datenbank wird als Liste von Wörterbüchern dargestellt, wobei jedes Wörterbuch ein Buch repräsentiert.
           c) Bücher nach Jahr filtern: Eine Funktion buecher_nach_jahr(jahr), die alle Bücher zurückgibt, die in einem bestimmten
           Jahr veröffentlicht wurden. Verwende die filter()-Funktion, um diese Aufgabe zu erfüllen.
           d) Anzeige der Bücherei-Datenbank: Eine Funktion zeige_datenbank(), die den aktuellen Inhalt der Bücherei-Datenbank in
           einer formatierten Ausgabe anzeigt. Hierbei soll jeder Eintrag folgende Informationen enthalten: Titel, Autor, Erscheinungsjahr.
           e) Interaktives Menü: Implementiere ein interaktives Menü, das es dem Benutzer ermöglicht, die oben genannten Funktionen
           auszuführen. Verwende eine Schleife mit while, um das Menü kontinuierlich anzuzeigen, bis der Benutzer sich entscheidet, das Programm zu beenden.
           Datenbankstruktur (Beispiel):
           buecherei_datenbank = [
                                  {"Titel": "Python lernen", "Autor": "Max Mustermann", "Jahr": 2020},
                                  {"Titel": "Fortgeschrittene Python-Programmierung", "Autor": "Erika Musterfrau", "Jahr": 2021},
                                  {"Titel": "Python lernen", "Autor": "John Doe", "Jahr": 2019}
                                 ]
Task (EN): You work for a company that develops software for managing libraries. Your task is to write a Python program that
           offers the following functionalities:
           a) Book search: A function search_book(title, author=None), which searches for books by title and optionally by author.
           The function returns a list of books that match the search criteria. If no author is specified, all books with the corresponding
           title are returned.
           b) Add book: A function add_book(title, author, year), which adds a new book to the library database. The database is
           represented as a list of dictionaries, where each dictionary represents a book.
           c) Filter books by year: A function books_by_year(year), which returns all books that were published in a specific year.
           Use the filter() function to accomplish this task.
           d) Display the library database: A function show_database(), which displays the current content of the library database
           in a formatted output. Each entry should contain the following information: Title, Author, Year of publication.
           e) Interactive menu: Implement an interactive menu that allows the user to execute the above-mentioned functions.
           Use a while loop to display the menu continuously until the user decides to exit the program.
           Database structure (example):
           library_database = [
                               {"Title": "Learning Python", "Author": "Max Mustermann", "Year": 2020},
                               {"Title": "Advanced Python Programming", "Author": "Erika Musterfrau", "Year": 2021},
                               {"Title": "Learning Python", "Author": "John Doe", "Year": 2019}
                              ]
"""

library_database = [
    {"Title": "Learning Python", "Author": "Max Mustermann", "Year": 2020},
    {
        "Title": "Advanced Python Programming",
        "Author": "Erika Musterfrau",
        "Year": 2021,
    },
    {"Title": "Learning Python", "Author": "John Doe", "Year": 2019},
]


def search_book(title: str, author: str = None) -> list:
    """Search library_database for books matching the given title and optional author.

    Args:
        title (str): The title of the book to search for.
        author (str, optional): The author to filter by. Defaults to None.

    Returns:
        list: A list of dictionaries containing matching books.
    """
    matching_books = []
    for book in library_database:
        if book["Title"] == title:
            if author is None or book["Author"] == author:
                matching_books.append(
                    book
                )  # Add book if title matches and author (if provided) matches
    return matching_books


def add_book(title: str, author: str, year: int) -> dict:
    """Create a new book dictionary with the given details.

    Args:
        title (str): The title of the book.
        author (str): The author of the book.
        year (int): The publication year of the book.

    Returns:
        dict: A dictionary representing the new book.
    """
    adding_books = {"Title": title, "Author": author, "Year": year}
    return adding_books


def books_by_year(year: int) -> list:
    """Filter library_database to return books published in the specified year.

    Args:
        year (int): The publication year to filter by.

    Returns:
        list: A list of dictionaries containing books from the given year.
    """
    filtered_books = list(filter(lambda book: book["Year"] == year, library_database))
    return filtered_books


def show_database(data: list) -> None:
    """Display all books in the provided database list.

    Args:
        data (list): A list of book dictionaries to display.
    """
    for book in data:
        print(f"{book['Title']}, {book['Author']}, {book['Year']}")


while True:
    print("\nLibrary Management System")
    print("1. Search Book")
    print("2. Add Book")
    print("3. Show Books by Year")
    print("4. Show Database")
    print("5. Exit")
    choice = input("Enter your choice (1-5): ")

    if choice == "1":
        title = input("Enter book title: ")
        author = input("Enter author (press Enter to skip): ")
        if author == "":
            author = None  # Convert empty input to None for optional author filtering
        results = search_book(title, author)
        for book in results:
            print(f"Found: {book['Title']}, {book['Author']}, {book['Year']}")
        if not results:
            print("No books found.")

    elif choice == "2":
        title = input("Enter book title: ")
        author = input("Enter author: ")
        try:
            year = int(input("Enter publication year: "))
        except ValueError:
            print("Invalid year. Please enter a number.")
            continue  # Skip to next iteration on invalid input
        new_book = add_book(title, author, year)
        library_database.append(new_book)
        print("Book added successfully!")

    elif choice == "3":
        year = int(input("Enter year: "))
        results = books_by_year(year)
        for book in results:
            print(f"Found: {book['Title']}, {book['Author']}, {book['Year']}")
        if not results:
            print("No books found for that year.")

    elif choice == "4":
        show_database(library_database)

    elif choice == "5":
        print("Exiting program.")
        break

    else:
        print("Invalid choice, please try again (1-5).")
