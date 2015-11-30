# -*- coding: utf-8 -*-
import urlparse
from selenium.webdriver import ActionChains
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions
from selenium.common.exceptions import TimeoutException



class Component(object):

    def __init__(self, driver):
        self.driver = driver

    def wait_element(self, element):
        WebDriverWait(self.driver, 30).until(
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




class MainPage(AnswersPage):

    @property
    def auth_form(self):
        return AuthForm(self.driver)

    @property
    def top_menu(self):
        return TopMenu(self.driver)


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


class CenterForm(Component):
    SUBSCRIBE_COUNT_QUESTIONS = '//span[@title="Вопросов"]'

    def get_subscribe_count_questions(self):
        self.wait_element(self.SUBSCRIBE_COUNT_QUESTIONS)
        return self.driver.find_element_by_xpath(self.SUBSCRIBE_COUNT_QUESTIONS).text

class QuestionForm(Component):
    ID_TEXT_AREA = 'ask-text'
    SEC_TEXT_PATH = '//*[@placeholder="Введите текст пояснения"]'
    CATEGORY = '//*[@id="ask-categories"]'
    SUB_CATEGORY = '//*[@id="ask-sub-category"]'
    OPTION = "/option[text()='%s']"
    QUESTION_BUTTON ='//span[text()="Опубликовать вопрос"]'

    NEW_PAGE = '//*[@id="ColumnCenter"]/div/div[2]/div[1]/h1/index/text()'

    def wait_element(self, element):
        WebDriverWait(self.driver, 30).until(
            expected_conditions.presence_of_element_located((By.ID, element))
        )

    def set_question(self, question, second_text):
        self.wait_element(self.ID_TEXT_AREA)
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

        return self.driver.current_url


class AskTop(Component):
    ASK_QUESTION_BUTTON = '//span[text()="Спросить"]'

    def wait_element(self, element):
        WebDriverWait(self.driver, 10).until(
            expected_conditions.presence_of_element_located((By.XPATH, element))
        )

    def ask_question_button(self):
        self.wait_element(self.ASK_QUESTION_BUTTON)
        self.driver.find_element_by_xpath(self.ASK_QUESTION_BUTTON).click()
        self.driver.switch_to_window(self.driver.window_handles[-1])
        return self.driver.current_url


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


class MyRoom(Component):
    MY_WORLD_BUTTON = '//a[text()="Мой мир"]'
    MY_WORLD_TITLE = '//a[@class="portal-menu__logo icon-head-logo booster-sc "]'

    MY_PHOTOS_BUTTON = '//a[text()="Фотографии"]'
    MY_VIDEOS_BUTTON = '//a[text()="Видео"]'

    MY_VIDEOS_TITLE = '//a[@class="sp-video__head__logo sp-video-icon-head-logo js-router-link"]'

    TAKE_VIP_BUTTON = '//span[text()="Получить VIP-статус"]'
    VIP_TITLE = '//span[text()="1. Ваш заказ: Продление VIP статуса на 10 дней [100.00 руб.]"]'

    SETINGS_BUTTON = '//a[text()="Настройки"]'

    ACTIVITY_BUTTON = '//a[text()="Активность"]'

    SUBSC_BUT_AD_USER = '//span[text()="Подписаться"]'


    def wait_element(self, element):
        WebDriverWait(self.driver, 50).until(
            expected_conditions.presence_of_element_located((By.XPATH, element))
        )

    def wait_element(self, element):
        WebDriverWait(self.driver, 50).until(
            expected_conditions.element_to_be_clickable((By.XPATH, element))
        )

    def go_to_my_world(self):
        self.wait_element(self.MY_WORLD_BUTTON)
        self.driver.find_element_by_xpath(self.MY_WORLD_BUTTON).click()
        self.driver.switch_to_window(self.driver.window_handles[-1])
        return WebDriverWait(self.driver, 50, 0.1).until(
            lambda d: d.find_element_by_xpath(self.MY_WORLD_TITLE).get_attribute('href')
        )

    def go_to_photos(self):
        self.wait_element(self.MY_PHOTOS_BUTTON)
        self.driver.find_element_by_xpath(self.MY_PHOTOS_BUTTON).click()
        self.driver.switch_to_window(self.driver.window_handles[-1])
        return WebDriverWait(self.driver, 50, 0.1).until(
            lambda d: d.find_element_by_xpath(self.MY_WORLD_TITLE).get_attribute('href')
        )

    def go_to_videos(self):
        self.wait_element(self.MY_VIDEOS_BUTTON)
        self.driver.find_element_by_xpath(self.MY_VIDEOS_BUTTON).click()
        self.driver.switch_to_window(self.driver.window_handles[-1])
        return WebDriverWait(self.driver, 50, 0.1).until(
            lambda d: d.find_element_by_xpath(self.MY_VIDEOS_TITLE).get_attribute('href')
        )

    def press_settings(self):
        self.wait_element(self.SETINGS_BUTTON)
        self.driver.find_element_by_xpath(self.SETINGS_BUTTON).click()
        return self.driver.current_url

    def press_activity(self):
        self.wait_element(self.ACTIVITY_BUTTON)
        self.driver.find_element_by_xpath(self.ACTIVITY_BUTTON).click()
        return self.driver.current_url

    def subsc_on_user(self):
        wait = WebDriverWait(self.driver, 50)
        wait.until(expected_conditions.presence_of_element_located((By.XPATH, self.SUBSC_BUT_AD_USER)))
        self.driver.find_element_by_xpath(self.SUBSC_BUT_AD_USER).click()






