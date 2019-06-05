from functools import wraps

from selenium.webdriver.support.wait import WebDriverWait
from selenium.webdriver.support import expected_conditions as ec
from selenium.webdriver.common.by import By
from selenium.common.exceptions import WebDriverException, TimeoutException

from test.front.cover_saver import *
from test.front.front_config import USING_HTTPS
from test.front.util import rs

from .basic_page import BasicPage
from .home_page import HomePage
from .regist_page import RegistPage

class LoginPage(BasicPage):
    def __init__(self, driver, url=None):
        super().__init__(driver, url)
        self.home_page_btn_xpath = "//a[@href='./index.html']"
        self.regist_page_btn_xpath = "//a[@href='./signup.html']"

        self.name_text_id = "name"
        self.password_text_id = "password"
        self.login_btn_id = "login"

    def checkIsSelf(self):
        self.waitAppear_ID(self.login_btn_id)

    def goLoginPage(self):
        raise NotImplementedError

    def goHomePage(self):
        btn = self.waitAppear_xpath(self.home_page_btn_xpath)
        btn.click()
        return HomePage(self.driver)

    def goRegistPage(self):
        btn = self.waitAppear_xpath(self.regist_page_btn_xpath)
        btn.click()
        return RegistPage(self.driver)

    def logIn(self, name, password):
        rs()
        name_text = self.waitAppear_ID(self.name_text_id)
        name_text.send_keys(name)
        password_text = self.waitAppear_ID(self.password_text_id)
        password_text.send_keys(password)
        btn = self.waitAppear_ID(self.login_btn_id)
        btn.click()
        self.alertAccept()
        return HomePage(self.driver)

