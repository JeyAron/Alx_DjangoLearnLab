from relationship_app.models import Author, Book, Library, Librarian

# Required variables
author_name = "George Orwell"
library_name = "Central Library"

# Create sample data
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
# REQUIRED QUERY PATTERNS
# ------------------------

# 1. Query all books by a specific author (ForeignKey)
books_by_author = Book.objects.filter(author=author)

# 2. List all books in a library (ManyToMany)
library = Library.objects.get(name=library_name)
books_in_library = library.books.all()

# 3. Retrieve the librarian for a library (OneToOne)
librarian = Librarian.objects.get(library=library)
