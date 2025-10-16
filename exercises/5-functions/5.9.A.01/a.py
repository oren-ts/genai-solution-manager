"""
Transfer 5.9.A.01
Task (DE): Entwickle ein Python-Programm, das folgende Funktionen umfasst:
           a) Eine Funktion buch_daten_speichern, die als Parameter den Titel eines Buches (String),
           den Namen des Autors (String), das Veröffentlichungsjahr (Integer), und optional die Anzahl
           der Seiten (Integer, Defaultwert 0) erhält. Die Funktion soll alle diese Daten in einem Dictionary
           speichern, wobei die Schlüssel titel, autor, jahr, und seiten sind. Die Funktion gibt dieses Dictionary zurück.
           b) Eine Funktion buecher_sammlung, die eine Liste von Bücher-Dictionaries (erstellt von buch_daten_speichern)
           als Parameter erhält und die Gesamtanzahl der Seiten aller Bücher in der Liste berechnet. Die Funktion gibt die Gesamtseitenzahl zurück.
           c) Verwende eine Schleife, um den Benutzer zur Eingabe von Daten für drei verschiedene Bücher aufzufordern.
           Nutze dabei die Funktion buch_daten_speichern für jedes Buch und speichere jedes resultierende Dictionary in einer Liste.
           d) Nachdem alle Bücher eingegeben wurden, rufe die Funktion buecher_sammlung mit der Liste der Bücher-Dictionaries
           als Argument auf, um die Gesamtanzahl der Seiten aller Bücher zu berechnen.
           e) Gib die Gesamtanzahl der Seiten aller Bücher aus.
Task (EN): Develop a Python program that includes the following functions:
           a) A function save_book_data that takes as parameters the title of a book (string), the authors name (string),
           the year of publication (integer), and optionally the number of pages (integer, default value 0).
           The function should store all this data in a dictionary, using the keys title, author, year, and pages.
           The function should return this dictionary.
           b) A function book_collection that takes a list of book dictionaries (created by save_book_data)
           as a parameter and calculates the total number of pages of all books in the list.
           The function should return the total number of pages.
           c) Use a loop to prompt the user to enter data for three different books.
           For each book, use the save_book_data function and store each resulting dictionary in a list.
           d) After all books have been entered, call the book_collection function with the list of book dictionaries
           as an argument to calculate the total number of pages of all books.
           e) Output the total number of pages of all books.
"""

# This list will hold the three (validated) book dictionaries
books_list = []


def save_book_data(title: str, author: str, year: int, pages: int = 0) -> dict:
    """
    Create and return one standardized book record.

    Parameters:
        title  (str): non-empty after stripping spaces
        author (str): non-empty after stripping spaces
        year   (int): whole number > 0
        pages  (int): whole number >= 0 (defaults to 0 if not provided)
    """
    book_data = {
        "title": title,
        "author": author,
        "year": year,
        "pages": pages,
    }
    return book_data


def book_collection(books) -> int:
    """
    Return the total number of pages across all books in the list.

    Parameters:
        books (list[dict]): each dict has keys title, author, year, pages

    Returns:
        int: sum of the 'pages' field for every book
    """
    total_pages = sum(x["pages"] for x in books)
    return total_pages


# Outer loop: we need exactly 3 valid books
for i in range(3):
    # ----- TITLE (retry until non-empty) -----
    while True:
        book_title = input("Enter book title: ").strip()
        if book_title == "":
            print("Title is required")
            continue  # ask for title again
        break  # title is valid

    # ----- AUTHOR (retry until non-empty) -----
    while True:
        book_author = input("Enter book author: ").strip()
        if book_author == "":
            print("Author is required")
            continue  # ask for author again
        break  # author is valid

    # ----- YEAR (retry until integer > 0) -----
    while True:
        raw = input("Enter book publish year: ").strip()
        try:
            year = int(raw)  # this can raise ValueError if not a number
        except ValueError:
            print("Invalid year. Enter a whole number (e.g., 2020) greater than 0.")
            continue  # ask for year again

        if year <= 0:
            print("Invalid year. Enter a whole number (e.g., 2020) greater than 0.")
            continue  # ask for year again
        # valid numeric year

        # valid numeric year
        book_year = year
        break
    # pages

    # ----- PAGES (optional; blank -> 0; else integer >= 0) -----
    while True:
        raw = input("Enter book number of pages: ").strip()
        # If user presses Enter, pages defaults to 0
        if raw != "":
            book_pages = 0
            break
        # If user typed something, it must be an integer >= 0
        try:
            pages = int(raw)
        except ValueError:
            print(
                "Invalid page numbers. Enter a whole number (e.g., 358) greater than 0."
            )
            continue  # ask for pages again
        if pages < 0:
            print(
                "Invalid page numbers. Enter a whole number (e.g., 358) greater than 0."
            )
            continue  # ask for pages again
        # valid numeric pages
        book_pages = pages
        break

    # Build one book dictionary and append to the list
    books_temp = save_book_data(book_title, book_author, book_year, book_pages)
    books_list.append(books_temp)

# After collecting 3 books, compute the total pages and print
show_pages = book_collection(books_list)
print(f"The total number of pages of all books is: {show_pages}")
