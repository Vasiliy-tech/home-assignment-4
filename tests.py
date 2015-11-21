# -*- coding: utf-8 -*-
import os
import time
from Pages import *
from unittest import TestCase
from selenium.webdriver import DesiredCapabilities, Remote
__author__ = 'ivansemenov'


class SimpleTest(TestCase):
    FIRST_U_PASSWORD = 'testirovanie'
    FIRST_USER_EMAIL = 'stotch_leopold@inbox.ru'
    FIRST_PROFILE_ID = 'profile/id207816682/'

    def auth_of_first_user(self, my_room_page):

        auth_form = my_room_page.auth_form
        auth_form.open_form()
        auth_form.set_login(self.FIRST_USER_EMAIL)
        auth_form.set_password(self.FIRST_U_PASSWORD)
        auth_form.submit()

        self.driver.switch_to_window(self.driver.window_handles[-1]) #почему без этой строчки крашиться не совсем понятно, т.к простая авторизация работает

    def setUp(self):
        browser = os.environ.get('TTHA2BROWSER', 'FIREFOX')

        self.driver = Remote(
            command_executor='http://127.0.0.1:4444/wd/hub',
            desired_capabilities=getattr(DesiredCapabilities, browser).copy()
        )


    def tearDown(self):
        time.sleep(1)
        self.driver.quit()


    def test_go_to_MyWorld(self):
        my_room_page = MyRoomPage(self.driver, PATH=self.FIRST_PROFILE_ID)
        my_room_page.open()
        #print(self.driver.current_url)

        self.auth_of_first_user(my_room_page)

        my_room = my_room_page.my_room
        href = my_room.go_to_my_world()
        self.assertEquals(href, 'http://my.mail.ru/')


    def test_authorization(self):
        auth_page = AuthPage(self.driver)
        auth_page.open()
        auth_form = auth_page.form
        auth_form.open_form()
        auth_form.set_login(self.FIRST_USER_EMAIL)
        auth_form.set_password(self.FIRST_U_PASSWORD)
        auth_form.submit()

        top_menu = auth_page.top_menu
        name = top_menu.get_name()
        self.assertEquals(name, self.FIRST_USER_EMAIL)


    def test_go_to_photos(self):
        my_room_page = MyRoomPage(self.driver, PATH=self.FIRST_PROFILE_ID)
        my_room_page.open()

        self.auth_of_first_user(my_room_page)

        my_room = my_room_page.my_room
        href = my_room.go_to_photos()
        self.assertEquals(href, 'http://my.mail.ru/')


    def test_go_to_videos(self):
        my_room_page = MyRoomPage(self.driver, PATH=self.FIRST_PROFILE_ID)
        my_room_page.open()

        self.auth_of_first_user(my_room_page)

        my_room = my_room_page.my_room
        href = my_room.go_to_videos()

        self.assertEquals(href, 'https://my.mail.ru/video')


    def test_press_settings_button(self):
        my_room_page = MyRoomPage(self.driver, PATH=self.FIRST_PROFILE_ID)
        my_room_page.open()

        self.auth_of_first_user(my_room_page)

        my_room = my_room_page.my_room
        url = my_room.press_settings()
        self.assertEquals(url, 'https://otvet.mail.ru/settings')


    def test_press_activity_button(self):
        my_room_page = MyRoomPage(self.driver, PATH=self.FIRST_PROFILE_ID)
        my_room_page.open()

        self.auth_of_first_user(my_room_page)
        first_url = self.driver.current_url

        my_room = my_room_page.my_room

        my_room.press_settings()
        my_room.press_activity()

        second_url = self.driver.current_url
        self.assertEquals(first_url.encode(), second_url.encode() + '?from=authpopup')


