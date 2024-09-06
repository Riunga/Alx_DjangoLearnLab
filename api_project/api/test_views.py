from django.test import TestCase
from rest_framework.test import APIClient
from rest_framework import status
from django.urls import reverse
from .models import Book, Author

class BookAPITestCase(TestCase):

    def setUp(self):
        self.client = APIClient()
        self.author = Author.objects.create(name="Author 1")
        self.book_data = {
            "title": "Book Title",
            "publication_year": 2023,
            "author": self.author.id
        }
        self.create_url = reverse('book-create')

    def test_create_book(self):
        response = self.client.post(self.create_url, self.book_data, format='json')
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(Book.objects.count(), 1)
        self.assertEqual(Book.objects.get().title, 'Book Title')

    def test_get_book_detail(self):
        book = Book.objects.create(title="Sample Book", publication_year=2020, author=self.author)
        response = self.client.get(reverse('book-detail', kwargs={'pk': book.id}))
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data['title'], 'Sample Book')

    def test_update_book(self):
        book = Book.objects.create(title="Old Title", publication_year=2020, author=self.author)
        updated_data = {
            "title": "Updated Title",
            "publication_year": 2021,
            "author": self.author.id
        }
        response = self.client.put(reverse('book-update', kwargs={'pk': book.id}), updated_data, format='json')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        book.refresh_from_db()
        self.assertEqual(book.title, "Updated Title")

    def test_delete_book(self):
        book = Book.objects.create(title="Sample Book", publication_year=2020, author=self.author)
        response = self.client.delete(reverse('book-delete', kwargs={'pk': book.id}))
        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)
        self.assertEqual(Book.objects.count(), 0)

    def test_filter_books(self):
        author2 = Author.objects.create(name="Author 2")
        Book.objects.create(title="Book 1", publication_year=2020, author=self.author)
        Book.objects.create(title="Book 2", publication_year=2021, author=author2)

        response = self.client.get(reverse('book-list'), {'author__name': 'Author 2'})
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data), 1)
        self.assertEqual(response.data[0]['title'], 'Book 2')

    def test_search_books(self):
        Book.objects.create(title="Unique Title", publication_year=2020, author=self.author)
        response = self.client.get(reverse('book-list'), {'search': 'Unique'})
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data), 1)
        self.assertEqual(response.data[0]['title'], 'Unique Title')

    def test_order_books(self):
        Book.objects.create(title="Book A", publication_year=2020, author=self.author)
        Book.objects.create(title="Book B", publication_year=2021, author=self.author)

        response = self.client.get(reverse('book-list'), {'ordering': 'title'})
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data[0]['title'], 'Book A')
