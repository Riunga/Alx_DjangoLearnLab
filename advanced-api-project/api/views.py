from rest_framework.generics import ListAPIView
from .models import Book
from .serializers import BookSerializer

class BookListView(ListAPIView):
    queryset = Book.objects.all()
    serializer_class = BookSerializer 
    
from rest_framework.generics import RetrieveAPIView

class BookDetailView(RetrieveAPIView):
    queryset = Book.objects.all()
    serializer_class = BookSerializer

from rest_framework.generics import CreateAPIView

class BookCreateView(CreateAPIView):
    queryset = Book.objects.all()
    serializer_class = BookSerializer
    
from rest_framework.generics import UpdateAPIView

class BookUpdateView(UpdateAPIView):
    queryset = Book.objects.all()
    serializer_class = BookSerializer

from rest_framework.generics import DestroyAPIView

class BookDeleteView(DestroyAPIView):
    queryset = Book.objects.all()
    serializer_class = BookSerializer 
    
from rest_framework.generics import CreateAPIView
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework import status
from .models import Book
from .serializers import BookSerializer
from datetime import datetime

class BookCreateView(CreateAPIView):
    queryset = Book.objects.all()
    serializer_class = BookSerializer
    permission_classes = [IsAuthenticated]  
    def create(self, request, *args, **kwargs):
        data = request.data
        publication_year = data.get('publication_year')

        if publication_year and int(publication_year) > datetime.now().year:
            return Response(
                {"error": "Publication year cannot be in the future."},
                status=status.HTTP_400_BAD_REQUEST
            )

        return super().create(request, *args, **kwargs)

from rest_framework.generics import UpdateAPIView
from rest_framework.permissions import IsAuthenticated, IsAdminUser
from rest_framework.exceptions import PermissionDenied

class BookUpdateView(UpdateAPIView):
    queryset = Book.objects.all()
    serializer_class = BookSerializer
    permission_classes = [IsAuthenticated]  

    def update(self, request, *args, **kwargs):
        book = self.get_object()

        if request.user != book.author and not request.user.is_staff:
            raise PermissionDenied("You do not have permission to update this book.")
        
        return super().update(request, *args, **kwargs) 
    
from rest_framework.generics import ListAPIView
from rest_framework.permissions import IsAuthenticated

class BookListView(ListAPIView):
    serializer_class = BookSerializer
    permission_classes = [IsAuthenticated] 

    def get_queryset(self):
        user = self.request.user
        return Book.objects.filter(author=user) 
    
from rest_framework.generics import ListAPIView, RetrieveAPIView
from rest_framework.permissions import AllowAny

class BookListView(ListAPIView):
    queryset = Book.objects.all()
    serializer_class = BookSerializer
    permission_classes = [AllowAny]  

class BookDetailView(RetrieveAPIView):
    queryset = Book.objects.all()
    serializer_class = BookSerializer
    permission_classes = [AllowAny]  

from rest_framework.generics import CreateAPIView
from rest_framework.permissions import IsAuthenticated

class BookCreateView(CreateAPIView):
    queryset = Book.objects.all()
    serializer_class = BookSerializer
    permission_classes = [IsAuthenticated] 
    
from rest_framework.generics import UpdateAPIView
from rest_framework.permissions import IsAuthenticated

class BookUpdateView(UpdateAPIView):
    queryset = Book.objects.all()
    serializer_class = BookSerializer
    permission_classes = [IsAuthenticated] 
    
from rest_framework import generics, filters
from django_filters.rest_framework import DjangoFilterBackend
from .models import Book
from .serializers import BookSerializer

class BookListView(generics.ListAPIView):
    queryset = Book.objects.all()
    serializer_class = BookSerializer
    filter_backends = [DjangoFilterBackend, filters.SearchFilter]
    filterset_fields = ['title', 'author__name', 'publication_year']
    search_fields = ['title', 'author__name'] 
    
from rest_framework import generics, filters
from django_filters.rest_framework import DjangoFilterBackend
from .models import Book
from .serializers import BookSerializer

class BookListView(generics.ListAPIView):
    queryset = Book.objects.all()
    serializer_class = BookSerializer
    filter_backends = [DjangoFilterBackend, filters.SearchFilter, filters.OrderingFilter] 
    filterset_fields = ['title', 'author__name', 'publication_year']  
    search_fields = ['title', 'author__name']  
    ordering_fields = ['title', 'publication_year']  
    ordering = ['title'] 
    
from rest_framework import generics, filters
from django_filters.rest_framework import DjangoFilterBackend
from .models import Book
from .serializers import BookSerializer

class BookListView(generics.ListAPIView):
    queryset = Book.objects.all()
    serializer_class = BookSerializer
    
    filter_backends = [DjangoFilterBackend, filters.SearchFilter, filters.OrderingFilter]
    
    filterset_fields = ['title', 'author__name', 'publication_year']
    
    search_fields = ['title', 'author__name']
    
    ordering_fields = ['title', 'publication_year']
    
    ordering = ['title']

from rest_framework import generics
from .models import YourModel
from .serializers import YourModelSerializer
from rest_framework.permissions import IsAuthenticatedOrReadOnly, IsAuthenticated

class YourModelListView(generics.ListCreateAPIView):
    queryset = YourModel.objects.all()
    serializer_class = YourModelSerializer
    permission_classes = [IsAuthenticatedOrReadOnly]

class YourModelDetailView(generics.RetrieveUpdateDestroyAPIView):
    queryset = YourModel.objects.all()
    serializer_class = YourModelSerializer
    permission_classes = [IsAuthenticated] # views.py
from rest_framework import generics
from django_filters import rest_framework as filters
from .models import YourModel
from .serializers import YourModelSerializer
from .filters import YourModelFilter

class YourModelListView(generics.ListCreateAPIView):
    queryset = YourModel.objects.all()
    serializer_class = YourModelSerializer
    filter_backends = (filters.DjangoFilterBackend,)
    filterset_class = YourModelFilter




