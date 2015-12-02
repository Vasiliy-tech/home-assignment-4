# -*- coding: utf-8 -*-
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions
from selenium.webdriver.support.ui import WebDriverWait
import urlparse
__author__ = 'ivansemenov'


class Component(object):

    def __init__(self, driver):
        self.driver = driver

    def wait_element(self, element):
        WebDriverWait(self.driver, 10).until(
            expected_conditions.element_to_be_clickable((By.XPATH, element))
        )


class AnswersPage(object):
    PATH = ''
    BASE_URL = 'https://otvet.mail.ru/'

    def __init__(self, driver):
        self.driver = driver

    def open(self):
        url = urlparse.urljoin(self.BASE_URL, self.PATH)
        self.driver.get(url)
        self.driver.maximize_window()