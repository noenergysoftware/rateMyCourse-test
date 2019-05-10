from selenium.webdriver.common.by import By
from selenium.common.exceptions import WebDriverException, TimeoutException

from test.front.cover_saver import *
from test.front.front_config import USING_HTTPS
from test.front.util import rs

from .basic_page import BasicPage

class CommentPage(BasicPage):
    def __init__(self, driver, url=None):
        super().__init__(driver, url)
        self.comment_textarea_id = "comment"
        self.select_teacher_list_id = "buttonSelectTeacher"
        self.teacher_list_xpath = "//ul[@id='teacherlist']/li[{0}]/a"
        self.submit_btn_text = "提交"

    def checkIsSelf(self):
        check_ids = [
            self.comment_textarea_id,
            self.select_teacher_list_id
        ]
        for id in check_ids:
            self.waitAppear_ID(id)

    def editComment(self, s):
        textarea = self.waitAppear_ID(self.comment_textarea_id)
        textarea.send_keys(s)

    def selectTeacher(self, index):
        btn = self.waitAppear_ID(self.select_teacher_list_id)
        btn.click()
        list_item = self.waitAppear_xpath(self.teacher_list_xpath.format(index+1))
        list_item.click()

    def submitComment(self):
        from .detail_page import DetailPage

        btn = self.waitAppear_text(self.submit_btn_text)
        btn.click()
        self.alertAccept()
        return DetailPage(self.driver)
        