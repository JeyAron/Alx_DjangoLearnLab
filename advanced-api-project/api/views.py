from django.shortcuts import render

# Create your views here.
from rest_framework import generics
from rest_framework.permissions import IsAuthenticatedOrReadOnly, IsAuthenticated
from django_filters import rest_framework
from rest_framework.filters import SearchFilter, OrderingFilter
from .models import Book
from .serializers import BookSerializer
import datetime


class BookListView(generics.ListAPIView):
    """
    GET /books/
    Returns a list of all books.

    Advanced Features:
    - Filtering by title, author, publication_year
    - Searching by title and author name
    - Ordering by title and publication_year

    Permissions:
    - Read-only access for everyone.
    """
    queryset = Book.objects.all()
    serializer_class = BookSerializer
    permission_classes = [IsAuthenticatedOrReadOnly]

    filter_backends = [DjangoFilterBackend, SearchFilter, OrderingFilter]
    filterset_fields = ['title', 'publication_year', 'author']

    search_fields = ['title', 'author__name']

    ordering_fields = ['title', 'publication_year']
    ordering = ['title']

class BookDetailView(generics.RetrieveAPIView):
    """
    GET /books/<pk>/
    Returns details of a single book by ID.

    Permissions:
    - Read-only access for everyone.
    """
    queryset = Book.objects.all()
    serializer_class = BookSerializer
    permission_classes = [IsAuthenticatedOrReadOnly]


class BookCreateView(generics.CreateAPIView):
    """
    POST /books/create/
    Creates a new book.

    Permissions:
    - Only authenticated users can create books.
    """
    queryset = Book.objects.all()
    serializer_class = BookSerializer
    permission_classes = [IsAuthenticated]


class BookUpdateView(generics.UpdateAPIView):
    """
    PUT /books/<pk>/update/
    Updates an existing book.

    Permissions:
    - Only authenticated users can update books.
    """
    queryset = Book.objects.all()
    serializer_class = BookSerializer
    permission_classes = [IsAuthenticated]


class BookDeleteView(generics.DestroyAPIView):
    """
    DELETE /books/<pk>/delete/
    Deletes a book.

    Permissions:
    - Only authenticated users can delete books.
    """
    queryset = Book.objects.all()
    serializer_class = BookSerializer
    permission_classes = [IsAuthenticated]
