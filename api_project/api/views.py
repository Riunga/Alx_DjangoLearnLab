from rest_framework import generics, viewsets, permissions
from .models import Book
from .serializers import BookSerializer
from .permissions import IsAdminOrReadOnly

class BookViewSet(viewsets.ModelViewSet):
    queryset = Book.objects.all()
    serializer_class = BookSerializer
    permission_classes = [IsAdminOrReadOnly]

from rest_framework import generics, viewsets, permissions
from .models import Book
from .serializers import BookSerializer
from .permissions import IsAdminOrReadOnly
from django_filters import rest_framework as filters
from rest_framework import generics, filters as rest_framework_filters
from django_filters.rest_framework import DjangoFilterBackend

class BookListView(generics.ListAPIView):
    queryset = Book.objects.all()
    serializer_class = BookSerializer

    # Add filtering, searching, and ordering backends
    filter_backends = [DjangoFilterBackend, rest_framework_filters.SearchFilter, rest_framework_filters.OrderingFilter]

    # Specify which fields can be filtered
    filterset_fields = ['title', 'author__name', 'publication_year']

    # Specify fields to search
    search_fields = ['title', 'author__name']

    # Specify fields for ordering
    ordering_fields = ['title', 'publication_year']

    # Set the default ordering
    ordering = ['title']

class BookDetailView(generics.RetrieveAPIView):
    queryset = Book.objects.all()
    serializer_class = BookSerializer

class BookCreateView(generics.CreateAPIView):
    queryset = Book.objects.all()
    serializer_class = BookSerializer

class BookUpdateView(generics.UpdateAPIView):
    queryset = Book.objects.all()
    serializer_class = BookSerializer

class BookDeleteView(generics.DestroyAPIView):
    queryset = Book.objects.all()
    serializer_class = BookSerializer