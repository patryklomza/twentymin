from django.shortcuts import render, redirect
from django.http import HttpResponse
from notes.models import Note, Book

# Create your views here.


def home_page(request):
    return render(request, "home.html")


def view_note(request, book_id):
    book = Book.objects.get(id=book_id)
    return render(request, "notes.html", {"book": book})


def new_note(request):
    book = Book.objects.create()
    Note.objects.create(text=request.POST["note_text"], book=book)
    return redirect(f"/notes/books/{book.id}/")


def add_note(request, book_id):
    book = Book.objects.get(id=book_id)
    Note.objects.create(text=request.POST["note_text"], book=book)
    return redirect(f"/notes/books/{book.id}/")
