from selenium.webdriver.support.wait import WebDriverWait
from selenium.webdriver.support import expected_conditions as ec
from selenium.webdriver.common.by import By
from selenium.common.exceptions import WebDriverException
from cover_saver import *


class BasicPage:
    cover_count = 0

    def __init__(self, driver, url=None):
        self.driver = driver
        if url:
            if FS_COVER:
                try:
                    cover_saver.trySaveCoverageReport(driver)
                except WebDriverException as e:
                    # TODO The driver's first get must have such an exception presently,
                    #   Try to remove this
                    pass
            driver.get("http://" + url)
        self.login_page_btn_id = "signIn"
        self.regist_page_btn_id = "signUp"
        self.home_page_btn_xpath = "//a[@href='index.html']"
        self.person_page_btn_id = "personalInfo"
        self.logout_btn_id = "logOut"

    def clearCookies(self):
        self.driver.delete_all_cookies()

    def waitAppear(self, locator):
        return WebDriverWait(self.driver, 10).until(
            ec.visibility_of_element_located(
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

    def goHomePage(self):
        btn = self.waitAppear_xpath(self.home_page_btn_xpath)
        btn.click()
        return HomePage(self.driver)

    def goLoginPage(self):
        btn = self.waitAppear_ID(self.login_page_btn_id)
        btn.click()
        return LoginPage(self.driver)

    def goRegistPage(self):
        btn = self.waitAppear_ID(self.regist_page_btn_id)
        btn.click()
        return RegistPage(self.driver)

    def goPersonPage(self):
        btn = self.waitAppear_ID(self.person_page_btn_id)
        btn.click()
        return PersonPage(self.driver)

    def logout(self):
        btn = self.waitAppear_ID(self.logout_btn_id)
        btn.click()
        self.alertAccept()
        return HomePage(self.driver)

class HomePage(BasicPage):
    def __init__(self, driver, url=None):
        super().__init__(driver, url)
        self.search_box_id = "searchboxCourse"
        self.select_department_btn_id = "buttonSelectDepartment"
        self.search_btn_id = "buttonSearchCourse"

    def checkIsSelf(self):
        check_ids = [
            self.search_box_id,
            self.select_department_btn_id
        ]
        for id in check_ids:
            self.waitAppear_ID(id)

    def goHomePage(self):
        raise NotImplementedError

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

class LoginPage(BasicPage):
    def __init__(self, driver, url=None):
        super().__init__(driver, url)
        self.home_page_btn_xpath = "//a[@href='index.html']"
        self.regist_page_btn_xpath = "//a[@href='signup.html']"

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
        name_text = self.waitAppear_ID(self.name_text_id)
        name_text.send_keys(name)
        password_text = self.waitAppear_ID(self.password_text_id)
        password_text.send_keys(password)
        btn = self.waitAppear_ID(self.login_btn_id)
        btn.click()
        self.alertAccept()
        return HomePage(self.driver)


class SearchResultPage(BasicPage):
    def __init__(self, driver, url=None):
        super().__init__(driver, url)
        self.course_num_id = "serachedCourseNum"
        self.course_detail_xpath = "//div[@id='course{0}']//a[@href='#']"

    def checkIsSelf(self):
        self.waitAppear_ID(self.course_num_id)

    def goDetailPage(self, index):
        btn = self.waitAppear_xpath(self.course_detail_xpath.format(index))
        btn.click()
        return DetailPage(self.driver)


class RegistPage(BasicPage):
    def __init__(self, driver, url=None):
        super().__init__(driver, url)
        self.home_page_btn_xpath = "//a[@href='index.html']"
        self.login_page_btn_xpath = "//a[@href='login.html']"

        self.name_text_id = "name"
        self.email_text_id = "email"
        self.password_text_id = "passwd"
        self.repassword_text_id = "repasswd"
        self.submit_signup_btn_id = "tos"

    def checkIsSelf(self):
        self.waitAppear_ID(self.submit_signup_btn_id)

    def goRegistPage(self):
        raise NotImplementedError

    def goHomePage(self):
        btn = self.waitAppear_xpath(self.home_page_btn_xpath)
        btn.click()
        return HomePage(self.driver)

    def goLoginPage(self):
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
        btn = self.waitAppear_ID(self.submit_signup_btn_id)
        btn.click()
        self.alertAccept()
        return LoginPage(self.driver)

class PersonPage(BasicPage):
    def __init__(self, driver, url=None):
        super().__init__(driver, url)
        self.name_text_id = "name"
        self.role_text_id = "role"
        self.gender_text_id = "gender"
        self.intro_text_id = "personalIntroduce"

    def checkIsSelf(self):
        check_ids = [
            self.role_text_id,
            self.gender_text_id,
            self.intro_text_id
        ]
        for id in check_ids:
            self.waitAppear_ID(id)

    def getForm(self):
        res = {}
        text = self.waitAppear_ID(self.name_text_id)
        res["name"] = text.get_attribute("value")
        text = self.waitAppear_ID(self.role_text_id)
        res["role"] = text.get_attribute("value")
        text = self.waitAppear_ID(self.gender_text_id)
        res["gender"] = text.get_attribute("value")
        text = self.waitAppear_ID(self.intro_text_id)
        res["intro"] = text.get_attribute("value")
        return res


class DetailPage(BasicPage):
    def __init__(self, driver, url=None):
        super().__init__(driver, url)
        self.comment_divs = None

        self.name_text_id = "course_name"
        self.credit_text_id = "course_credit"
        self.school_text_id = "course_school"
        self.type_text_id = "course_type"
        self.description_text_id = "coursedescription"

        self.comment_div_xpath = "//body/div[2]/div/div[position()>=3 and position() < last()]"
        self.comment_username_xpath = "./div[1]/p"
        self.comment_teachername_xpath = "./table[1]/tbody/tr/td[2]/p"
        self.comment_content_xpath = "./div[2]/p"
        self.comment_time_xpath = "./div[3]/a[last()]/p"

        self.comment_page_btn_id = "toComment"

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

    def getCommentNumber(self):
        if not self.comment_divs:
            self.comment_divs = self.driver.find_elements_by_xpath(self.comment_div_xpath)
        return len(self.comment_divs)

    def getCommentForm(self, index):
        if not self.comment_divs:
            self.comment_divs = self.driver.find_elements_by_xpath(self.comment_div_xpath)
        div = self.comment_divs[index]
        res = {}
        temp = {
            "username": self.comment_username_xpath,
            "teachername": self.comment_teachername_xpath,
            "content": self.comment_content_xpath,
            "time": self.comment_time_xpath
        }
        for key, id in temp.items():
            res[key] = div.find_element_by_xpath(id).text
        return res


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
        btn = self.waitAppear_text(self.submit_btn_text)
        btn.click()
        self.alertAccept()
        return DetailPage(self.driver)
        