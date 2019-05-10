from selenium.webdriver.support.wait import WebDriverWait
from selenium.webdriver.support import expected_conditions as ec
from selenium.webdriver.common.by import By
from selenium.common.exceptions import WebDriverException, TimeoutException

from test.front.cover_saver import *
from test.front.front_config import USING_HTTPS
from test.front.util import rs

from .util import navbar

class BasicPage:
    cover_count = 0

    def __init__(self, driver, url=None):
        self.driver = driver
        if url:
            if USING_HTTPS:
                driver.get("https://" + url)
            else:
                driver.get("http://" + url)

        self.nav_bar_btn_xpath = "//div[@id='navbarContainer']/button"
        self.login_page_btn_id = "signIn"
        self.regist_page_btn_id = "signUp"
        self.home_page_btn_xpath = "//div[@id='navbarContainer']/a[1]"
        self.person_page_btn_id = "personalInfo"
        self.logout_btn_id = "logOut"

    def clearCookies(self):
        self.driver.delete_all_cookies()

    def waitAppear(self, locator):
        return WebDriverWait(self.driver, 10).until(
            ec.visibility_of_element_located(
                locator
        ))

    def waitPresence(self, locator):
        return WebDriverWait(self.driver, 10).until(
            ec.presence_of_element_located(
                locator
        ))

    def waitAppear_ID(self, id):
        return self.waitAppear((By.ID, id))

    def waitAppear_text(self, text):
        return self.waitAppear((By.LINK_TEXT, text))

    def waitAppear_xpath(self, xpath):
        return self.waitAppear((By.XPATH, xpath))

    def alertAccept(self):
        WebDriverWait(self.driver, 10).until(
            ec.alert_is_present()
        )
        alert = self.driver.switch_to.alert
        alert.accept()

    def openNavBar(self):
        dom = self.waitPresence((By.XPATH, self.nav_bar_btn_xpath))
        if dom.is_displayed():
            dom.click()

    def getRatioValue(self, id_dict):
        for key, ctl_id in id_dict.items():
            if self.waitAppear_ID(ctl_id).is_selected():
                return key
        return None

    def setRatioValue(self, id_dict, value):
        if value in id_dict.keys():
            ctl = self.waitAppear_ID(id_dict[value])
            if not ctl.is_selected():
                ctl.click()

    def goHomePage(self):
        from .home_page import HomePage
        btn = self.waitAppear_xpath(self.home_page_btn_xpath)
        btn.click()
        return HomePage(self.driver)

    @navbar
    def goLoginPage(self):
        from .login_page import LoginPage
        btn = self.waitAppear_ID(self.login_page_btn_id)
        btn.click()
        return LoginPage(self.driver)

    @navbar
    def goRegistPage(self):
        from .regist_page import RegistPage
        btn = self.waitAppear_ID(self.regist_page_btn_id)
        btn.click()
        return RegistPage(self.driver)

    @navbar
    def goPersonPage(self):
        from .person_page import PersonPage
        btn = self.waitAppear_ID(self.person_page_btn_id)
        btn.click()
        return PersonPage(self.driver)

    @navbar
    def logout(self):
        from .home_page import HomePage
        btn = self.waitAppear_ID(self.logout_btn_id)
        btn.click()
        self.alertAccept()
        return HomePage(self.driver)
