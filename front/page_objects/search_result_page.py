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

class SearchResultPage(SplitBasePage):
    def __init__(self, driver, url=None):

        self.course_divs_xpath = "//div[starts-with(@id, 'course')]"
        self.course_name_xpath = "./div[1]/a"
        self.course_school_xpath = "./div[2]/div[1]/div[1]/div[2]"
        self.course_department_xpath = "./div[2]/div[1]/div[2]/div[2]"
        self.course_type_xpath = "./div[2]/div[1]/div[3]/div[2]"
        self.course_credit_xpath = "./div[2]/div[1]/div[4]/div[2]"

        # self.course_rank_id = "rank_number_{0}"
        self.course_difficulty_id = "difficulty_score_"
        self.course_funny_id = "funny_score_"
        self.course_gain_id = "gain_score_"
        self.course_recommend_id = "recommend_score_"

        def getForm(block):
            res = {}
            text_dict = {
                "name": self.course_name_xpath,
                "school": self.course_school_xpath,
                "department": self.course_department_xpath,
                "type": self.course_type_xpath,
            }
            for key, xpath in text_dict.items():
                res[key] = block.find_element_by_xpath(xpath).text
            res["credit"] = float(block.find_element_by_xpath(self.course_credit_xpath).text)

            def getScore(div):
                stars = div.find_elements_by_xpath("./img")
                score = 0
                for star in stars:
                    src_attr = star.get_attribute("src")
                    if "on" in src_attr:
                        score += 1
                    elif not "off" in src_attr:
                        raise Exception("a src without on and off: {0}".foramt(src_attr))
                return score

            rank_dict = {
                "difficulty": self.course_difficulty_id,
                "funny": self.course_funny_id,
                "gain": self.course_gain_id,
                "recommend": self.course_recommend_id,
            }
            for key, ctl_id in rank_dict.items():
                res[key] = getScore(block.find_element_by_xpath("//div[starts-with(@id, \"{0}\")]".format(ctl_id)))

            return res


        super().__init__(
            driver,
            url,
            prev_btn_loc        = (By.XPATH, "//li[@id='lastpage']"),
            next_btn_loc        = (By.XPATH, "//li[@id='nextpage']"),
            # jump_text_loc       = (By.ID, "jumpPage"),
            # jump_btn_loc        = (By.XPATH, "//nobr[@id='jump']/button"),
            split_btn_loc_temp  = (By.ID, "page{0}"),
            split_btn_div_loc   = (By.ID, "c_pagination"),
            prev_dot_loc        = (By.ID, "page_dot"),
            next_dot_loc        = (By.ID, "page_dot2"),
            now_index_text_loc  = (By.ID, "pagenum"),
            max_index_text_loc  = (By.ID, "totalpage"),
            block_div_loc       = (By.ID, "course_data"),
            block_relative_loc  = (By.XPATH, "./div"),
            form_get_method     = getForm
        )


        self.course_num = None

        self.course_num_id = "serachedCourseNum"
        self.no_result_id = "noresult"

        self.course_detail_xpath = "//div[@id='course{0}']//a[@href='#']"


    def checkIsSelf(self):
        self.waitAppear_ID(self.course_num_id)

    def goDetailPage(self, index):
        from .detail_page import DetailPage

        btn = self.waitAppear_xpath(self.course_detail_xpath.format(index))
        btn.click()
        return DetailPage(self.driver)

    def getCourseNum(self):
        if not self.course_num:
            self.course_num = int(self.waitAppear_ID(self.course_num_id).text)
        return self.course_num

    def isNoResult(self):
        try:
            self.waitAppear_ID(self.no_result_id)
        except TimeoutException as e:
            return False
        return True

    def searchBlockByCourseName(self, course_name):
        for i in range(self.getBlockNum()):
            form = self.getBlockForm(i)
            if not "name" in form.keys():
                continue
            if form["name"] == course_name:
                return i
        return None
