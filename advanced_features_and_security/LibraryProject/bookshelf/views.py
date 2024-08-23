from django.shortcuts import render

# Create your views here.
from django.shortcuts import render, redirect
from django.contrib.auth.decorators import permission_required
from .models import Book
from .forms import BookForm

@permission_required('bookshelf.can_add_book')
def add_book(request):
    if request.method == 'POST':
        form = BookForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('book_list')  # Redirect to a view that lists books
    else:
        form = BookForm()
    return render(request, 'bookshelf/add_book.html', {'form': form})

from django.shortcuts import get_object_or_404
from django.contrib.auth.decorators import permission_required
from .models import Book

@permission_required('bookshelf.can_delete_book')
def delete_book(request, book_id):
    book = get_object_or_404(Book, pk=book_id)
    if request.method == 'POST':
        book.delete()
        return redirect('book_list')  # Redirect to a view that lists books
    return render(request, 'bookshelf/delete_book.html', {'book': book})

# bookshelf/views.py

from django.shortcuts import render, get_object_or_404
from django.contrib.auth.decorators import permission_required
from bookshelf.models import Book

@permission_required('bookshelf.can_view', raise_exception=True)
def view_book(request, book_id):
    book = get_object_or_404(Book, id=book_id)
    return render(request, 'bookshelf/view_book.html', {'book': book})

@permission_required('bookshelf.can_create', raise_exception=True)
def create_book(request):
    # Your code for creating a book
    pass

@permission_required('bookshelf.can_edit', raise_exception=True)
def edit_book(request, book_id):
    book = get_object_or_404(Book, id=book_id)
    # Your code for editing the book
    pass

@permission_required('bookshelf.can_delete', raise_exception=True)
def delete_book(request, book_id):
    book = get_object_or_404(Book, id=book_id)
    # Your code for deleting the book
    pass

# bookshelf/views.py

from django.shortcuts import render, get_object_or_404
from django.contrib.auth.decorators import permission_required
from bookshelf.models import Book

@permission_required('bookshelf.can_view', raise_exception=True)
def view_book(request, book_id):
    book = get_object_or_404(Book, id=book_id)
    return render(request, 'bookshelf/view_book.html', {'book': book})

@permission_required('bookshelf.can_create', raise_exception=True)
def create_book(request):
    # Your code for creating a book
    pass

@permission_required('bookshelf.can_edit', raise_exception=True)
def edit_book(request, book_id):
    book = get_object_or_404(Book, id=book_id)
    # Your code for editing the book
    pass

@permission_required('bookshelf.can_delete', raise_exception=True)
def delete_book(request, book_id):
    book = get_object_or_404(Book, id=book_id)
    # Your code for deleting the book
    pass

# Use Django ORM (safe):
books = Book.objects.filter(title=title)

from django.shortcuts import render
from .forms import ExampleForm

def example_view(request):
    if request.method == 'POST':
        form = ExampleForm(request.POST)
        if form.is_valid():
            # Process the form data
            name = form.cleaned_data['name']
            email = form.cleaned_data['email']
            # Do something with the data
    else:
        form = ExampleForm()
    return render(request, 'bookshelf/form_example.html', {'form': form})

from django.shortcuts import render
from .models import Book

def book_list_view(request):
    books = Book.objects.all()  # Retrieve all books from the database
    return render(request, 'bookshelf/book_list.html', {'books': books})
