# -*- coding: utf-8 -*-
from base import AnswersPage, Component
from selenium.common.exceptions import TimeoutException
__author__ = 'ivansemenov'


class QuestionPage(AnswersPage):

    @property
    def question(self):
        return Question(self.driver)


class Question(Component):

    SUBSCRIBE_BUTTON = '//button[@title="Подписаться"]'
    DELETE_BUTTON = '//button[@title="Удалить вопрос"]'
    DELETE_BUY_FRAME = '//iframe[starts-with(@src,"https://pw.money.mail.ru")]'
    QUESTION_TITLE = '//index'
    CLOSE_POPUP = '//div[@class="popup"]/i'

    def subscribe(self):
        self.wait_element_click(self.SUBSCRIBE_BUTTON)
        self.driver.find_element_by_xpath(self.SUBSCRIBE_BUTTON).click()

    def is_delete(self):
        self.wait_element_click(self.DELETE_BUTTON)
        self.driver.find_element_by_xpath(self.DELETE_BUTTON).click()
        try:
            self.wait_element_visible(self.DELETE_BUY_FRAME)
        except TimeoutException:
            return False
        return True

    def close_popup(self):
        self.wait_element_click(self.CLOSE_POPUP)
        self.driver.find_element_by_xpath(self.CLOSE_POPUP).click()

    def get_title(self):
        self.wait_element_visible(self.QUESTION_TITLE)
        return self.driver.find_element_by_xpath(self.QUESTION_TITLE).text
