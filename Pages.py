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


    def __init__(self, driver, PATH = ''):
        self.driver = driver
        self.PATH = PATH

    def open(self):
        url = urlparse.urljoin(self.BASE_URL, self.PATH)
        self.driver.get(url)
        self.driver.maximize_window()


class AuthPage(AnswersPage):
    #PATH = ''

    @property
    def form(self):
        return AuthForm(self.driver)

    @property
    def top_menu(self):
        return TopMenu(self.driver)


class MyRoomPage(AnswersPage):

    @property
    def my_room(self):
        return MyRoom(self.driver)

    @property
    def auth_form(self):
        return AuthForm(self.driver)

    @property
    def top_ask_question(self):
        return AskTop(self.driver)


class AskPage(AnswersPage):

    @property
    def auth_form(self):
        return AuthForm(self.driver)

    @property
    def question_form(self):
        return QuestionForm(self.driver)



class QuestionForm(Component):
    ID_TEXT_AREA = 'ask-text'
    SEC_TEXT_PATH = '//*[@id="ColumnCenter"]/div/div/form/div[3]/div/div[1]/div/textarea'
    QUESTION_TEXT = u'Как переключиться на iframe в Selenium, если у него нет имени и по xpath его не найти?'
    SECOND_TEXT = u'ЯП python'

    #не закончил тест задать вопрос
    def ask_question(self):
        #findmethods.Firefox.find_element_by_id('f').send_keys()
        self.driver.find_element_by_id(self.ID_TEXT_AREA).send_keys(self.QUESTION_TEXT)
        self.driver.find_element_by_xpath(self.SEC_TEXT_PATH).send_keys(self.SECOND_TEXT)





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
    AVATAR = '//span[@bem-id="192"]'

    def get_name(self):
        return WebDriverWait(self.driver, 30, 0.1).until(
            lambda d: d.find_element_by_id('PH_user-email').text
        )

    def go_to_my_room(self):
        self.driver.find_element_by_xpath(self.AVATAR).click()




class MyRoom(Component):
    MY_WORLD_BUTTON = '//a[text()="Мой мир"]'
    MY_WORLD_TITLE = '//a[@class="portal-menu__logo icon-head-logo booster-sc "]' #не забывай пробел на конце, где он есть

    MY_PHOTOS_BUTTON = '//a[text()="Фотографии"]'
    MY_VIDEOS_BUTTON = '//a[text()="Видео"]'

    MY_VIDEOS_TITLE = '//a[@class="sp-video__head__logo sp-video-icon-head-logo js-router-link"]'

    TAKE_VIP_BUTTON = '//span[text()="Получить VIP-статус"]'
    VIP_TITLE = '//span[text()="1. Ваш заказ: Продление VIP статуса на 10 дней [100.00 руб.]"]'

    SETINGS_BUTTON = '//a[text()="Настройки"]'

    ACTIVITY_BUTTON = '//a[text()="Активность"]'


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

    def take_vip(self):
        self.driver.find_element_by_xpath(self.TAKE_VIP_BUTTON).click()
        self.driver.implicitly_wait(5)
        print(self.driver.window_handles)
        #self.driver.switch_to_frame("relative=top")
        self.driver.switch_to.frame(self.driver.find_element(By.XPATH, "/html/body/div[3]/div/div[2]/iframe"));

        self.driver.find_element_by_xpath(self.VIP_TITLE)
        print (self.driver.find_element_by_xpath(self.VIP_TITLE).text)



        return  self.driver.current_url

    def press_settings(self):
        self.driver.find_element_by_xpath(self.SETINGS_BUTTON).click()
        return self.driver.current_url

    def press_activity(self):
        self.driver.find_element_by_xpath(self.ACTIVITY_BUTTON).click()
        return self.driver.current_url

