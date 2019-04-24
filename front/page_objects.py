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
        self.course_num = None
        self.course_divs = None
        self.course_list = None

        self.course_num_id = "serachedCourseNum"
        self.course_div_id = "course{0}"

        self.course_detail_xpath = "//div[@id='course{0}']//a[@href='#']"

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
        btn = self.waitAppear_xpath(self.course_detail_xpath.format(index))
        btn.click()
        return DetailPage(self.driver)

    def getCourseNum(self):
        if not self.course_num:
            self.course_num = int(self.waitAppear_ID(self.course_num_id).text)
        return self.course_num

    def _getCourseDivs(self):
        if not self.course_divs:
            self.course_divs = self.driver.find_elements_by_xpath(self.course_divs_xpath)
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

        self.now_page_num_text_id = "pagenum"
        self.total_page_num_text_id = "totalpage"
        self.next_page_btn_xpath = "//li[@id='nextpage']/a"
        self.prev_page_btn_xpath = "//li[@id='lastpage']/a"
        self.jump_page_text_id = "jumpPage"
        self.jump_page_btn_xpath = "//nobr[@id='jump']/button"

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

    def getCommentNum(self):
        if not self.comment_divs:
            self.comment_divs = self.driver.find_elements_by_xpath(self.comment_div_xpath)
        return len(self.comment_divs)

    def _getCommentDivs(self):
        if not self.comment_divs:
            self.comment_divs = self.driver.find_elements_by_xpath(self.comment_div_xpath)
        return self.comment_divs

    def getCommentForm(self, index):
        div = self._getCommentDivs()[index]
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

    def isCommentShow(self, index):
        if index >= self.getCommentNum():
            raise Exception("Index {0} is too large.".format(index))
        div = self._getCommentDivs()[index]
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
        