import socket
from urllib.parse import urlparse
import time

from django.contrib.staticfiles.testing import StaticLiveServerTestCase
from django.test import override_settings, tag

from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.desired_capabilities import DesiredCapabilities
from selenium.common.exceptions import WebDriverException

MAX_WAIT = 10


@tag("selenium")
@override_settings(ALLOWED_HOSTS=["*"])
class BaseTestCase(StaticLiveServerTestCase):
    """
    Provides base test class which connects to the Docker
    container running selenium.
    """

    host = "0.0.0.0"

    @classmethod
    def setUpClass(cls):
        super().setUpClass()
        cls.host = socket.gethostbyname(socket.gethostname())
        cls.selenium = webdriver.Remote(
            command_executor="http://selenium:4444/wd/hub",
            desired_capabilities=DesiredCapabilities.CHROME,
        )

    @classmethod
    def tearDownClass(cls):
        cls.selenium.quit()
        super().tearDownClass()


@tag("selenium")
class WebTest(BaseTestCase):

    def check_for_multiple_paragraphs(self, paragraph_text):
        paragraphs = self.selenium.find_elements_by_id("id_note_paragraph")
        self.assertIn(paragraph_text, [item.text for item in paragraphs])

    def wait_for_paragraph(self, paragraph_text):
        start_time = time.time()
        while True:
            try:
                self.check_for_multiple_paragraphs(paragraph_text)
                return
            except (AssertionError, WebDriverException) as e:
                if time.time() - start_time > MAX_WAIT:
                    raise e
                time.sleep(0.5)

    def test_home(self):

        # Surma has heard about a new online app promoting reading and note
        # making. She goes to check out its homepage
        self.selenium.get("%s%s" % (self.live_server_url, "/"))
        path = urlparse(self.selenium.current_url).path
        self.assertEqual("/", path)

        # She notices the page header mention notes made by community
        header_text = self.selenium.find_element_by_tag_name("h1").text
        self.assertIn("Community notes", header_text)

        # She is invited to make her own note
        inputbox = self.selenium.find_element_by_id("id_new_item")
        self.assertEqual(inputbox.get_attribute("placeholder"), "Make a new note")

        # She types "New note from reading TDD with Django"
        inputbox.send_keys("TDD is an intriguing experience")

        # When she hits enter, the page updates, and now the page lists
        # "TDD is an intriguing experience" in a paragraph

        inputbox.send_keys(Keys.ENTER)
        self.wait_for_paragraph("TDD is an intriguing experience")

        # There is still a text box inviting her to add another note.
        # She enters "TDD is not easy at start"
        inputbox = self.selenium.find_element_by_id("id_new_item")
        inputbox.send_keys("TDD is not easy at start")
        inputbox.send_keys(Keys.ENTER)

        self.wait_for_paragraph("TDD is an intriguing experience")
        self.wait_for_paragraph("TDD is not easy at start")

        # Surma wonders whether the site will remember her list. Then she sees
        # that the site has generated a unique URL for her -- there is some
        # explanatory text to that effect
        self.fail("Finish the test!")

        # She visits that URL - her notes are still there
