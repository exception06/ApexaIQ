class Library:
    """
    Represents the lib system that manages books and member interactions.

    Attributes:
        books (list): A list of all Book objects in the lib.
        
    Methods:
        add_book(book): Adds a new book to the lib collection.
        show_available_books(): Displays all books that are currently available.
        show_borrowed_books(): Displays all books that are currently borrowed.
    """
    def __init__(self):
        self.books = []

    def add_book(self,added_book: str):
        self.books.append(added_book)
        print(f"The book {added_book} is added in the Library.")

    def show_available_books(self) -> list:
        if self.books:
            print(f"The available books are: {self.books}.")
        else:
            print("No books available in the lib.")




