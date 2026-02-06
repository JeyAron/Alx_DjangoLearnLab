from relationship_app.models import Author, Book, Library, Librarian

# ------------------------
# Sample Data Creation
# ------------------------
# Creating author
author, created = Author.objects.get_or_create(name="George Orwell")

# Creating books
book1, _ = Book.objects.get_or_create(title="1984", author=author)
book2, _ = Book.objects.get_or_create(title="Animal Farm", author=author)

# Creating library
library, _ = Library.objects.get_or_create(name="Central Library")
library.books.add(book1, book2)

# Creating librarian
librarian, _ = Librarian.objects.get_or_create(name="Alice", library=library)

# ------------------------
# Queries
# ------------------------

# 1
books_by_author = author.books.all()
print("Books by", author.name)
for book in books_by_author:
    print("-", book.title)

# 2
print("\nBooks in", library.name)
for book in library.books.all():
    print("-", book.title)

# 3
print("\nLibrarian of", library.name, "is", library.librarian.name)
