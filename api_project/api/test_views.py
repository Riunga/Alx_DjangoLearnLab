import json
from django.test import TestCase, Client
from rest_framework import status
from .models import Book
from .serializers import BookSerializer

class BookAPITestCase(TestCase):
    def setUp(self):
        self.client = Client()
        self.book_data = {'title': 'Test Book', 'author': 'Test Author', 'publication_year': 2022}

    def test_create_book(self):
        response = self.client.post('/api/books/', self.book_data, format='json')
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(Book.objects.count(), 1)
        self.assertEqual(Book.objects.get().title, self.book_data['title'])

    def test_update_book(self):
        book = Book.objects.create(**self.book_data)
        updated_data = {'title': 'Updated Book'}
        response = self.client.patch(f'/api/books/{book.id}/', updated_data, format='json')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(Book.objects.get().title, updated_data['title'])

    def test_delete_book(self):
        book = Book.objects.create(**self.book_data)
        response = self.client.delete(f'/api/books/{book.id}/')
        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)
        self.assertEqual(Book.objects.count(), 0)

    def test_list_books(self):
        Book.objects.create(**self.book_data)
        response = self.client.get('/api/books/')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data), 1)

    def test_filter_books(self):
        Book.objects.create(**self.book_data)
        response = self.client.get('/api/books/?title=Test Book')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data), 1)

    def test_search_books(self):
        Book.objects.create(**self.book_data)
        response = self.client.get('/api/books/?search=Test')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data), 1)

    def test_ordering_books(self):
        Book.objects.create(**self.book_data)
        response = self.client.get('/api/books/?ordering=title')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data), 1)

    def test_permissions(self):
        # Test permission scenarios here
        pass