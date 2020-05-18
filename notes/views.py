from django.shortcuts import render
from django.http import HttpResponse
from notes.models import Note

# Create your views here.


def home_page(request):
    note = Note()
    note.text = request.POST.get("note_text", "")
    note.save()

    return render(request, "home.html", {"new_note_text": note.text})
