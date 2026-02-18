from django.shortcuts import render

# Create your views here.
from django.shortcuts import render, get_object_or_404, redirect
from django.contrib.auth.decorators import permission_required, login_required
from .models import Book

"""
PERMISSIONS & GROUP SETUP GUIDE

Custom Permissions Defined in Book Model:
- can_view
- can_create
- can_edit
- can_delete

Groups Created:
1. Viewers:
   - can_view

2. Editors:
   - can_view
   - can_create
   - can_edit

3. Admins:
   - can_view
   - can_create
   - can_edit
   - can_delete

Views are protected using Django's @permission_required decorator.
If a user lacks permission, a 403 error is raised.
"""

@login_required
@permission_required("bookshelf.can_view", raise_exception=True)
def book_list(request):
    books = Book.objects.all()
    return render(request, "bookshelf/book_list.html", {"books": books})


@login_required
@permission_required("bookshelf.can_create", raise_exception=True)
def create_book(request):
    if request.method == "POST":
        title = request.POST.get("title")
        author = request.POST.get("author")
        Book.objects.create(title=title, author=author)
        return redirect("book_list")

    return render(request, "bookshelf/create_book.html")


@login_required
@permission_required("bookshelf.can_edit", raise_exception=True)
def edit_book(request, pk):
    book = get_object_or_404(Book, pk=pk)

    if request.method == "POST":
        book.title = request.POST.get("title")
        book.author = request.POST.get("author")
        book.save()
        return redirect("book_list")

    return render(request, "bookshelf/edit_book.html", {"book": book})


@login_required
@permission_required("bookshelf.can_delete", raise_exception=True)
def delete_book(request, pk):
    book = get_object_or_404(Book, pk=pk)
    book.delete()
    return redirect("book_list")
