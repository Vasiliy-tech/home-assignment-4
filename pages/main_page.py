# -*- coding: utf-8 -*-
from base import AnswersPage, Component
from my_room_page import MyRoomPage
from question_page import QuestionPage
from another_room_page import AnotherRoomPage
from selenium.webdriver.support.ui import WebDriverWait
from selenium.common.exceptions import TimeoutException
__author__ = 'ivansemenov'


class MainPage(AnswersPage):

    @property
    def auth_form(self):
        return AuthForm(self.driver)

    @property
    def top_menu(self):
        return TopMenu(self.driver)

    @property
    def center_block(self):
        return CenterBlock(self.driver)



class AuthForm(Component):

    LOGIN = '//input[@name="Login"]'
    PASSWORD = '//input[@name="Password"]'
    SIGNUP = '//span[text()="Регистрация"]'
    SUBMIT = '//span[@data-action="login"]'
    LOGIN_BUTTON = '//a[text()="Вход"]'
    EXIT = '//a[text()="выход"]'

    def open_form(self):
        self.wait_element(self.LOGIN_BUTTON)
        self.driver.find_element_by_xpath(self.LOGIN_BUTTON).click()
        self.wait_element(self.SIGNUP)

    def set_login(self, login):
        self.wait_element(self.LOGIN)
        self.driver.find_element_by_xpath(self.LOGIN).send_keys(login)

    def set_password(self, pwd):
        self.wait_element(self.PASSWORD)
        self.driver.find_element_by_xpath(self.PASSWORD).send_keys(pwd)

    def submit(self):
        self.wait_element(self.SUBMIT)
        self.driver.find_element_by_xpath(self.SUBMIT).click()

    def logout(self):
        self.wait_element(self.EXIT)
        self.driver.find_element_by_xpath(self.EXIT).click()


class CenterBlock(Component):
    LAST_QUESTION = '//div[@class="pageQuestions"]/div[starts-with(@class,"q--li")]/a[starts-with(@href,"/question/")]'
    LAST_AUTHOR = '//div[@class="pageQuestions"]/div[starts-with(@class,"q--li")]/a[starts-with(@href,"/profile/")]'
    LOGIN = '//input[@name="Login"]'
    def choose_last_question(self):
        self.wait_element(self.LAST_QUESTION)
        self.driver.find_element_by_xpath(self.LAST_QUESTION).click()
        return QuestionPage(self.driver)

    def choose_last_author_quest(self):
        self.wait_element(self.LAST_AUTHOR)
        self.driver.find_element_by_xpath(self.LAST_AUTHOR).click()
        return AnotherRoomPage(self.driver)

    def is_authorizate(self):
        try:
            self.wait_element(self.LOGIN)
        except TimeoutException:
            return True
        return False

class TopMenu(Component):
    AVATAR = '//a[starts-with(@title, "Личный кабинет")]'

    def get_name(self):
        return WebDriverWait(self.driver, 30, 0.1).until(
            lambda d: d.find_element_by_id('PH_user-email').text
        )

    def go_to_my_room(self):
        self.wait_element(self.AVATAR)
        self.driver.find_element_by_xpath(self.AVATAR).click()
        return MyRoomPage(self.driver)
