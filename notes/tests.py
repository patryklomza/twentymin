from django.test import TestCase, tag
from django.urls import resolve
from django.http import HttpRequest
from django.template.loader import render_to_string
from notes.models import Note

from notes.views import home_page

# Create your tests here.


@tag("unit_test")
class HomePageTest(TestCase):
    def test_home_page_returns_correct_html(self):
        response = self.client.get("/")
        self.assertTemplateUsed(response, "home.html")

    def test_can_save_a_POST_request(self):
        self.client.post("/", data={"note_text": "A new note"})

        self.assertEqual(Note.objects.count(), 1)
        new_note = Note.objects.first()
        self.assertEqual(new_note.text, "A new note")

    def test_only_saves_when_necessary(self):
        self.client.get("/")
        self.assertEqual(Note.objects.count(), 0)

    def test_redirect_on_POST_request(self):
        response = self.client.post("/", data={"note_text": "redirect me"})
        self.assertRedirects(response, "/", 302)


@tag("unit_test")
class NoteModelTest(TestCase):
    def test_saving_and_retrieving_notes(self):
        first_note = Note()
        first_note.text = "The first (ever) note"
        first_note.save()

        second_note = Note()
        second_note.text = "Note the second"
        second_note.save()

        saved_notes = Note.objects.all()
        self.assertEqual(saved_notes.count(), 2)
        first_saved_note = saved_notes[0]
        second_saved_note = saved_notes[1]
        self.assertEqual(first_saved_note.text, "The first (ever) note")
        self.assertEqual(second_saved_note.text, "Note the second")
