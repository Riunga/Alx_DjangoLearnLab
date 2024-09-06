from datetime import timezone
from django.shortcuts import render

# Create your views here.
from rest_framework import generics
from .models import Book
from .serializers import BookSerializer

class BookList(generics.ListAPIView):
    queryset = Book.objects.all()  # Fetch all book records
    serializer_class = BookSerializer  # Use the BookSerializer to format the data

from rest_framework import viewsets
from .models import Book
from .serializers import BookSerializer

class BookViewSet(viewsets.ModelViewSet):
    queryset = Book.objects.all()
    serializer_class = BookSerializer

from rest_framework.permissions import IsAuthenticated
from rest_framework import viewsets
from .models import Book
from .serializers import BookSerializer

class BookViewSet(viewsets.ModelViewSet):
    queryset = Book.objects.all()
    serializer_class = BookSerializer
    permission_classes = [IsAuthenticated]  # Only authenticated users can access

from rest_framework import viewsets
from .models import Book
from .serializers import BookSerializer
from .permissions import IsAdminOrReadOnly  # Import your custom permission

class BookViewSet(viewsets.ModelViewSet):
    queryset = Book.objects.all()
    serializer_class = BookSerializer
    permission_classes = [IsAdminOrReadOnly]  # Apply the custom permission

from rest_framework import generics
from .models import Book
from .serializers import BookSerializer
from rest_framework.permissions import IsAuthenticatedOrReadOnly, IsAuthenticated

# ListAPIView for retrieving all books
class BookListView(generics.ListView):
    queryset = Book.objects.all()
    serializer_class = BookSerializer
    permission_classes = [IsAuthenticatedOrReadOnly]  # Read access for unauthenticated users

# RetrieveAPIView for retrieving a single book by ID
class BookDetailView(generics.DetailView):
    queryset = Book.objects.all()
    serializer_class = BookSerializer
    permission_classes = [IsAuthenticatedOrReadOnly]

# CreateAPIView for adding a new book
class BookCreateView(generics.CreateView):
    queryset = Book.objects.all()
    serializer_class = BookSerializer
    permission_classes = [IsAuthenticated]  # Only authenticated users can create a book

# UpdateAPIView for modifying an existing book
class BookUpdateView(generics.UpdateView):
    queryset = Book.objects.all()
    serializer_class = BookSerializer
    permission_classes = [IsAuthenticated]  # Only authenticated users can update a book

# DestroyAPIView for removing a book
class BookDeleteView(generics.DeleteView):
    queryset = Book.objects.all()
    serializer_class = BookSerializer
    permission_classes = [IsAuthenticated]  # Only authenticated users can delete a book