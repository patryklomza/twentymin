from django.test import TestCase
from django.urls import resolve
from django.http import HttpRequest

from notes.views import home_page

# Create your tests here.


class HomePageTest(TestCase):
    def test_root_url_resolves_to_home_page(self):
        found = resolve("/")
        self.assertEqual(found.func, home_page)

    def test_home_page_returns_correct_html(self):
        request = HttpRequest()
        response = home_page(request)
        html = response.content.decode("utf8")
        self.assertTrue(html.startswith("<html>"))
        self.assertIn("<h1>Community notes</h1>", html)
        self.assertTrue(html.endswith("</html>"))
