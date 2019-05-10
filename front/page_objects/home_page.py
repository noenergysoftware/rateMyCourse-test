from functools import wraps

from selenium.webdriver.support.wait import WebDriverWait
from selenium.webdriver.support import expected_conditions as ec
from selenium.webdriver.common.by import By
from selenium.common.exceptions import WebDriverException, TimeoutException

from test.front.cover_saver import *
from test.front.front_config import USING_HTTPS
from test.front.util import rs

from .basic_page import BasicPage
from .search_result_page import SearchResultPage

class HomePage(BasicPage):
    def __init__(self, driver, url=None):
        super().__init__(driver, url)
        self.search_box_id = "searchboxCourse"
        self.search_btn_id = "buttonSearchCourse"

        self.select_department_btn_id = "buttonSelectDepartment"
        self.department_list_id = "departments"

    def checkIsSelf(self):
        check_ids = [
            self.search_box_id,
            self.select_department_btn_id
        ]
        for id in check_ids:
            self.waitAppear_ID(id)

    def goHomePage(self):
        raise NotImplementedError

    def selectDepartmentByText(self, depa_name):
        btn = self.waitAppear_ID(self.select_department_btn_id)
        btn.click()
        depa_list = self.waitAppear_ID(self.department_list_id)
        href = depa_list.find_element_by_link_text(depa_name)
        href.click()

    def search(self, s):
        return self.searchEnter(s)

    def searchEnter(self, s):
        box = self.waitAppear_ID(self.search_box_id)
        box.send_keys(s + "\n")
        return SearchResultPage(self.driver)

    def searchButton(self, s):
        box = self.waitAppear_ID(self.search_box_id)
        box.send_keys(s)
        btn = self.waitAppear_ID(self.search_btn_id)
        btn.click()
        return SearchResultPage(self.driver)