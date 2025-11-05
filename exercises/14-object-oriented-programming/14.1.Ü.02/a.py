"""
Übung 14.1.Ü.02
Task (DE):
Task (EN): Develop a Python class named Book, which is used to manage a small library.
           The class should have the following attributes and methods:
           a) The class should have three attributes: title (string), author (string), and checked_out
           (boolean), where checked_out is set to False by default.
           b) Write an initialization method __init__ that receives title and author as parameters and
           assigns them along with the default value for checked_out.
           c) Add a method borrow that sets the attribute checked_out to True if the book is not already
           checked out. If the book is already checked out, a message "Book already checked out" should be displayed.
           d) Add a method return_book that sets the attribute checked_out to False if the book was checked out.
           If the book is not checked out, a message "Book was not checked out" should be displayed.
           e) Write a method status that outputs the title, author, and the loan status of the book in a sentence.
"""


class Book:
    """A class representing a book in a small library system.

    Attributes:
        title (str): The title of the book.
        author (str): The author of the book.
        checked_out (bool): Indicates if the book is currently checked out (default: False).
    """

    def __init__(self, title, author):
        """Initialize a Book instance with title and author.

        Args:
            title (str): The title of the book.
            author (str): The author of the book.
        """
        self.title = title
        self.author = author
        self.checked_out = False

    def borrow(self):
        """Borrow the book if it's available.

        If the book is already checked out, print a message instead.
        """
        if not self.checked_out:
            self.checked_out = True
        else:
            print("Book already checked out.")

    def return_book(self):
        """Return the book if it's checked out.

        If the book is not checked out, print a message instead.
        """
        if self.checked_out:
            self.checked_out = False
        else:
            print("Book was not checked out")

    def status(self):
        """Print the book's title, author, and loan status."""
        if self.checked_out:
            text = "Not available"
        else:
            text = "Available"
        print(f"Title: {self.title}\nAuthor: {self.author}\nLoan Status: {text}")


if __name__ == "__main__":
    bk1 = Book(
        "The Clockmaker of Hollow Glen", "Elara Finnwick"
    )  # Create bk1 with checked_out set to False
    bk2 = Book("Saffron Skies Over Naharim", "Darius Kelmoran")
    bk1.borrow()  # Set checked_out to True
    bk1.borrow()  # Should print: "Book already checked out."
    bk1.status()  # Should show Loan Status: Not available
    bk1.return_book()  # Set checked_out to False
    bk1.return_book()  # Should print: "Book was not checked out"
    bk1.status()  # Should show Loan Status: Available
