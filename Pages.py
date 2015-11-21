# -*- coding: utf-8 -*-
import urlparse
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions
__author__ = 'ivansemenov'


class Component(object):
    def __init__(self, driver):
        self.driver = driver


class AnswersPage(object):
    BASE_URL = 'https://otvet.mail.ru/'
    PATH = ''

    def __init__(self, driver):
        self.driver = driver

    def open(self):
        url = urlparse.urljoin(self.BASE_URL, self.PATH)
        self.driver.get(url)
        self.driver.maximize_window()


class AuthPage(AnswersPage):
    PATH = ''

    @property
    def form(self):
        return AuthForm(self.driver)

    @property
    def top_menu(self):
        return TopMenu(self.driver)


class MyRoomPage(AnswersPage):
    PATH = 'profile/id207816682/' # id of stotch_leopold@inbox.ru

    @property
    def my_room(self):
        return MyRoom(self.driver)




class AuthForm(Component):
    LOGIN = '//input[@name="Login"]'
    PASSWORD = '//input[@name="Password"]'
    SIGNUP = '//span[text()="Регистрация"]'
    SUBMIT = '//input[@value="Войти"]'
    LOGIN_BUTTON = '//a[text()="Вход"]'

    def open_form(self):
        self.driver.find_element_by_xpath(self.LOGIN_BUTTON).click()
        wait = WebDriverWait(self.driver, 5)
        wait.until(expected_conditions.element_to_be_clickable((By.XPATH, self.SIGNUP)))

    def set_login(self, login):
        self.driver.find_element_by_xpath(self.LOGIN).send_keys(login)

    def set_password(self, pwd):
        self.driver.find_element_by_xpath(self.PASSWORD).send_keys(pwd)

    def submit(self):
        self.driver.find_element_by_xpath(self.SUBMIT).click()


class TopMenu(Component):
    USERNAME = '//a[text()="Личный кабинет, Леопольд Стотч"]'

    def get_name(self):
        return WebDriverWait(self.driver, 30, 0.1).until(
            lambda d: d.find_element_by_id('PH_user-email').text
        )


class MyRoom(Component):
    #GOTOROOM = '//a[text()="Личный кабинет, Леопольд Стотч"]'
    MY_WORLD_BUTTON = '//i[@class="icon icon-my_15"]'
    MY_WORLD_TITLE = '//a[@class="portal-menu__logo icon-head-logo booster-sc "]' #не забывай пробел на конце, где он есть
    MY_PHOTOS_BUTTON = '//i[@class="icon icon-photo_14"]'
    MY_VIDEOS_BUTTON = '//i[@class="icon icon-video_12"]'
    MY_VIDEOS_TITLE = '//a[@class="sp-video__head__logo sp-video-icon-head-logo js-router-link"]'


    def go_to_my_world(self):
        self.driver.find_element_by_xpath(self.MY_WORLD_BUTTON).click()
        #self.driver.switch_to_window('http://my.mail.ru/inbox/stotch_leopold/') #не понятно почему не работает

        self.driver.switch_to_window(self.driver.window_handles[-1])
        return WebDriverWait(self.driver, 50, 0.1).until(
            lambda d: d.find_element_by_xpath(self.MY_WORLD_TITLE).get_attribute('href')
        )


    def go_to_photos(self):
        self.driver.find_element_by_xpath(self.MY_PHOTOS_BUTTON).click()

        self.driver.switch_to_window(self.driver.window_handles[-1])
        return WebDriverWait(self.driver, 50, 0.1).until(
            lambda d: d.find_element_by_xpath(self.MY_WORLD_TITLE).get_attribute('href')
        )


    def go_to_videos(self):
        self.driver.find_element_by_xpath(self.MY_VIDEOS_BUTTON).click()

        self.driver.switch_to_window(self.driver.window_handles[-1])
        return WebDriverWait(self.driver, 50, 0.1).until(
            lambda d: d.find_element_by_xpath(self.MY_VIDEOS_TITLE).get_attribute('href')
        )