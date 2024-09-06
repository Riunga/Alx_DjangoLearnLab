from django.urls import reverse
from rest_framework.test import APITestCase, APIClient
from rest_framework import status
from api.models import Book, Author

class BookAPITestCase(APITestCase):

    def setUp(self):
        # Set up initial data: an Author and a Book instance
        self.author = Author.objects.create(name="J.K. Rowling")
        self.book = Book.objects.create(
            title="Harry Potter and the Philosopher's Stone",
            publication_year=1997,
            author=self.author
        )
        self.client = APIClient()  # Use the APIClient for making API requests

    # Test for creating a book
    def test_create_book(self):
        url = reverse('book-list')  # Ensure this matches the URL pattern for listing/creating books
        data = {
            "title": "Harry Potter and the Chamber of Secrets",
            "publication_year": 1998,
            "author": self.author.id  # Reference the author by ID
        }
        response = self.client.post(url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(Book.objects.count(), 2)  # Ensure a second book was created
        self.assertEqual(Book.objects.last().title, "Harry Potter and the Chamber of Secrets")

    # Test for retrieving a book
    def test_retrieve_book(self):
        url = reverse('book-detail', args=[self.book.id])  # Ensure this matches the URL pattern for book details
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data['title'], self.book.title)

    # Test for updating a book
    def test_update_book(self):
        url = reverse('book-detail', args=[self.book.id])
        data = {
            "title": "Harry Potter and the Sorcerer's Stone",  # Updated title
            "publication_year": 1997,
            "author": self.author.id
        }
        response = self.client.put(url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.book.refresh_from_db()  
        self.assertEqual(self.book.title, "Harry Potter and the Sorcerer's Stone")

    def test_delete_book(self):
        url = reverse('book-detail', args=[self.book.id])
        response = self.client.delete(url)
        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)
        self.assertEqual(Book.objects.count(), 0)  
