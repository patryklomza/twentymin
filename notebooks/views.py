from django.shortcuts import render, redirect
from django.http import HttpResponse
from notebooks.models import Note, Notebook

# Create your views here.


def home_page(request):
    return render(request, "home.html")


def view_notebook(request, notebook_id):
    notebook = Notebook.objects.get(id=notebook_id)
    return render(request, "notebooks.html", {"notebook": notebook})


def new_note(request):
    notebook = Notebook.objects.create()
    Note.objects.create(text=request.POST["note_text"], notebook=notebook)
    return redirect(f"/notebooks/{notebook.id}/")


def add_note(request, notebook_id):
    notebook = Notebook.objects.get(id=notebook_id)
    Note.objects.create(text=request.POST["note_text"], notebook=notebook)
    return redirect(f"/notebooks/{notebook.id}/")
