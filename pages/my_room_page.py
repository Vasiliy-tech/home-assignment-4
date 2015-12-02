# -*- coding: utf-8 -*-
from base import AnswersPage, Component
from question_page import QuestionPage
from selenium.common.exceptions import TimeoutException
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver import ActionChains
__author__ = 'ivansemenov'


class MyRoomPage(AnswersPage):

    @property
    def left_block(self):
        return LeftBlock(self.driver)

    @property
    def center_block(self):
        return CenterForm(self.driver)


class LeftBlock(Component):
    MY_WORLD_BUTTON = '//a[text()="Мой мир"]'
    LOGO_TITLE = '//a[starts-with(@class,"portal-menu__logo")]'
    MY_PHOTOS_BUTTON = '//a[text()="Фотографии"]'
    MY_PHOTOS_NAME = '//a[contains(@class,"b-leftmenu__user-page-2")]'
    MY_WORLD_CATEGORY_TITLE = '//div[contains(@class,"b-navigation__page-name")]'
    MY_VIDEOS_BUTTON = '//a[text()="Видео"]'
    MY_VIDEOS_TITLE = '//a[text()="Мое видео"]'
    MY_WORLD_NAME = '//h1'
    USERNAME = '//h1'
    VIPBUTTON = '//i[@title="VIP-пользователь"]'
    VIPCLOSE = '//div[@class="popup"]/i'
    BUY_FRAME = '//iframe[starts-with(@src,"https://pw.money.mail.ru")]'
    SETINGS_BUTTON = '//a[text()="Настройки"]'
    ACTIVITY_BUTTON = '//a[text()="Активность"]'

    def get_user_name(self):
        self.wait_element(self.USERNAME)
        return self.driver.find_element_by_xpath(self.USERNAME).text

    def get_vip(self):
        self.wait_element(self.VIPBUTTON)
        self.driver.find_element_by_xpath(self.VIPBUTTON).click()

    def close_vip(self):
        self.wait_element(self.VIPCLOSE)
        self.driver.find_element_by_xpath(self.VIPCLOSE).click()

    def buy_vip_frame_exist(self):
        try:
            self.wait_element(self.BUY_FRAME)
        except TimeoutException:
            return False
        return True

    def go_to_my_world(self):
        self.wait_element(self.MY_WORLD_BUTTON)
        self.driver.find_element_by_xpath(self.MY_WORLD_BUTTON).click()
        self.driver.switch_to_window(self.driver.window_handles[-1])
        return WebDriverWait(self.driver, 30, 0.1).until(
            lambda d: d.find_element_by_xpath(self.LOGO_TITLE).get_attribute('href')
        )

    def get_name_by_my_world(self):
        self.wait_element(self.MY_WORLD_NAME)
        return self.driver.find_element_by_xpath(self.MY_WORLD_NAME).text

    def go_to_photos(self):
        self.wait_element(self.MY_PHOTOS_BUTTON)
        self.driver.find_element_by_xpath(self.MY_PHOTOS_BUTTON).click()
        self.driver.switch_to_window(self.driver.window_handles[-1])
        return WebDriverWait(self.driver, 30, 0.1).until(
            lambda d: d.find_element_by_xpath(self.LOGO_TITLE).get_attribute('href')
        )

    def is_photos(self):
        self.wait_element(self.MY_WORLD_CATEGORY_TITLE)
        return self.driver.find_element_by_xpath(self.MY_WORLD_CATEGORY_TITLE).text

    def go_to_videos(self):
        self.wait_element(self.MY_VIDEOS_BUTTON)
        self.driver.find_element_by_xpath(self.MY_VIDEOS_BUTTON).click()
        self.driver.switch_to_window(self.driver.window_handles[-1])
        return WebDriverWait(self.driver, 30, 0.1).until(
            lambda d: d.find_element_by_xpath(self.MY_VIDEOS_TITLE).get_attribute('href')
        )

    def is_videos(self):
        try:
            self.wait_element(self.MY_VIDEOS_TITLE)
        except TimeoutException:
            return False
        return True

    def press_settings(self):
        self.wait_element(self.SETINGS_BUTTON)
        self.driver.find_element_by_xpath(self.SETINGS_BUTTON).click()
        return self.driver.current_url

    def press_activity(self):
        self.wait_element(self.ACTIVITY_BUTTON)
        self.driver.find_element_by_xpath(self.ACTIVITY_BUTTON).click()
        return self.driver.current_url


