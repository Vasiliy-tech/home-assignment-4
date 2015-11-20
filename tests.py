import os
import time
from AnswersPage import *
from unittest import TestCase
from selenium.webdriver import DesiredCapabilities, Remote
__author__ = 'ivansemenov'


class SimpleTest(TestCase):
    USEREMAIL = 'stotch_leopold@inbox.ru'
    PASSWORD = ''

    def setUp(self):
        browser = os.environ.get('TTHA2BROWSER', 'CHROME')

        self.driver = Remote(
            command_executor='http://127.0.0.1:4444/wd/hub',
            desired_capabilities=getattr(DesiredCapabilities, browser).copy()
        )

    def tearDown(self):
        time.sleep(5)
        self.driver.quit()

    def test(self):
        auth_page = AuthPage(self.driver)
        auth_page.open()

        auth_form = auth_page.form
        auth_form.open_form()
        auth_form.set_login(self.USEREMAIL)
        auth_form.set_password(self.PASSWORD)
        auth_form.submit()
