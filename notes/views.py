from django.shortcuts import render, redirect
from django.http import HttpResponse
from notes.models import Note

# Create your views here.


def home_page(request):
    if request.method == "POST":
        new_note_text = request.POST["note_text"]
        Note.objects.create(text=new_note_text)
        return redirect("/")

    notes = Note.objects.all()

    return render(request, "home.html", {"notes": notes})
