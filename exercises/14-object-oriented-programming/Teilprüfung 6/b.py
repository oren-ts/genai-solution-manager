"""
Teilprüfung 6
Task (DE): Entwickle ein Python-Programm, das eine einfache Simulation eines Online-Buchladens durchführt.
           Der Buchladen soll Bücher in verschiedenen Kategorien (z.B. Roman, Sachbuch, Wissenschaft) führen.
           Jedes Buch hat einen Titel, einen Autor, eine Kategorie und einen Preis. Nutze deine Kenntnisse in
           objektorientierter Programmierung, um Klassen für Bücher und den Buchladen zu definieren.
           Implementiere zudem Funktionen für das Hinzufügen von Büchern, das Durchsuchen nach Kategorien und
           das Berechnen des Gesamtpreises für eine Auswahl von Büchern. Berücksichtige dabei folgende Anforderungen:
           a) Definiere eine Klasse Buch mit den Attributen titel, autor, kategorie und preis. Implementiere
           eine __init__-Methode, die diese Attribute initialisiert, und eine __str__-Methode, die eine
           repräsentative Zeichenkette für das Buchobjekt zurückgibt.
           b) Definiere eine Klasse Buchladen mit einem Attribut inventar, das eine Liste von Buchobjekten speichert.
           Implementiere Methoden für das Hinzufügen eines Buches zum Inventar, das Durchsuchen des Inventars nach
           Kategorie und das Berechnen des Gesamtpreises einer Buchauswahl.
           c) Erstelle ein paar Buchobjekte und füge sie zum Inventar des Buchladens hinzu. Teste anschließend die
           Funktionalitäten des Buchladens, indem du Bücher nach Kategorie durchsuchst und den Gesamtpreis für eine
           Auswahl von Büchern berechnest.
Task (EN): Develop a Python program that performs a simple simulation of an online bookstore. The bookstore should
           offer books in different categories (e.g., novel, non-fiction, science). Each book has a title, an author,
           a category, and a price. Use your knowledge of object-oriented programming to define classes for Book and Bookstore.
           Also implement functions to: add books, search by category, calculate the total price of a selection of books. Requirements:
           a) Define a class Book with the attributes title, author, category, and price. Implement an __init__ method that
           initializes these attributes, and a __str__ method that returns a representative string for the Book object.
           b) Define a class Bookstore with an attribute inventory, which stores a list of Book objects. Implement methods for:
           adding a book to the inventory, searching the inventory by category, calculating the total price of a selection of books.
           c) Create a few Book objects and add them to the bookstore's inventory. Then test the bookstore's functionalities by
           searching for books by category and calculating the total price of a selection of books.
"""


class Book:
    """Represents a book with title, author, category, and price."""

    def __init__(self, title, author, category, price):
        self.title = title
        self.author = author
        self.category = category
        self.price = price

    def __str__(self):
        return f"{self.title} by {self.author} ({self.category}) - €{self.price:.2f}"


class BookStore:
    """Represents a bookstore that manages an inventory of books."""

    def __init__(self):
        self.inventory = []

    def add_book(self, book):
        """Add a book to the inventory."""
        self.inventory.append(book)

    def search_category(self, category):
        """Search for all books in a specific category."""
        return [book for book in self.inventory if book.category == category]

    def calculate_price(self, books):
        """Calculate the total price of a list of books."""
        return sum(book.price for book in books)

    def show_books_by_category(self, category):
        """Display all books in a specific category."""
        books = self.search_category(category)
        if books:
            print(f"\n=== {category} Books ===")
            for book in books:
                print(book)
            return books
        else:
            print(f"\nNo books found in category: {category}")
            return []

    def show_all_books(self):
        """Display all books in the inventory."""
        print("\n=== All Books in Inventory ===")
        for book in self.inventory:
            print(book)


def main():
    """Main function to demonstrate the bookstore functionality."""
    # Create book objects
    books_data = [
        ("The Clockmaker's Paradox", "Amelia Roth", "Novel", 14.90),
        ("A Quiet Theory of Rain", "Jasper Lin", "Poetry", 11.50),
        ("Designing Tomorrow", "Mira Kessler", "Non-fiction", 22.30),
        ("Echoes of the Cedar Forest", "Daniel Arendt", "Novel", 9.80),
        ("The Invisible Ingredient", "Sofia Marek", "Non-fiction", 18.20),
        ("1984", "George Orwell", "Novel", 15.99),
    ]

    # Create bookstore and add books
    inventory = BookStore()
    for title, author, category, price in books_data:
        book = Book(title, author, category, price)
        inventory.add_book(book)

    # Display all books
    inventory.show_all_books()

    # Search and display books by category
    novels = inventory.show_books_by_category("Novel")

    # Calculate and display total price of novels
    total_price = inventory.calculate_price(novels)
    print(f"\nThe total price of all novels is: €{total_price:.2f}")


if __name__ == "__main__":
    main()
