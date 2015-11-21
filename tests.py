# -*- coding: utf-8 -*-
import os
import time
from Pages import *
from unittest import TestCase
from selenium.webdriver import DesiredCapabilities, Remote
__author__ = 'ivansemenov'


class SimpleTest(TestCase):
    PASSWORD = 'testirovanie'
    USER_EMAIL = 'stotch_leopold@inbox.ru'

    def setUp(self):
        browser = os.environ.get('TTHA2BROWSER', 'FIREFOX')

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
        auth_form.set_login(self.USER_EMAIL)
        auth_form.set_password(self.PASSWORD)
        auth_form.submit()

        top_menu = auth_page.top_menu
        name = top_menu.get_name()
        self.assertEquals(name, self.USER_EMAIL)



    def test_go_to_MyWorld(self):
        my_room_page = MyRoomPage(self.driver)
        my_room_page.open()

        my_room = my_room_page.my_room
        href = my_room.go_to_my_world()
        self.assertEquals(href, 'http://my.mail.ru/')

    def test_go_to_photos(self):
        my_room_page = MyRoomPage(self.driver)
        my_room_page.open()

        my_room = my_room_page.my_room
        href = my_room.go_to_photos()
        self.assertEquals(href, 'http://my.mail.ru/')


    def test_go_to_videos(self):
        my_room_page = MyRoomPage(self.driver)
        my_room_page.open()

        my_room = my_room_page.my_room
        href = my_room.go_to_videos()
        print (href)
        self.assertEquals(href, 'http://my.mail.ru/video')




