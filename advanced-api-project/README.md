# Generic API Views Configuration

This project uses Django REST Framework generic views to handle CRUD operations for the Book model.

Views Implemented:

- BookListView (ListAPIView)
- BookDetailView (RetrieveAPIView)
- BookCreateView (CreateAPIView)
- BookUpdateView (UpdateAPIView)
- BookDeleteView (DestroyAPIView)

Permissions:

- List and Detail views allow read-only access to all users.
- Create, Update, and Delete views require authentication.

Custom Behavior:

- Publication year validation ensures books cannot be created with a future year.
- Validation is handled inside BookSerializer.

Endpoints:

GET     /api/books/
GET     /api/books/<id>/
POST    /api/books/create/
PUT     /api/books/<id>/update/
DELETE  /api/books/<id>/delete/

# Advanced Query Capabilities

This API supports:

1. Filtering
   - ?title=
   - ?publication_year=
   - ?author=

2. Search
   - ?search=<keyword>
   Searches title and author name.

3. Ordering
   - ?ordering=title
   - ?ordering=-publication_year

Filtering backend:
- DjangoFilterBackend
- SearchFilter
- OrderingFilter

