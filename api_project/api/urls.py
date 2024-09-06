from django.urls import path
from .views import BookList

urlpatterns = [
    path('books/', BookList.as_view(), name='book-list'),  # List all books
]

from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import BookViewSet

# Create a router and register the BookViewSet
router = DefaultRouter()
router.register(r'books', BookViewSet)

# The API URLs are determined automatically by the router
urlpatterns = [
    path('', include(router.urls)),
]

from django.urls import path, include
from rest_framework import routers
from . import views

router = routers.DefaultRouter()
router.register(r'books', views.BookViewSet, basename='books')

urlpatterns = [
    path('', include(router.urls)),
    path('books/', views.BookListView.as_view()),
    path('books/<int:pk>/', views.BookDetailView.as_view()),
    path('books/create/', views.BookCreateView.as_view()),
    path('books/<int:pk>/update/', views.BookUpdateView.as_view()),
    path('books/<int:pk>/delete/', views.BookDeleteView.as_view()),
]