class CenterForm(Component):
    SUBSCRIBE_COUNT_QUESTIONS = '//span[@title="Вопросов"]'
    SUBSCRIBE_COUNT_USERS = '//span[@title="Пользователей"]'
    CHECK_QUESTION = '//a[starts-with(@href,"/question/") and text()="%s"]'
    CHECK_USER = '//div[a[@href="/profile/%s/" and not(@style)]]'
    SUBSCRIBE_BUTTON = '//a[./div[text()="Подписки"]]'
    SUBSCRIBE_QUESTION_BUTTON = '//a[text()="Вопросы"]'
    SUBSCRIBE_USERS_BUTTON = '//a[text()="Пользователи"]'
    UNSUBSCRIBE_QUESTION_BUTTON = '//div[a[starts-with(@href,"/question/") and text()="%s"]]//button'
    UNSUBSCRIBE_USER_BUTTON = '//div[a[@href="/profile/%s/" and not(@style)]]//button'
    MY_QUESTIONS_BUTTON = '//div[text()="Вопросы"]'
    MY_LAST_OPEN_QUESTION = '//a[starts-with(@href,"/question/") and @title="Вопрос на голоcовании"]'

    def get_subscribe_count_questions(self):
        self.wait_element(self.SUBSCRIBE_COUNT_QUESTIONS)
        return self.driver.find_element_by_xpath(self.SUBSCRIBE_COUNT_QUESTIONS).text

    def get_subscribe_count_users(self):
        self.wait_element(self.SUBSCRIBE_COUNT_USERS)
        return self.driver.find_element_by_xpath(self.SUBSCRIBE_COUNT_USERS).text

    def go_to_subcribes_users(self):
        self.wait_element(self.SUBSCRIBE_BUTTON)
        self.driver.find_element_by_xpath(self.SUBSCRIBE_BUTTON).click()
        self.wait_element(self.SUBSCRIBE_USERS_BUTTON)
        self.driver.find_element_by_xpath(self.SUBSCRIBE_USERS_BUTTON).click()

    def go_to_subcribes_question(self):
        self.wait_element(self.SUBSCRIBE_BUTTON)
        self.driver.find_element_by_xpath(self.SUBSCRIBE_BUTTON).click()
        self.wait_element(self.SUBSCRIBE_QUESTION_BUTTON)
        self.driver.find_element_by_xpath(self.SUBSCRIBE_QUESTION_BUTTON).click()

    def go_to_questions(self):
        self.wait_element(self.MY_QUESTIONS_BUTTON)
        self.driver.find_element_by_xpath(self.MY_QUESTIONS_BUTTON).click()

    def choose_last_my_open_question(self):
        self.wait_element(self.MY_LAST_OPEN_QUESTION)
        self.driver.find_element_by_xpath(self.MY_LAST_OPEN_QUESTION).click()
        return QuestionPage(self.driver)

    def unsubscribe_question(self, title):
        self.wait_element(self.CHECK_QUESTION % title)
        question = self.driver.find_element_by_xpath(self.CHECK_QUESTION % title)
        hov = ActionChains(self.driver).move_to_element(question)
        hov.perform()
        self.driver.find_element_by_xpath(self.UNSUBSCRIBE_QUESTION_BUTTON % title).click()

    def unsubscribe_user(self, user_id):
        self.wait_element(self.CHECK_USER % user_id)
        user = self.driver.find_element_by_xpath(self.CHECK_USER % user_id)
        hov = ActionChains(self.driver).move_to_element(user)
        hov.perform()
        self.driver.find_element_by_xpath(self.UNSUBSCRIBE_USER_BUTTON % user_id).click()

    def check_question(self, title):
        try:
            self.wait_element(self.CHECK_QUESTION % title)
        except TimeoutException:
            return False
        return True

    def check_user(self, user_id):
        try:
            self.wait_element(self.CHECK_USER % user_id)
        except TimeoutException:
            return False
        return True
