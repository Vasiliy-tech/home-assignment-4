# -*- coding: utf-8 -*-
from base import AnswersPage, Component
__author__ = 'ivansemenov'


class AnotherRoomPage(AnswersPage):

    @property
    def left_block(self):
        return LeftAnotherRoomBlock(self.driver)


class LeftAnotherRoomBlock(Component):
    SUBCRIBE_USER = '//span[text()="Подписаться"]'
    GIFT_VIP = '//span[text()="Подарить VIP-статус"]'

    def get_user_id(self):
        self.wait_element(self.SUBCRIBE_USER)
        return self.driver.current_url.split('/')[-2]

    def subcribe(self):
        self.wait_element(self.SUBCRIBE_USER)
        self.driver.find_element_by_xpath(self.SUBCRIBE_USER).click()

    def gift_vip(self):
        self.wait_element(self.GIFT_VIP)
        self.driver.find_element_by_xpath(self.GIFT_VIP).click()