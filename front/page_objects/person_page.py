from functools import wraps

from selenium.webdriver.support.wait import WebDriverWait
from selenium.webdriver.support import expected_conditions as ec
from selenium.webdriver.common.by import By
from selenium.common.exceptions import WebDriverException, TimeoutException

from test.front.cover_saver import *
from test.front.front_config import USING_HTTPS
from test.front.util import rs

from .basic_page import BasicPage

class PersonPage(BasicPage):
    def __init__(self, driver, url=None):
        super().__init__(driver, url)
        self.name_text_id = "name"
        self.role_teacher_id = "role_teacher"
        self.role_student_id = "role_student"
        self.role_others_id = "role_others"
        self.gender_male_id = "gender_male"
        self.gender_female_id = "gender_female"
        self.gender_secret_id = "gender_secret"
        self.intro_text_id = "personalIntroduce"
        self.submit_btn_id = "modify"

        self.photo_exhibit_img_loc = (By.ID, "user_profile_photo")
        self.photo_open_dialog_btn_id = "show_modal"
        self.photo_open_file_input_id = "photoInput"
        self.photo_cancel_cross_btn_id = "close_modal"
        self.photo_submit_btn_xpath = "//div[@id='changeModal']//button[text()='提交']"
        self.photo_cancel_text_btn_id = "//div[@id='changeModal']//button[text()='取消']"

        self.role_dict = {
                "T": self.role_teacher_id,
                "S": self.role_student_id,
                "O": self.role_others_id,
        }        
        self.gender_dict = {
                "M": self.gender_male_id,
                "F": self.gender_female_id,
                "A": self.gender_secret_id,
        }

    def checkIsSelf(self):
        check_ids = [
            self.role_teacher_id,
            self.gender_male_id,
            self.intro_text_id
        ]
        for id in check_ids:
            self.waitAppear_ID(id)

    def getRoleValue(self):
        return self.getRatioValue(
            self.role_dict
        )

    def getGenderValue(self):
        return self.getRatioValue(
            self.gender_dict
        )

    def setRoleValue(self, value):
        self.setRatioValue(
            self.role_dict,
            value
        )

    def setGenderValue(self, value):
        self.setRatioValue(
            self.gender_dict,
            value
        )

    def getForm(self):
        rs()
        res = {}
        text = self.waitAppear_ID(self.name_text_id)
        res["name"] = text.text
        res["role"] = self.getRoleValue()
        res["gender"] = self.getGenderValue()
        text = self.waitAppear_ID(self.intro_text_id)
        res["intro"] = text.get_attribute("value")
        return res

    def setForm(self, form):
        if "role" in form.keys():
            self.setRoleValue(form["role"])
        if "gender" in form.keys():
            self.setGenderValue(form["gender"])
        if "intro" in form.keys():
            text = self.waitAppear_ID(self.intro_text_id)
            text.clear()
            text.send_keys(form["intro"])

    def submit(self):
        btn = self.waitAppear_ID(self.submit_btn_id)
        btn.click()
        self.alertAccept()

    def uploadPage_wholeProcess(self, image_path):
        btn = self.waitAppear_ID(self.photo_open_dialog_btn_id)
        btn.click()

        file_ctl = self.waitAppear_ID(self.photo_open_file_input_id)
        file_ctl.send_keys(image_path)

        rs()

        btn = self.waitAppear_xpath(self.photo_submit_btn_xpath)
        btn.click()
        self.alertAccept()

    def getImageURL(self) -> str:
        img_ctl = self.waitAppear(self.photo_exhibit_img_loc)
        src_text = img_ctl.get_attribute("src")
        return src_text
