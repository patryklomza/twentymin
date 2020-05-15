import socket
from urllib.parse import urlparse

from django.contrib.staticfiles.testing import StaticLiveServerTestCase
from django.test import override_settings, tag

from selenium import webdriver
from selenium.webdriver.common.desired_capabilities import DesiredCapabilities


@tag('selenium')
@override_settings(ALLOWED_HOSTS=['*'])
class BaseTestCase(StaticLiveServerTestCase):
    """
    Provides base test class which connects to the Docker
    container running selenium.
    """
    host = '0.0.0.0'

    @classmethod
    def setUpClass(cls):
        super().setUpClass()
        cls.host = socket.gethostbyname(socket.gethostname())
        cls.selenium = webdriver.Remote(
            command_executor='http://selenium:4444/wd/hub',
            desired_capabilities=DesiredCapabilities.CHROME,
        )
        cls.selenium.implicitly_wait(5)

    @classmethod
    def tearDownClass(cls):
        cls.selenium.quit()
        super().tearDownClass()

class WebTest(BaseTestCase):

    def test_home(self):
        self.selenium.get('%s%s' % (self.live_server_url, '/'))
        path = urlparse(self.selenium.current_url).path
        self.assertEqual('/', path)

        body_text = self.selenium.find_element_by_tag_name('body').text
        self.assertIn('Community Notes', body_text)
