from django.test import TestCase, tag
from django.urls import resolve
from django.http import HttpRequest
from django.template.loader import render_to_string
from notes.models import Note, Book

from notes.views import home_page

# Create your tests here.


@tag("unit_test")
class HomePageTest(TestCase):
    def test_home_page_returns_correct_html(self):
        response = self.client.get("/")
        self.assertTemplateUsed(response, "home.html")


@tag("unit_test")
class BookAndNoteModelTest(TestCase):
    def test_saving_and_retrieving_notes(self):
        book = Book()
        book.save()

        first_note = Note()
        first_note.text = "The first (ever) note"
        first_note.book = book
        first_note.save()

        second_note = Note()
        second_note.text = "Note the second"
        second_note.book = book
        second_note.save()

        saved_book = Book.objects.first()
        self.assertEqual(saved_book, book)

        saved_notes = Note.objects.all()
        self.assertEqual(saved_notes.count(), 2)
        first_saved_note = saved_notes[0]
        second_saved_note = saved_notes[1]
        self.assertEqual(first_saved_note.text, "The first (ever) note")
        self.assertEqual(first_saved_note.book, book)
        self.assertEqual(second_saved_note.text, "Note the second")
        self.assertEqual(second_saved_note.book, book)


class NoteViewTest(TestCase):
    def test_uses_notes_template(self):
        book = Book.objects.create()
        response = self.client.get(f"/notes/books/{book.id}/")
        self.assertTemplateUsed(response, "notes.html")

    def test_display_all_notes_from_associated_book(self):
        correct_book = Book.objects.create()
        Note.objects.create(text="notey 1", book=correct_book)
        Note.objects.create(text="notey 2", book=correct_book)
        other_book = Book.objects.create()
        Note.objects.create(text="some other note 1", book=other_book)
        Note.objects.create(text="some other note 2", book=other_book)

        response = self.client.get(f"/notes/books/{correct_book.id}/")

        self.assertContains(response, "notey 1")
        self.assertContains(response, "notey 2")
        self.assertNotContains(response, "some other note 1")
        self.assertNotContains(response, "some other note 2")


class NewNoteTest(TestCase):
    def test_can_save_a_POST_request(self):
        self.client.post("/notes/new", data={"note_text": "A new note"})

        self.assertEqual(Note.objects.count(), 1)
        new_note = Note.objects.first()
        self.assertEqual(new_note.text, "A new note")

    def test_redirect_on_POST_request(self):
        response = self.client.post(
            "/notes/new", data={"note_text": "note for redirect me"}
        )
        new_book = Book.objects.first()
        self.assertRedirects(response, f"/notes/books/{new_book.id}/", 302)

    def test_can_save_a_POST_request_to_an_existing_book(self):
        other_book = Book.objects.create()
        correct_book = Book.objects.create()

        self.client.post(
            f"/notes/books/{correct_book.id}/add_note",
            data={"note_text": "A new note from an existing book"},
        )

        self.assertEqual(Note.objects.count(), 1)
        new_note = Note.objects.first()
        self.assertEqual(new_note.text, "A new note from an existing book")
        self.assertEqual(new_note.book, correct_book)

    def test_redirects_to_book_view(self):
        other_book = Book.objects.create()
        correct_book = Book.objects.create()

        response = self.client.post(f'/notes/books/{correct_book.id}/add_note', data={'note_text': 'A new note from an existing book'})

        self.assertRedirects(response, f'/notes/books/{correct_book.id}/')
