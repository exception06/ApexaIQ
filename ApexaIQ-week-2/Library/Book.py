class Book:
    """Represents a single book in the lib system.

    Attributes:
        title (str): The title of the book.

    Methods:
        __repr__():
            Returns a string representation of the book with its title, author, 
            and availability status.
    """
    def __init__(self, title: str):
        self.title = title

    def __repr__(self) -> str:
        return self.title