# -*- coding: utf-8 -*-
import urlparse
import time
import selenium.webdriver as findmethods
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
        print(url)
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

    def login(self, login, password):
        auth_form = self.form
        auth_form.open_form()
        auth_form.set_login(login)
        auth_form.set_password(password)
        auth_form.submit()

        return self


class MyRoomPage(AnswersPage):
    PATH = ''

    @property
    def my_room(self):
        return MyRoom(self.driver)

    @property
    def auth_form(self):
        return AuthForm(self.driver)

    @property
    def top_ask_question(self):
        return AskTop(self.driver)

    @property
    def center_form(self):
        return CenterForm(self.driver)


class AskPage(AnswersPage):
    PATH = '/ask/'

    @property
    def auth_form(self):
        return AuthForm(self.driver)

    @property
    def question_form(self):
        return QuestionForm(self.driver)

class CenterForm(Component):
    LAST_QUEST = '//*[@id="ColumnCenter"]/div/div/div[4]/div[1]/a'
    QUEST_IN_OPEN = '//*[@id="ColumnCenter"]/div/div/div[4]/div[1]/a'
    OPEN_BUTTON = '//*[@id="ColumnCenter"]/div/div/div[3]/div/a[2]'

    def wait_element(self, element):
        WebDriverWait(self.driver, 10).until(
            expected_conditions.presence_of_element_located((By.XPATH, element))
        )

    def last_quest_in_all(self):
        self.wait_element(self.LAST_QUEST)
        return self.driver.find_element_by_xpath(self.LAST_QUEST).get_attribute("href")

    def go_to_open_question(self):
        self.driver.find_element_by_xpath(self.OPEN_BUTTON).click()

    def last_quest_in_open(self):
        self.wait_element(self.QUEST_IN_OPEN)
        return self.driver.find_element_by_xpath(self.QUEST_IN_OPEN).get_attribute("href")


class QuestionForm(Component):
    ID_TEXT_AREA = 'ask-text'
    SEC_TEXT_PATH = '//*[@id="ColumnCenter"]/div/div/form/div[3]/div/div[1]/div/textarea'
    CATEGORY = '//*[@id="ask-categories"]'
    SUB_CATEGORY = '//*[@id="ask-sub-category"]'
    OPTION = "/option[text()='%s']"
    QUESTION_BUTTON = '//span[text()="Опубликовать вопрос"]'

    NEW_PAGE = '//*[@id="ColumnCenter"]/div/div[2]/div[1]/h1/index/text()'

    def set_question(self, question, second_text):
        self.driver.find_element_by_id(self.ID_TEXT_AREA).send_keys(question)
        self.driver.find_element_by_xpath(self.SEC_TEXT_PATH).send_keys(second_text)

    def set_category(self, category_name):
        self.driver.find_element_by_xpath(self.CATEGORY + (self.OPTION % category_name)).click()
        WebDriverWait(self.driver, 30).until(
            expected_conditions.presence_of_element_located((By.XPATH, self.SUB_CATEGORY))
        )

    def set_subcategory(self, subcategory_name):
        self.driver.find_element_by_xpath(self.SUB_CATEGORY + (self.OPTION % subcategory_name)).click()

    def publicate_question(self):
        self.driver.find_element_by_xpath(self.QUESTION_BUTTON).click()

    def get_url_question(self):
        self.driver.switch_to_window(self.driver.window_handles[-1])
        # WebDriverWait(self.driver, 5).until(
        #     expected_conditions.presence_of_element_located((By.XPATH, self.NEW_PAGE))
        # )

        return self.driver.current_url





class AskTop(Component):
    ASK_QUESTION_BUTTON = '//span[text()="Спросить"]'

    def ask_question_button(self):
        self.driver.find_element_by_xpath(self.ASK_QUESTION_BUTTON).click()
        self.driver.switch_to_window(self.driver.window_handles[-1])
        return self.driver.current_url



class AuthForm(Component):
    LOGIN = '//input[@name="Login"]'
    PASSWORD = '//input[@name="Password"]'
    SIGNUP = '//span[text()="Регистрация"]'
    SUBMIT = '//input[@value="Войти"]'
    LOGIN_BUTTON = '//a[text()="Вход"]'

    def wait_element(self, element):
        WebDriverWait(self.driver, 10).until(
            expected_conditions.presence_of_element_located((By.XPATH, element))
        )

    def open_form(self):
        self.driver.find_element_by_xpath(self.LOGIN_BUTTON).click()
        wait = WebDriverWait(self.driver, 5)
        wait.until(expected_conditions.element_to_be_clickable((By.XPATH, self.SIGNUP)))

    def set_login(self, login):
        self.wait_element(self.LOGIN)
        self.driver.find_element_by_xpath(self.LOGIN).send_keys(login)

    def set_password(self, pwd):
        self.driver.find_element_by_xpath(self.PASSWORD).send_keys(pwd)

    def submit(self):
        self.driver.find_element_by_xpath(self.SUBMIT).click()




