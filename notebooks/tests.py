from django.test import TestCase, tag
from django.urls import resolve
from django.http import HttpRequest
from django.template.loader import render_to_string
from notebooks.models import Note, Notebook

from notebooks.views import home_page

# Create your tests here.


@tag("unit_test")
class HomePageTest(TestCase):
    def test_home_page_returns_correct_html(self):
        response = self.client.get("/")
        self.assertTemplateUsed(response, "home.html")


@tag("unit_test")
class NotebookAndNoteModelTest(TestCase):
    def test_saving_and_retrieving_notes(self):
        notebook = Notebook()
        notebook.save()

        first_note = Note()
        first_note.text = "The first (ever) note"
        first_note.notebook = notebook
        first_note.save()

        second_note = Note()
        second_note.text = "Note the second"
        second_note.notebook = notebook
        second_note.save()

        saved_notebook = Notebook.objects.first()
        self.assertEqual(saved_notebook, notebook)

        saved_notes = Note.objects.all()
        self.assertEqual(saved_notes.count(), 2)
        first_saved_note = saved_notes[0]
        second_saved_note = saved_notes[1]
        self.assertEqual(first_saved_note.text, "The first (ever) note")
        self.assertEqual(first_saved_note.notebook, notebook)
        self.assertEqual(second_saved_note.text, "Note the second")
        self.assertEqual(second_saved_note.notebook, notebook)


class NotebookViewTest(TestCase):
    def test_uses_notebooks_template(self):
        notebook = Notebook.objects.create()
        response = self.client.get(f"/notebooks/{notebook.id}/")
        self.assertTemplateUsed(response, "notebooks.html")

    def test_display_all_notes_from_associated_notebook(self):
        correct_notebook = Notebook.objects.create()
        Note.objects.create(text="notey 1", notebook=correct_notebook)
        Note.objects.create(text="notey 2", notebook=correct_notebook)
        other_notebook = Notebook.objects.create()
        Note.objects.create(text="some other note 1", notebook=other_notebook)
        Note.objects.create(text="some other note 2", notebook=other_notebook)

        response = self.client.get(f"/notebooks/{correct_notebook.id}/")

        self.assertContains(response, "notey 1")
        self.assertContains(response, "notey 2")
        self.assertNotContains(response, "some other note 1")
        self.assertNotContains(response, "some other note 2")

    def test_passes_correct_notebook_to_template(self):
        other_notebook = Notebook.objects.create()
        correct_notebook = Notebook.objects.create()
        response = self.client.get(f'/notebooks/{correct_notebook.id}/')
        self.assertEquals(response.context['notebook'], correct_notebook)


class NewNoteTest(TestCase):
    def test_can_save_a_POST_request(self):
        self.client.post("/notebooks/new", data={"note_text": "A new note"})

        self.assertEqual(Note.objects.count(), 1)
        new_note = Note.objects.first()
        self.assertEqual(new_note.text, "A new note")

    def test_redirect_on_POST_request(self):
        response = self.client.post(
            "/notebooks/new", data={"note_text": "note for redirect me"}
        )
        new_notebook = Notebook.objects.first()
        self.assertRedirects(response, f"/notebooks/{new_notebook.id}/", 302)

    def test_can_save_a_POST_request_to_an_existing_notebook(self):
        other_notebook = Notebook.objects.create()
        correct_notebook = Notebook.objects.create()

        self.client.post(
            f"/notebooks/{correct_notebook.id}/add_note",
            data={"note_text": "A new note from an existing notebook"},
        )

        self.assertEqual(Note.objects.count(), 1)
        new_note = Note.objects.first()
        self.assertEqual(new_note.text, "A new note from an existing notebook")
        self.assertEqual(new_note.notebook, correct_notebook)

    def test_redirects_to_notebook_view(self):
        other_notebook = Notebook.objects.create()
        correct_notebook = Notebook.objects.create()

        response = self.client.post(f'/notebooks/{correct_notebook.id}/add_note', data={'note_text': 'A new note from an existing notebook'})

        self.assertRedirects(response, f'/notebooks/{correct_notebook.id}/')
