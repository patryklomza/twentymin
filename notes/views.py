from django.shortcuts import render, redirect
from django.http import HttpResponse
from notes.models import Note

# Create your views here.


def home_page(request):
    return render(request, "home.html")


def view_note(request):
    notes = Note.objects.all()

    return render(request, "notes.html", {"notes": notes})


def new_note(request):
    Note.objects.create(text=request.POST["note_text"])
    return redirect("/notes/the-one-of-a-kind-note/")
