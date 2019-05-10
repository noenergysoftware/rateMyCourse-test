from functools import wraps

from selenium.webdriver.support.wait import WebDriverWait
from selenium.webdriver.support import expected_conditions as ec
from selenium.webdriver.common.by import By
from selenium.common.exceptions import WebDriverException, TimeoutException

from test.front.cover_saver import *
from test.front.front_config import USING_HTTPS
from test.front.util import rs

from .basic_page import BasicPage
from .comment_page import CommentPage

class DetailPage(BasicPage):
    def __init__(self, driver, url=None):
        super().__init__(driver, url)
        self.comment_divs = None

        self.name_text_id = "course_name"
        self.credit_text_id = "course_credit"
        self.school_text_id = "course_school"
        self.type_text_id = "course_type"
        self.description_text_id = "coursedescription"

        self.comment_big_div_id = "comment"
        self.comment_sub_divs_xpath = "./div"
        self.comment_username_xpath = "./div[1]/p"
        self.comment_teachername_xpath = "./table[1]/tbody/tr/td[2]/p"
        self.comment_content_xpath = "./div[2]/p"
        self.comment_time_xpath = "./div[3]/a[last()]/p"

        self.comment_page_btn_id = "toComment"

        self.now_page_num_text_id = "pagenum"
        self.total_page_num_text_id = "totalpage"
        self.next_page_btn_xpath = "//li[@id='nextpage']/a"
        self.prev_page_btn_xpath = "//li[@id='lastpage']/a"
        self.jump_page_text_id = "jumpPage"
        self.jump_page_btn_xpath = "//nobr[@id='jump']/button"

    def splitedPageChange(f):
        @wraps(f)
        def wrap_func(self):
            self.comment_divs = None
            return f(self)
        return wrap_func

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

    def _getCommentDivs(self):
        if not self.comment_divs:
            comment_div = self.waitAppear_ID(self.comment_big_div_id)
            self.comment_divs = comment_div.find_elements_by_xpath(self.comment_sub_divs_xpath)
        return self.comment_divs

    def getCommentNum(self):
        return len(self._getCommentDivs())

    def getCommentForm(self, index):
        div = self._getCommentDivs()[index]
        res = {}
        temp = {
            "username": self.comment_username_xpath,
            "teachername": self.comment_teachername_xpath,
            "content": self.comment_content_xpath,
            "time": self.comment_time_xpath
        }
        for key, xpath in temp.items():
            res[key] = div.find_element_by_xpath(xpath).text
        return res

    def isCommentShow(self, index):
        if index >= self.getCommentNum():
            raise Exception("Index {0} is too large.".format(index))
        div = self._getCommentDivs()[index]
        return not ("none" in div.get_attribute("style"))
            
    @splitedPageChange
    def prevPage(self):
        btn = self.waitAppear_xpath(self.prev_page_btn_xpath)
        btn.click()

    @splitedPageChange
    def nextPage(self):
        btn = self.waitAppear_xpath(self.next_page_btn_xpath)
        btn.click()

    @splitedPageChange
    def jumpPage(self, index):
        text = self.waitAppear_ID(self.jump_page_text_id)
        text.send_keys(str(index))
        btn = self.waitAppear_xpath(self.jump_page_btn_xpath)
        btn.click()

    def getNowPageNum(self):
        return int(self.waitAppear_ID(self.now_page_num_text_id).text)

    def getTotalPageNum(self):
        return int(self.waitAppear_ID(self.total_page_num_text_id).text)
