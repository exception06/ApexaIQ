from Library import Library
from Book import Book
from Members import Members
# Create lib and books
lib = Library()
b1 = Book("Harry Potter")
b2 = Book("1980")
b3 = Book("Ikigai")

lib.add_book(b1)
lib.add_book(b2)
lib.add_book(b3)

lib.show_available_books()

# Create a member
member1 = Members("Ravi")

# Borrow books
member1.borrow_book("Harry Potter", lib)
member1.borrow_book("1980", lib)
member1.borrow_book("Gulliver's Adventures", lib)

lib.show_available_books()  # Only Ikigai left

# Return a book
member1.return_book("1980", lib)
member1.return_book("Atomic Habits", lib)

lib.show_available_books()  # Ikigai and 1980 are back

#persons info about the books borrowed
