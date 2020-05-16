import socket
from urllib.parse import urlparse
import time

from django.contrib.staticfiles.testing import StaticLiveServerTestCase
from django.test import override_settings, tag

from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.desired_capabilities import DesiredCapabilities



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
        cls.selenium.implicitly_wait(5)

    @classmethod
    def tearDownClass(cls):
        cls.selenium.quit()
        super().tearDownClass()


@tag("selenium")
class WebTest(BaseTestCase):
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
        time.sleep(1)

        paragraph = self.selenium.find_element_by_id("id_note_paragraph")
        self.assertIn("TDD is an intriguing experience", paragraph)

        # There is still a text box inviting her to add another note.
        # She enters "TDD is not easy at start"
        self.fail("Finish the test!")