class TopMenu(Component):
    USEREMAIL = '//i[@id="PH_user-email"]'
    AVATAR = '//a[starts-with(@title, "Личный кабинет")]'

    def get_name(self):
        return WebDriverWait(self.driver, 30, 0.1).until(
            lambda d: d.find_element_by_xpath(self.USEREMAIL).text
        )

    def go_to_my_room(self):
        wait = WebDriverWait(self.driver, 5)
        wait.until(expected_conditions.element_to_be_clickable((By.XPATH, self.AVATAR)))
        self.driver.find_element_by_xpath(self.AVATAR).click()
        href = WebDriverWait(self.driver, 30, 0.1).until(
             lambda d: d.find_element_by_xpath(self.AVATAR).get_attribute('href'))
        return MyRoomPage(self.driver, href)




class MyRoom(Component):
    MY_WORLD_BUTTON = '//a[text()="Мой мир"]'
    MY_WORLD_TITLE = '//span[@class="portal-menu__block "]/a'
    MY_WORLD_NAME_USER = '//h1'

    MY_WORLD_CATEGORY = '//div[@class="b-navigation__page-name"]'
    MY_PHOTOS_BUTTON = '//a[text()="Фотографии"]'
    MY_VIDEOS_BUTTON = '//a[text()="Видео"]'

    MY_VIDEOS_TITLE = '//a[@class="sp-video__head__logo sp-video-icon-head-logo js-router-link"]'

    TAKE_VIP_BUTTON = '//span[text()="Получить VIP-статус"]'
    VIP_TITLE = '//span[text()="1. Ваш заказ: Продление VIP статуса на 10 дней [100.00 руб.]"]'

    SETINGS_BUTTON = '//a[text()="Настройки"]'

    ACTIVITY_BUTTON = '//a[text()="Активность"]'

    def go_to_my_world(self):
        wait = WebDriverWait(self.driver, 5)
        wait.until(expected_conditions.element_to_be_clickable((By.XPATH, self.MY_WORLD_BUTTON)))
        self.driver.find_element_by_xpath(self.MY_WORLD_BUTTON).click()
        self.driver.switch_to_window(self.driver.window_handles[-1])
        return WebDriverWait(self.driver, 30, 0.1).until(
            lambda d: d.find_element_by_xpath(self.MY_WORLD_TITLE).get_attribute('href')
        )

    def get_name_on_my_world(self):
        return self.driver.find_element_by_xpath(self.MY_WORLD_NAME_USER).text

    def go_to_photos(self):
        wait = WebDriverWait(self.driver, 5)
        wait.until(expected_conditions.element_to_be_clickable((By.XPATH, self.MY_PHOTOS_BUTTON)))
        self.driver.find_element_by_xpath(self.MY_PHOTOS_BUTTON).click()

        self.driver.switch_to_window(self.driver.window_handles[-1])
        return WebDriverWait(self.driver, 50, 0.1).until(
            lambda d: d.find_element_by_xpath(self.MY_WORLD_TITLE).get_attribute('href')
        )

    def get_title_on_photos(self):
        return self.driver.find_element_by_xpath(self.MY_WORLD_CATEGORY).text

    def go_to_videos(self):
        wait = WebDriverWait(self.driver, 5)
        wait.until(expected_conditions.element_to_be_clickable((By.XPATH, self.MY_VIDEOS_BUTTON)))
        self.driver.find_element_by_xpath(self.MY_VIDEOS_BUTTON).click()

        self.driver.switch_to_window(self.driver.window_handles[-1])
        return WebDriverWait(self.driver, 30, 0.1).until(
            lambda d: d.find_element_by_xpath(self.MY_VIDEOS_TITLE).get_attribute('href')
        )

    def press_settings(self):
        self.driver.find_element_by_xpath(self.SETINGS_BUTTON).click()
        return self.driver.current_url

    def press_activity(self):
        self.driver.find_element_by_xpath(self.ACTIVITY_BUTTON).click()
        return self.driver.current_url


