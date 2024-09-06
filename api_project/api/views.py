from rest_framework import generics, viewsets, permissions
from .models import Book
from .serializers import BookSerializer
from .permissions import IsAdminOrReadOnly

class BookViewSet(viewsets.ModelViewSet):
    queryset = Book.objects.all()
    serializer_class = BookSerializer
    permission_classes = [IsAdminOrReadOnly]

# Ensure these imports are included
from django_filters import rest_framework as filters
from rest_framework import generics, filters as rest_framework_filters
from django_filters.rest_framework import DjangoFilterBackend
from .models import Book
from .serializers import BookSerializer

# Assign DRF views to variables named as requested
ListView = generics.ListAPIView
DetailView = generics.RetrieveAPIView
CreateView = generics.CreateAPIView
UpdateView = generics.UpdateAPIView
DeleteView = generics.DestroyAPIView

# Define views using the variables
class BookListView(ListView):
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

class BookDetailView(DetailView):
    queryset = Book.objects.all()
    serializer_class = BookSerializer

class BookCreateView(CreateView):
    queryset = Book.objects.all()
    serializer_class = BookSerializer

class BookUpdateView(UpdateView):
    queryset = Book.objects.all()
    serializer_class = BookSerializer

class BookDeleteView(DeleteView):
    queryset = Book.objects.all()
    serializer_class = BookSerializer
