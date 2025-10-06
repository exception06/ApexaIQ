from Library import Library
class Members:
    """
    Represents a member of the lib who can borrow and return books.

    Attributes:
        name (str): The name of the member.
        borrowed_books (list): A list of Book objects currently borrowed by the member.

    Methods:
        borrow_book(book): Borrows a book if it is available.
        return_book(book): Returns a book if it was previously borrowed by the member.
    """
    def __init__(self, name: str):
        self.name = name
        self.borrowed_books = []
        
    def borrow_book(self, book_name: str, lib: Library) -> None:
        for book in lib.books:
            if book.title.strip().lower() == book_name.strip().lower():  # safer comparison
                lib.books.remove(book)
                self.borrowed_books.append(book)
                print(f"{self.name} borrowed '{book_name}'")
                return
        print(f"Sorry, '{book_name}' is not available in the library.")

    def return_book(self, book_name: str, lib: Library) -> None:
        for book in self.borrowed_books:
            if book.title.strip().lower() == book_name.strip().lower():
                self.borrowed_books.remove(book)
                lib.books.append(book)
                print(f"{self.name} returned '{book_name}'")
                return
        print(f"{self.name} did not borrow '{book_name}'")

