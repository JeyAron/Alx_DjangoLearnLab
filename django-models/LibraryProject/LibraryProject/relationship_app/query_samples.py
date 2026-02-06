from relationship_app.models import Author, Book, Library, Librarian

# ------------------------
# Sample Data Creation
# ------------------------

author_name = "George Orwell"
library_name = "Central Library"

author, _ = Author.objects.get_or_create(name=author_name)

book1, _ = Book.objects.get_or_create(title="1984", author=author)
book2, _ = Book.objects.get_or_create(title="Animal Farm", author=author)

library, _ = Library.objects.get_or_create(name=library_name)
library.books.add(book1, book2)

librarian, _ = Librarian.objects.get_or_create(
    name="Alice",
    library=library
)

# ------------------------
# Queries
# ------------------------

# 1. Querying all books by a specific author
books_by_author = Book.objects.filter(author=author)
for book in books_by_author:
    print(book.title)

# 2. Listing all books in a library
library = Library.objects.get(name=library_name)
for book in library.books.all():
    print(book.title)

# 3. Retrieving the librarian for a library
librarian = Librarian.objects.get(library=library)
print(librarian.name)
