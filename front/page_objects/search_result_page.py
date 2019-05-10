from functools import wraps

from selenium.webdriver.support.wait import WebDriverWait
from selenium.webdriver.support import expected_conditions as ec
from selenium.webdriver.common.by import By
from selenium.common.exceptions import WebDriverException, TimeoutException

from test.front.cover_saver import *
from test.front.front_config import USING_HTTPS
from test.front.util import rs

from .basic_page import BasicPage

class SearchResultPage(BasicPage):
    def __init__(self, driver, url=None):
        super().__init__(driver, url)
        self.course_num = None
        self.course_divs = None
        self.course_list = None

        self.course_num_id = "serachedCourseNum"
        self.no_result_id = "noresult"

        self.course_detail_xpath = "//div[@id='course{0}']//a[@href='#']"

        self.course_big_div_id = "course_data"
        self.course_sub_divs_xpath = "./div"
        self.course_divs_xpath = "//div[starts-with(@id, 'course')]"
        self.course_name_xpath = "./div[1]/a"
        self.course_school_xpath = "./div[2]/div[1]//p"
        self.course_department_xpath = "./div[2]/div[2]//p"
        self.course_type_xpath = "./div[2]/div[3]//p"
        self.course_credit_xpath = "./div[2]/div[4]//p"

        self.course_rank_id = "rank_number_{0}"
        self.course_difficulty_id = "difficulty_score_{0}"
        self.course_funny_id = "funny_score_{0}"
        self.course_gain_id = "gain_score_{0}"
        self.course_recommend_id = "recommend_score_{0}"

        self.now_page_num_text_id = "pagenum"
        self.total_page_num_text_id = "totalpage"
        self.next_page_btn_xpath = "//li[@id='nextpage']/a"
        self.prev_page_btn_xpath = "//li[@id='lastpage']/a"
        self.jump_page_text_id = "jumpPage"
        self.jump_page_btn_xpath = "//nobr[@id='jump']/button"

    def checkIsSelf(self):
        self.waitAppear_ID(self.course_num_id)

    def goDetailPage(self, index):
        from .detail_page import DetailPage

        btn = self.waitAppear_xpath(self.course_detail_xpath.format(index))
        btn.click()
        return DetailPage(self.driver)

    def getAllCourseNum(self):
        if not self.course_num:
            self.course_num = int(self.waitAppear_ID(self.course_num_id).text)
        return self.course_num

    def getCourseNum(self):
        return len(self._getCourseDivs())

    def isNoResult(self):
        try:
            self.waitAppear_ID(self.no_result_id)
        except TimeoutException as e:
            return False
        return True

    def _getCourseDivs(self):
        if not self.course_divs:
            try:
                course_big_div = self.waitAppear_ID(self.course_big_div_id)
                self.course_divs = course_big_div.find_elements_by_xpath(self.course_sub_divs_xpath)
            except TimeoutException as e:
                if self.isNoResult():
                    self.course_divs = []
                    return self.course_divs
                else:
                    raise e
        return self.course_divs

    def searchCourseForIndex(self, course_name):
        course_list = self.getCourseList()
        for i in range(len(course_list)):
            if not "name" in course_list[i].keys():
                continue
            if course_list[i]["name"] == course_name:
                return i
        return None

    def getCourseDetail(self, index):
        if index >= self.getCourseNum():
            raise Exception("Too large index for getCourseDetail.")

        if self.course_list and len(self.course_list) > index:
            return self.course_list[index]

        div = self._getCourseDivs()[index]

        name = div.find_element_by_xpath(self.course_name_xpath).text
        school = div.find_element_by_xpath(self.course_school_xpath).text
        department = div.find_element_by_xpath(self.course_department_xpath).text
        k_type = div.find_element_by_xpath(self.course_type_xpath).text
        credit = float(div.find_element_by_xpath(self.course_credit_xpath).text)

        # TODO Here still to be developed
        # rank = int(div.find_element_by_id(self.course_rank_id.format(index)).text)
        # difficulty = int(div.find_element_by_id(self.course_difficulty_id.format(index)).text)
        # funny = int(div.find_element_by_id(self.course_funny_id.format(index)).text)
        # gain = int(div.find_element_by_id(self.course_gain_id.format(index)).text)
        # recommend = int(div.find_element_by_id(self.course_recommend_id.format(index)).text)

        return {
            "name": name,
            "school": school,
            "department": department,
            "type": k_type,
            "credit": credit,
            # TODO like above todo
            # "rank": rank,
            # "difficulty": difficulty,
            # "funny": funny,
            # "gain": gain,
            # "recommend": recommend
        }

    def getCourseList(self):
        if self.course_list:
            return self.course_list

        self.course_list = []
        for i in range(self.getCourseNum()):
            res_dict = self.getCourseDetail(i)
            self.course_list.append(res_dict)
        return self.course_list

    def isCourseShow(self, index=None, name=None):
        if index == None and name == None:
            raise Exception("Must assign either index or name")
        if index != None and name != None:
            raise Exception("Cannot assign both index and name")

        if name != None:
            index = self.searchCourseForIndex(name)
            if index == None:
                raise Exception("Course {0} not exists.".format(name))

        if index >= self.getCourseNum():
            raise Exception("Index {0} is too large.".format(index))
        div = self._getCourseDivs()[index]
        return not ("none" in div.get_attribute("style"))
            
    def prevPage(self):
        btn = self.waitAppear_xpath(self.prev_page_btn_xpath)
        btn.click()

    def nextPage(self):
        btn = self.waitAppear_xpath(self.next_page_btn_xpath)
        btn.click()

    def getNowPageNum(self):
        return self.waitAppear_ID(self.now_page_num_text_id).text

    def getTotalPageNum(self):
        return self.waitAppear_ID(self.total_page_num_text_id)

    def jumpPage(self, index):
        text = self.waitAppear_ID(self.jump_page_text_id)
        text.send_keys(str(index))
        btn = self.waitAppear_xpath(self.jump_page_btn_xpath)
        btn.click()
