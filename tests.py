# -*- coding: utf-8 -*-
import os
from pages.main_page import MainPage
from unittest import TestCase
from selenium.webdriver import DesiredCapabilities, Remote
__author__ = 'ivansemenov'


class AnswersTest(TestCase):
    FIRST_U_NAME = u'Леопольд Стотч'
    FIRST_USER_EMAIL = 'stotch_leopold@inbox.ru'
    FIRST_U_PASSWORD = os.environ['TTHA2PASSWORD']

    def setUp(self):
        browser = os.environ.get('TTHA2BROWSER', 'CHROME')

        self.driver = Remote(
            command_executor='http://127.0.0.1:4444/wd/hub',
            desired_capabilities=getattr(DesiredCapabilities, browser).copy()
        )

    def test_authorization(self):
        main_page = MainPage(self.driver)
        main_page.open()

        auth_form = main_page.auth_form
        auth_form.open_form()
        auth_form.set_login(self.FIRST_USER_EMAIL)
        auth_form.set_password(self.FIRST_U_PASSWORD)
        auth_form.submit()

        top_menu = main_page.top_menu

        name = top_menu.get_name()

        self.assertEqual(name, self.FIRST_USER_EMAIL)

    def test_vip(self):
        main_page = MainPage(self.driver,)
        main_page.open()

        auth_form = main_page.auth_form
        auth_form.open_form()
        auth_form.set_login(self.FIRST_USER_EMAIL)
        auth_form.set_password(self.FIRST_U_PASSWORD)
        auth_form.submit()

        top_menu = main_page.top_menu
        room_page = top_menu.go_to_my_room()

        left_block = room_page.left_block
        left_block.get_vip()
        self.assertEqual(True, left_block.buy_vip_frame_exist())

        left_block.close_vip()
        auth_form.logout()

    def test_my_world(self):
        main_page = MainPage(self.driver)
        main_page.open()

        auth_form = main_page.auth_form
        auth_form.open_form()
        auth_form.set_login(self.FIRST_USER_EMAIL)
        auth_form.set_password(self.FIRST_U_PASSWORD)
        auth_form.submit()

        top_menu = main_page.top_menu
        room_page = top_menu.go_to_my_room()
        left_block = room_page.left_block
        href = left_block.go_to_my_world()
        self.assertEqual(u'http://my.mail.ru/',href)
        name = left_block.get_name_by_my_world()
        self.assertEqual(self.FIRST_U_NAME, name)
        auth_form.logout()

    def test_my_photos(self):
        main_page = MainPage(self.driver)
        main_page.open()

        auth_form = main_page.auth_form
        auth_form.open_form()
        auth_form.set_login(self.FIRST_USER_EMAIL)
        auth_form.set_password(self.FIRST_U_PASSWORD)
        auth_form.submit()

        top_menu = main_page.top_menu
        room_page = top_menu.go_to_my_room()
        left_block = room_page.left_block
        href = left_block.go_to_photos()
        self.assertEqual(u'http://my.mail.ru/', href)
        category = left_block.is_photos()
        self.assertEqual(u'Фотографии', category)
        auth_form.logout()

    def test_my_videos(self):
        main_page = MainPage(self.driver)
        main_page.open()

        auth_form = main_page.auth_form
        auth_form.open_form()
        auth_form.set_login(self.FIRST_USER_EMAIL)
        auth_form.set_password(self.FIRST_U_PASSWORD)
        auth_form.submit()

        top_menu = main_page.top_menu
        room_page = top_menu.go_to_my_room()
        left_block = room_page.left_block
        href = left_block.go_to_videos()
        self.assertEqual(True, left_block.is_videos())
        auth_form.logout()

    def test_subscribe_question(self):
        main_page = MainPage(self.driver)
        main_page.open()

        auth_form = main_page.auth_form
        auth_form.open_form()
        auth_form.set_login(self.FIRST_USER_EMAIL)
        auth_form.set_password(self.FIRST_U_PASSWORD)
        auth_form.submit()

        top_menu = main_page.top_menu
        room_page = top_menu.go_to_my_room()
        center_block = room_page.center_block
        last_count = center_block.get_subscribe_count_questions()

        main_page.open()
        question_block = main_page.center_block
        question_page = question_block.choose_last_question()

        question = question_page.question
        question_title = question.get_title()
        question.subscribe()

        top_menu.go_to_my_room()
        under_count = center_block.get_subscribe_count_questions()
        self.assertEqual(int(under_count)-int(last_count), 1)

        center_block.go_to_subcribes_question()

        self.assertEqual(True, center_block.check_question(question_title))

        center_block.unsubscribe_question(question_title)

        auth_form.logout()

    def test_unsubscribe_question(self):
        main_page = MainPage(self.driver)
        main_page.open()

        auth_form = main_page.auth_form
        auth_form.open_form()
        auth_form.set_login(self.FIRST_USER_EMAIL)
        auth_form.set_password(self.FIRST_U_PASSWORD)
        auth_form.submit()

        top_menu = main_page.top_menu
        room_page = top_menu.go_to_my_room()
        center_block = room_page.center_block
        first_count = center_block.get_subscribe_count_questions()

        main_page.open()
        question_block = main_page.center_block
        question_page = question_block.choose_last_question()

        question = question_page.question
        question_title = question.get_title()
        question.subscribe()

        top_menu.go_to_my_room()

        center_block.go_to_subcribes_question()
        center_block.unsubscribe_question(question_title)

        under_count = center_block.get_subscribe_count_questions()
        self.assertEqual(int(first_count), int(under_count))
        auth_form.logout()

    def test_subscribe_user(self):
        main_page = MainPage(self.driver)
        main_page.open()

        auth_form = main_page.auth_form
        auth_form.open_form()
        auth_form.set_login(self.FIRST_USER_EMAIL)
        auth_form.set_password(self.FIRST_U_PASSWORD)
        auth_form.submit()

        top_menu = main_page.top_menu
        room_page = top_menu.go_to_my_room()
        center_block = room_page.center_block
        first_count = center_block.get_subscribe_count_users()

        main_page.open()
        question_block = main_page.center_block
        user_room_page = question_block.choose_last_author_quest()

        left_block = user_room_page.left_block
        user_id = left_block.get_user_id()
        left_block.subcribe()
        top_menu.go_to_my_room()
        current_count = center_block.get_subscribe_count_users()

        self.assertEqual(int(current_count)-int(first_count), 1)

        center_block.go_to_subcribes_users()

        self.assertEqual(True, center_block.check_user(user_id))

        center_block.unsubscribe_user(user_id)
        auth_form.logout()

    def test_unsubscribe_user(self):
        main_page = MainPage(self.driver)
        main_page.open()

        auth_form = main_page.auth_form
        auth_form.open_form()
        auth_form.set_login(self.FIRST_USER_EMAIL)
        auth_form.set_password(self.FIRST_U_PASSWORD)
        auth_form.submit()

        top_menu = main_page.top_menu
        room_page = top_menu.go_to_my_room()
        center_block = room_page.center_block
        first_count = center_block.get_subscribe_count_users()

        main_page.open()
        question_block = main_page.center_block
        user_room_page = question_block.choose_last_author_quest()

        left_block = user_room_page.left_block
        user_id = left_block.get_user_id()
        left_block.subcribe()
        top_menu.go_to_my_room()
        center_block.go_to_subcribes_users()
        center_block.unsubscribe_user(user_id)

        current_count = center_block.get_subscribe_count_users()
        self.assertEqual(int(first_count), int(current_count))
        auth_form.logout()

    def test_settings_button(self):
        main_page = MainPage(self.driver)
        main_page.open()

        auth_form = main_page.auth_form
        auth_form.open_form()
        auth_form.set_login(self.FIRST_USER_EMAIL)
        auth_form.set_password(self.FIRST_U_PASSWORD)
        auth_form.submit()

        top_menu = main_page.top_menu
        my_room = top_menu.go_to_my_room()

        left_block = my_room.left_block
        url = left_block.press_settings()
        self.assertEquals(url, 'https://otvet.mail.ru/settings')
        auth_form.logout()

    def test_activity_button(self):
        main_page = MainPage(self.driver)
        main_page.open()

        auth_form = main_page.auth_form
        auth_form.open_form()
        auth_form.set_login(self.FIRST_USER_EMAIL)
        auth_form.set_password(self.FIRST_U_PASSWORD)
        auth_form.submit()

        top_menu = main_page.top_menu
        my_room = top_menu.go_to_my_room()

        left_block = my_room.left_block
        start_url = self.driver.current_url
        left_block.press_settings()
        left_block.press_activity()
        finish_url = self.driver.current_url
        self.assertEquals(start_url.encode(), finish_url.encode())
        auth_form.logout()

    def test_chech_pay_delete_question(self):
        main_page = MainPage(self.driver)
        main_page.open()

        auth_form = main_page.auth_form
        auth_form.open_form()
        auth_form.set_login(self.FIRST_USER_EMAIL)
        auth_form.set_password(self.FIRST_U_PASSWORD)
        auth_form.submit()

        top_menu = main_page.top_menu
        my_room = top_menu.go_to_my_room()

        center_block = my_room.center_block
        center_block.go_to_questions()
        ques_page = center_block.choose_last_my_open_question()
        question = ques_page.question

        self.assertEqual(True, question.is_delete())
        question.close_popup()
        auth_form.logout()

    def test_not_auth_subcribe_user(self):
        main_page = MainPage(self.driver)
        main_page.open()

        center_block = main_page.center_block

        another_room = center_block.choose_last_author_quest()
        left_block = another_room.left_block

        left_block.subcribe()

        self.assertEqual(False, center_block.is_authorizate())

    def test_not_auth_subcribe_question(self):
        main_page = MainPage(self.driver)
        main_page.open()

        center_block = main_page.center_block

        question_page = center_block.choose_last_question()
        question = question_page.question

        question.subscribe()

        self.assertEqual(False, center_block.is_authorizate())

    def test_not_auth_gift_vip(self):
        main_page = MainPage(self.driver)
        main_page.open()

        center_block = main_page.center_block

        another_room = center_block.choose_last_author_quest()
        left_block = another_room.left_block

        left_block.gift_vip()

        self.assertEqual(False, center_block.is_authorizate())

    def tearDown(self):
        self.driver.quit()
