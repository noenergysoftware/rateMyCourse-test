from functools import wraps

from selenium.webdriver.support.wait import WebDriverWait
from selenium.webdriver.support import expected_conditions as ec
from selenium.webdriver.common.by import By
from selenium.common.exceptions import WebDriverException, TimeoutException

from test.front.cover_saver import *
from test.front.front_config import USING_HTTPS
from test.front.util import rs

from .basic_page import BasicPage
from .split_base_page import SplitBasePage
from .comment_page import CommentPage

class DetailPage(SplitBasePage):
    def __init__(self, driver, url=None):

        self.name_text_id = "course_name"
        self.credit_text_id = "course_credit"
        self.school_text_id = "course_school"
        self.type_text_id = "course_type"
        self.description_text_id = "coursedescription"

        self.comment_page_btn_id = "toComment"
        self.comment_username_xpath = "./div[1]/p"
        self.comment_teachername_xpath = "./table[1]/tbody/tr/td[2]/p"
        self.comment_content_xpath = "./div[2]/p"
        self.comment_time_xpath = "./div[3]/a[last()]/p"

        def getForm(block):
            res = {}
            temp = {
                "username": self.comment_username_xpath,
                "teachername": self.comment_teachername_xpath,
                "content": self.comment_content_xpath,
                "time": self.comment_time_xpath
            }
            for key, xpath in temp.items():
                res[key] = block.find_element_by_xpath(xpath).text
            return res

        super().__init__(
            driver,
            url,
            prev_btn_loc        =(By.XPATH, "//li[@id='lastpage']/a"),
            next_btn_loc        =(By.XPATH, "//li[@id='nextpage']/a"),
            jump_text_loc       =(By.ID, "jumpPage"),
            jump_btn_loc        =(By.XPATH, "//nobr[@id='jump']/button"),
            now_index_text_loc  =(By.ID, "pagenum"),
            max_index_text_loc  =(By.ID, "totalpage"),
            block_div_loc       =(By.ID, "comment"),
            block_relative_loc  =(By.XPATH, "./div"),
            form_get_method     =getForm,
        )


    def checkIsSelf(self):
        check_ids = [
            self.credit_text_id,
        ]
        for id in check_ids:
            self.waitAppear_ID(id)

    def goCommentPage(self):
        btn = self.waitAppear_ID(self.comment_page_btn_id)
        btn.click()
        return CommentPage(self.driver)

    def isCommentShow(self, index):
        if index >= self.getBlockNum():
            raise Exception("Index {0} is too large.".format(index))
        block = self.getBlocks()[index]
        return not ("none" in block.get_attribute("style"))