from django.db import models

class Author(models.Model):
    name = models.CharField(max_length=255)

    def __str__(self):
        return self.name

class Book(models.Model):
    title = models.CharField(max_length=255)
    publication_year = models.IntegerField()
    author = models.ForeignKey(Author, on_delete=models.CASCADE, related_name='books')

    def __str__(self):
        return self.title

from django.db import models

class Author(models.Model):
    # The Author model represents an author of books.
    # This model has a single field 'name' to store the author's name.
    name = models.CharField(max_length=255)

    def __str__(self):
        return self.name


class Book(models.Model):
    # The Book model represents a book written by an author.
    # It has three fields: 'title' for the book's title, 'publication_year' for the year it was published,
    # and 'author' which is a ForeignKey linking to the Author model, establishing a one-to-many relationship.
    title = models.CharField(max_length=255)
    publication_year = models.IntegerField()
    author = models.ForeignKey(Author, on_delete=models.CASCADE, related_name='books')

    def __str__(self):
        return self.title
