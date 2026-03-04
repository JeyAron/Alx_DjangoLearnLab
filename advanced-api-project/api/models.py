from django.db import models

# Create your models here.

class Author(models.Model):
    """
    Author model represents a book author.

    Fields:
    - name: Stores the full name of the author.

    Relationship:
    - An Author can have multiple Books (one-to-many relationship).
    """
    name = models.CharField(max_length=255)

    def __str__(self):
        return self.name


class Book(models.Model):
    """
    Book model represents a book written by an Author.

    Fields:
    - title: The title of the book.
    - publication_year: The year the book was published.
    - author: ForeignKey linking the book to an Author.

    Relationship:
    - Each Book belongs to one Author.
    - If an Author is deleted, their Books are also deleted (CASCADE).
    """
    title = models.CharField(max_length=255)
    publication_year = models.IntegerField()
    author = models.ForeignKey(
        Author,
        on_delete=models.CASCADE,
        related_name='books'
    )

    def __str__(self):
        return self.title
