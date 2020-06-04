from django.db import models

# Create your models here.


class Book(models.Model):
    pass


class Note(models.Model):
    text = models.TextField(default="")
    book = models.ForeignKey(Book, default=None, on_delete=models.CASCADE)
