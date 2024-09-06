from rest_framework import generics, viewsets, permissions
from .models import Book
from .serializers import BookSerializer
from .permissions import IsAdminOrReadOnly

class BookViewSet(viewsets.ModelViewSet):
    queryset = Book.objects.all()
    serializer_class = BookSerializer
    permission_classes = [IsAdminOrReadOnly]

from rest_framework import generics, filters
from django_filters.rest_framework import DjangoFilterBackend
from .models import Book
from .serializers import BookSerializer

class BookListView(generics.ListAPIView):
    queryset = Book.objects.all()
    serializer_class = BookSerializer

    # Add filtering, searching, and ordering backends
    filter_backends = [DjangoFilterBackend, filters.SearchFilter, filters.OrderingFilter]

    # Specify which fields can be filtered
    filterset_fields = ['title', 'author__name', 'publication_year']  # author__name to filter by author's name

    # Specify fields to search
    search_fields = ['title', 'author__name']

    # Specify fields for ordering
    ordering_fields = ['title', 'publication_year']

    # Set the default ordering
    ordering = ['title']
