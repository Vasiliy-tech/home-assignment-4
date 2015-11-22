# -*- coding: utf-8 -*-
import os
from Pages import *
from unittest import TestCase
from selenium.webdriver import DesiredCapabilities, Remote
__author__ = 'ivansemenov'



class SimpleTest(TestCase):
    FIRST_U_PASSWORD = 'testirovanie'
    FIRST_USER_EMAIL = 'stotch_leopold@inbox.ru'
    FIRST_USER_FIR_AND_SEC_NAME = u'Леопольд Стотч'

    SECOND_U_PASSWORD = 'testirovanie'
    SECOND_U_EMAIL = 'lepold.kot@mail.ru'

    QUESTION_TEXT = u'Traceback most я на iframe в Selenium?'
    SECOND_TEXT = u'FAIL: test_ask_question (tests.SimpleTest)по xpath его не найти'
    CATEGORY_NAME = 'Программирование'
    SUBCATEGORY_NAME = 'JavaScript'

    def setUp(self):
        browser = os.environ.get('TTHA2BROWSER', 'CHROME')

        self.driver = Remote(
            command_executor='http://127.0.0.1:4444/wd/hub',
            desired_capabilities=getattr(DesiredCapabilities, browser).copy()
        )

    def tearDown(self):
        time.sleep(1)
        self.driver.quit()

    def test_authorization(self):
        auth_page = AuthPage(self.driver)
        auth_page.open()

        auth_form = auth_page.form
        auth_form.open_form()
        auth_form.set_login(self.FIRST_USER_EMAIL)
        auth_form.set_password(self.FIRST_U_PASSWORD)
        auth_form.submit()

        top_menu = auth_page.top_menu
        login = top_menu.get_name()
        self.assertEqual(self.FIRST_USER_EMAIL, login)

    def test_ask_question(self):
        auth_page = AuthPage(self.driver)
        auth_page.open()
        auth_page.login(self.FIRST_USER_EMAIL, self.FIRST_U_PASSWORD)

        ask_page = AskPage(self.driver)

        ask_page.open()
        ask_form = ask_page.question_form
        ask_form.set_question(self.QUESTION_TEXT, self.SECOND_TEXT)
        ask_form.set_category(self.CATEGORY_NAME)
        ask_form.set_subcategory(self.SUBCATEGORY_NAME)
        ask_form.publicate_question()
        # time.sleep(10)  #бывает нужно ввести капчу, еще нужно менять вопросы
        url_question = ask_form.get_url_question()

        my_room_page = auth_page.top_menu.go_to_my_room()
        center_form = my_room_page.center_form
        href = center_form.last_quest_in_all()
        self.assertEquals(url_question, href)
        center_form.go_to_open_question()
        href = center_form.last_quest_in_open()
        self.assertEquals(url_question, href)

    def test_ask_question_button(self):
        auth_page = AuthPage(self.driver)
        auth_page.open()
        auth_page.login(self.FIRST_USER_EMAIL, self.FIRST_U_PASSWORD)
        my_room_page = auth_page.top_menu.go_to_my_room()
        my_room = my_room_page.top_ask_question
        url = my_room.ask_question_button()
        self.assertEquals(url, 'https://otvet.mail.ru/ask')

    def test_go_to_MyWorld(self):     #TODO Done
        auth_page = AuthPage(self.driver)
        auth_page.open()
        auth_page.login(self.FIRST_USER_EMAIL, self.FIRST_U_PASSWORD)
        my_room_page = auth_page.top_menu.go_to_my_room()
        my_room = my_room_page.my_room
        href = my_room.go_to_my_world()
        self.assertEquals(href, 'http://my.mail.ru/')
        self.assertEqual(self.FIRST_USER_FIR_AND_SEC_NAME, my_room.get_name_on_my_world())

    def test_go_to_photos(self):     #TODO done
        auth_page = AuthPage(self.driver)
        auth_page.open()
        auth_page.login(self.FIRST_USER_EMAIL,self.FIRST_U_PASSWORD)
        my_room_page = auth_page.top_menu.go_to_my_room()
        my_room = my_room_page.my_room
        href = my_room.go_to_photos()
        self.assertEquals(href, 'http://my.mail.ru/')
        self.assertEqual(u'Фотографии', my_room.get_title_on_photos())

    def test_go_to_videos(self):      #TODO Done
        auth_page = AuthPage(self.driver)
        auth_page.open()
        auth_page.login(self.FIRST_USER_EMAIL, self.FIRST_U_PASSWORD)
        my_room_page = auth_page.top_menu.go_to_my_room()
        my_room = my_room_page.my_room
        href = my_room.go_to_videos()
        self.assertEquals(href, 'https://my.mail.ru/video')

    def test_press_settings_button(self): #TODO Done
        auth_page = AuthPage(self.driver)
        auth_page.open()
        auth_page.login(self.FIRST_USER_EMAIL, self.FIRST_U_PASSWORD)
        my_room_page = auth_page.top_menu.go_to_my_room()

        my_room = my_room_page.my_room
        url = my_room.press_settings()
        self.assertEquals(url, 'https://otvet.mail.ru/settings')

    def test_press_activity_button(self):
        auth_page = AuthPage(self.driver)
        auth_page.open()
        auth_page.login(self.FIRST_USER_EMAIL, self.FIRST_U_PASSWORD)
        my_room_page = auth_page.top_menu.go_to_my_room()

        first_url = self.driver.current_url

        my_room = my_room_page.my_room

        my_room.press_settings()
        my_room.press_activity()

        second_url = self.driver.current_url
        self.assertEquals(first_url.encode(), second_url.encode() + '?from=authpopup')




