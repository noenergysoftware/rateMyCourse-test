from functools import wraps

from selenium.webdriver.support.wait import WebDriverWait
from selenium.webdriver.support import expected_conditions as ec
from selenium.webdriver.common.by import By
from selenium.common.exceptions import WebDriverException, TimeoutException

from test.front.cover_saver import *
from test.front.front_config import USING_HTTPS
from test.front.util import rs

from .basic_page import BasicPage

class RegistPage(BasicPage):
    def __init__(self, driver, url=None):
        super().__init__(driver, url)
        self.home_page_btn_xpath = "//a[@href='./index.html']"
        self.login_page_btn_xpath = "//a[@href='./login.html']"

        self.name_text_id = "name"
        self.email_text_id = "email"
        self.password_text_id = "passwd"
        self.repassword_text_id = "repasswd"
        self.identity_btn_id = "TencentCaptcha"
        self.submit_signup_btn_id = "tos"

    def checkIsSelf(self):
        self.waitAppear_ID(self.submit_signup_btn_id)

    def goRegistPage(self):
        raise NotImplementedError

    def goHomePage(self):
        from .home_page import HomePage

        btn = self.waitAppear_xpath(self.home_page_btn_xpath)
        btn.click()
        return HomePage(self.driver)

    def goLoginPage(self):
        from .login_page import LoginPage

        btn = self.waitAppear_xpath(self.login_page_btn_xpath)
        btn.click()
        return LoginPage(self.driver)

    def fillForm(self, name=None, email=None, password=None, repassword=None):
        if name:
            text = self.waitAppear_ID(self.name_text_id)
            text.send_keys(name)
        if email:
            text = self.waitAppear_ID(self.email_text_id)
            text.send_keys(email)
        if password:
            text = self.waitAppear_ID(self.password_text_id)
            text.send_keys(password)
        if repassword:
            text = self.waitAppear_ID(self.repassword_text_id)
            text.send_keys(repassword)

    def submit(self):
        from .login_page import LoginPage

        btn = self.waitAppear_ID(self.identity_btn_id)
        btn.click()
        btn = self.waitAppear_ID(self.submit_signup_btn_id)
        btn.click()
        self.alertAccept()
        return LoginPage(self.driver)
