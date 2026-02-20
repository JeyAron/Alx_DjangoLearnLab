from django.urls import reverse
from rest_framework import status
from rest_framework.test import APITestCase
from django.contrib.auth.models import User
from .models import Author, Book


class BookAPITestCase(APITestCase):
    """
    Test suite for Book API endpoints.

    Tests:
    - CRUD operations
    - Filtering
    - Searching
    - Ordering
    - Permission enforcement
    """

    def setUp(self):
        """
        Create test user, author, and book instances.
        """
        self.user = User.objects.create_user(
            username="testuser",
            password="testpassword"
        )

        self.author = Author.objects.create(name="Chinua Achebe")

        self.book = Book.objects.create(
            title="Things Fall Apart",
            publication_year=1958,
            author=self.author
        )

        self.list_url = reverse("book-list")
        self.create_url = reverse("book-create")
        self.detail_url = reverse("book-detail", args=[self.book.id])
        self.update_url = reverse("book-update", args=[self.book.id])
        self.delete_url = reverse("book-delete", args=[self.book.id])

    # -------------------------
    # READ TESTS
    # -------------------------

    def test_list_books(self):
        """Test retrieving book list (public access allowed)."""
        response = self.client.get(self.list_url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data), 1)

    def test_retrieve_single_book(self):
        """Test retrieving a single book."""
        response = self.client.get(self.detail_url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data["title"], "Things Fall Apart")

    # -------------------------
    # CREATE TEST
    # -------------------------

    def test_create_book_authenticated(self):
        """Authenticated users can create books."""
        self.client.login(username="testuser", password="testpassword")

        data = {
            "title": "New Book",
            "publication_year": 2000,
            "author": self.author.id
        }

        response = self.client.post(self.create_url, data)
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(Book.objects.count(), 2)

    def test_create_book_unauthenticated(self):
        """Unauthenticated users cannot create books."""
        data = {
            "title": "Unauthorized Book",
            "publication_year": 2001,
            "author": self.author.id
        }

        response = self.client.post(self.create_url, data)
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)

    # -------------------------
    # UPDATE TEST
    # -------------------------

    def test_update_book(self):
        """Authenticated users can update books."""
        self.client.login(username="testuser", password="testpassword")

        data = {
            "title": "Updated Title",
            "publication_year": 1958,
            "author": self.author.id
        }

        response = self.client.put(self.update_url, data)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.book.refresh_from_db()
        self.assertEqual(self.book.title, "Updated Title")

    # -------------------------
    # DELETE TEST
    # -------------------------

    def test_delete_book(self):
        """Authenticated users can delete books."""
        self.client.login(username="testuser", password="testpassword")

        response = self.client.delete(self.delete_url)
        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)
        self.assertEqual(Book.objects.count(), 0)

    # -------------------------
    # FILTER TEST
    # -------------------------

    def test_filter_books_by_year(self):
        """Test filtering books by publication year."""
        response = self.client.get(self.list_url + "?publication_year=1958")
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data), 1)

    # -------------------------
    # SEARCH TEST
    # -------------------------

    def test_search_books(self):
        """Test searching books by title."""
        response = self.client.get(self.list_url + "?search=Things")
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data), 1)

    # -------------------------
    # ORDERING TEST
    # -------------------------

    def test_order_books(self):
        """Test ordering books by title."""
        Book.objects.create(
            title="Another Book",
            publication_year=2005,
            author=self.author
        )

        response = self.client.get(self.list_url + "?ordering=title")
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data[0]["title"], "Another Book")
