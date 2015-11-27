# -*- coding: utf-8 -*-
import os
import time
from Pages import  AskPage, MyRoomPage, AuthPage, QuestionSubscribe
from unittest import TestCase
from selenium.webdriver import DesiredCapabilities, Remote
__author__ = 'ivansemenov'


class SimpleTest(TestCase):
    question_subscribe_path = 'question/184708481'
    CENTRE_FORM_SUBSC_QUESR_PATH = 'profile/id207816682/feed/questions'
    #FIRST_U_PASSWORD = os.environ['TTHA2PASSWORD']
    FIRST_U_PASSWORD = 'testirovanie'
    FIRST_USER_EMAIL = 'stotch_leopold@inbox.ru'
    FIRST_PROFILE_ID = 'profile/id207816682/'

    #SECOND_U_PASSWORD = os.environ['TTHA2PASSWORD']
    SECOND_U_PASSWORD = 'testirovanie'
    SECOND_U_EMAIL = 'lepold.kot@mail.ru'
    SECOND_PROFILE_ID = 'profile/id211914728/'

    QUESTION_TEXT = u'Любишь мечтать? О чем мечтаешь?'
    SECOND_TEXT = u'Что тебя больше всего рассмешило за прошедшую неделю/ месяц?'
    CATEGORY_NAME = 'Программирование'
    SUBCATEGORY_NAME = 'JavaScript'


    def auth_of_user(self, my_room_page):

        auth_form = my_room_page.auth_form
        auth_form.open_form()
        auth_form.set_login(self.FIRST_USER_EMAIL)
        auth_form.set_password(self.FIRST_U_PASSWORD)
        auth_form.submit()

        self.driver.switch_to_window(self.driver.window_handles[-1])

    def auth_user_askpage(self, page):
        auth_form = page.auth_form
        auth_form.set_login(self.FIRST_USER_EMAIL)
        auth_form.set_password(self.FIRST_U_PASSWORD)
        auth_form.submit()

        self.driver.switch_to_window(self.driver.window_handles[-1])


    def setUp(self):
        browser = os.environ.get('TTHA2BROWSER', 'CHROME')

        self.driver = Remote(
            command_executor='http://127.0.0.1:4444/wd/hub',
            desired_capabilities=getattr(DesiredCapabilities, browser).copy()
        )



    def tearDown(self):
        time.sleep(1)
        self.driver.quit()






    # проверяем добовление пользователя во вкладке подписке, при подписке на него, не менять местами с нижним тестом
    def test_add_subscribe_user(self):
        my_room_page = MyRoomPage(self.driver, PATH=self.SECOND_PROFILE_ID)
        my_room_page.open()

        self.auth_of_user(my_room_page)
        my_room = my_room_page.my_room
        my_room.subsc_on_user()

        my_room_page = MyRoomPage(self.driver, PATH=self.FIRST_PROFILE_ID)
        my_room_page.open()

        cent_form = my_room_page.center_form
        cent_form.go_subsc_question_form()
        cent_form.open_subsc_user_list()
        result = cent_form.find_subsc_user()
        self.assertEquals(result, True)


    # проверяем удаление пользователя из подписок
    def test_delete_user_from_subscr(self):
        my_room_page = MyRoomPage(self.driver, PATH=self.FIRST_PROFILE_ID)
        my_room_page.open()

        self.auth_of_user(my_room_page)

        cent_form = my_room_page.center_form
        cent_form.go_subsc_question_form()
        cent_form.open_subsc_user_list()
        cent_form.delete_subscr_user()
        result = cent_form.is_it_del_user()
        self.assertEquals(result, True)





    # проверяем добовляется ли вопрос во вкладке подписки и роботоспособность всех кнопок перехода,  не менять местами с нижним тестом
    # def test_add_subscribe_question(self):
    #     subsc_question_page = QuestionSubscribe(self.driver, PATH=self.question_subscribe_path)
    #     subsc_question_page.open()
    #
    #     self.auth_of_user(subsc_question_page)
    #
    #     subsc_button = subsc_question_page.subscribe_question_top_form
    #     subsc_button.add_subscribe_on_question()
    #
    #     my_room_page = MyRoomPage(self.driver, PATH=self.FIRST_PROFILE_ID)
    #     my_room_page.open()
    #
    #     cent_form = my_room_page.center_form
    #     cent_form.go_subsc_question_form()
    #     href = cent_form.go_subsc_questions()
    #
    #     self.assertEquals('https://otvet.mail.ru/' + self.question_subscribe_path, href)

    # проверяем проподает ли вопрос из вкладки при отписке
    # def test_delete_subscribe_question(self):
    #     my_room_page = MyRoomPage(self.driver, PATH=self.FIRST_PROFILE_ID)
    #     my_room_page.open()
    #
    #     self.auth_of_user(my_room_page)
    #
    #     cent_form = my_room_page.center_form
    #     cent_form.go_subsc_question_form()
    #     cent_form.delete_subsc_quest()
    #     answer = cent_form.is_it_del()
    #     self.assertEquals(answer, True)






    # def test_ask_question(self):
    #      ask_page = AskPage(self.driver, PATH='ask')
    #      ask_page.open()
    #
    #      self.auth_user_askpage(ask_page)
    #
    #      ask_form = ask_page.question_form
    #      ask_form.set_question(self.QUESTION_TEXT, self.SECOND_TEXT)
    #      ask_form.set_category(self.CATEGORY_NAME)
    #      ask_form.set_subcategory(self.SUBCATEGORY_NAME)
    #      ask_form.publicate_question()
    #      time.sleep(20)
    #      url_question = ask_form.get_url_question()
    #
    #      my_room_page = MyRoomPage(self.driver, PATH=self.FIRST_PROFILE_ID)
    #      my_room_page.open()
    #
    #
    #      center_form = my_room_page.center_form
    #
    #      href = center_form.last_quest_in_all()
    #
    #      self.assertEquals(url_question, href)
    #
    #      center_form.go_to_open_question()
    #      href = center_form.last_quest_in_open()
    #
    #      self.assertEquals(url_question, href)





    # def test_ask_question_button(self):
    #     my_room_page = MyRoomPage(self.driver, PATH=self.FIRST_PROFILE_ID)
    #     my_room_page.open()
    #
    #     self.auth_of_user(my_room_page)
    #
    #     my_room = my_room_page.top_ask_question
    #     url = my_room.ask_question_button()
    #     self.assertEquals(url, 'https://otvet.mail.ru/ask')
    # #
    # #
    # #
    # def test_go_to_MyWorld(self):
    #     my_room_page = MyRoomPage(self.driver, PATH=self.FIRST_PROFILE_ID)
    #     my_room_page.open()
    #
    #
    #     self.auth_of_user(my_room_page)
    #
    #     my_room = my_room_page.my_room
    #     href = my_room.go_to_my_world()
    #     self.assertEquals(href, 'http://my.mail.ru/')
    # #
    #
    # def test_authorization(self):
    #     auth_page = AuthPage(self.driver)
    #     auth_page.open()
    #     auth_form = auth_page.form
    #     auth_form.open_form()
    #     auth_form.set_login(self.FIRST_USER_EMAIL)
    #     auth_form.set_password(self.FIRST_U_PASSWORD)
    #     auth_form.submit()
    #
    #     top_menu = auth_page.top_menu
    #     name = top_menu.get_name()
    #     print (name)
    #     self.assertEquals(name, self.FIRST_USER_EMAIL)
    #
    #
    # def test_go_to_photos(self):
    #     my_room_page = MyRoomPage(self.driver, PATH=self.FIRST_PROFILE_ID)
    #     my_room_page.open()
    #
    #     self.auth_of_user(my_room_page)
    #
    #     my_room = my_room_page.my_room
    #     href = my_room.go_to_photos()
    #     self.assertEquals(href, 'http://my.mail.ru/')
    #
    #
    # def test_go_to_videos(self):
    #     my_room_page = MyRoomPage(self.driver, PATH=self.FIRST_PROFILE_ID)
    #     my_room_page.open()
    #
    #     self.auth_of_user(my_room_page)
    #
    #     my_room = my_room_page.my_room
    #     href = my_room.go_to_videos()
    #
    #     self.assertEquals(href, 'https://my.mail.ru/video')
    #
    #
    # def test_press_settings_button(self):
    #     my_room_page = MyRoomPage(self.driver, PATH=self.FIRST_PROFILE_ID)
    #     my_room_page.open()
    #
    #     self.auth_of_user(my_room_page)
    #
    #     my_room = my_room_page.my_room
    #     url = my_room.press_settings()
    #     self.assertEquals(url, 'https://otvet.mail.ru/settings')

    # разное поведение в хроме и файерфоксе
    # def test_press_activity_button(self):
    #     my_room_page = MyRoomPage(self.driver, PATH=self.FIRST_PROFILE_ID)
    #     my_room_page.open()
    #
    #     self.auth_of_user(my_room_page)
    #     first_url = self.driver.current_url
    #
    #     my_room = my_room_page.my_room
    #
    #     my_room.press_settings()
    #     my_room.press_activity()
    #
    #     second_url = self.driver.current_url
    #     self.assertEquals(first_url.encode(), second_url.encode() + '?from=authpopup')



