from django.db import models

# Create your models here.


class Notebook(models.Model):
    pass


class Note(models.Model):
    text = models.TextField(default="")
    notebook = models.ForeignKey(Notebook, default=None, on_delete=models.CASCADE)
