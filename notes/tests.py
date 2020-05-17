from django.test import TestCase, tag
from django.urls import resolve
from django.http import HttpRequest
from django.template.loader import render_to_string

from notes.views import home_page

# Create your tests here.


@tag("unit_test")
class HomePageTest(TestCase):
    def test_home_page_returns_correct_html(self):
        response = self.client.get("/")
        self.assertTemplateUsed(response, "home.html")

    def test_can_save_a_POST_request(self):
        response = self.client.post("/", data={"item_text": "A new note"})
        self.assertIn("A new note", response.content.decode())
        self.assertTemplateUsed(response, "home.html")
