
from unittest import skip

from django.test import tag

from test.front.page_objects import *
from test.front.user_actions import *
from test.front.util import rs
from .front_basic import FrontBasicTC, TAG_DB_MODIFY, TAG_FRONT, TAG_SPLIT


@tag(TAG_FRONT)
class FrontFuncLogInTC(FrontBasicTC):
    def test_login_exist_user(self):
        page = HomePage(self.driver, self.domain)
        try:
            page = page.goLoginPage()
            page = page.logIn("hong", "hong")
            page.checkIsSelf()
        finally:
            self.driver.delete_all_cookies()

    def test_login_not_exist_user(self):
        page = HomePage(self.driver, self.domain)
        try:
            page = page.goLoginPage()
            page = page.logIn("test_login_not_exist_user", "test_login_not_exist_user")
            page = LoginPage(self.driver)
            page.checkIsSelf()
        finally:
            self.driver.delete_all_cookies()

    def test_person(self):
        page = HomePage(self.driver, self.domain)
        with LogStatus(page, "ming", "ming") as page:
            page = page.goPersonPage()
            page.checkIsSelf()
            form = page.getForm()
            self.assertEqual(form["name"], "ming")
            self.assertEqual(form["role"], "S")
            self.assertEqual(form["gender"], "M")
            self.assertEqual(form["intro"], "mingming")

    @tag(TAG_DB_MODIFY)
    def test_comment(self):
        test_words = "test_login_comment_is_mine"

        page = HomePage(self.driver, self.domain)
        with LogStatus(page, "hong", "hong") as page:
            page = page.search("rbq")
            page = page.goDetailPage(0)
            page = page.goCommentPage()
            page.editComment(test_words)
            page.selectTeacher(0)
            page = page.submitComment()

            now_index = page.getNowIndex()
            max_index = page.getMaxIndex()
            global_exist_flag = False
            while now_index <= max_index:
                block_num = page.getBlockNum()
                exp_dict = {
                    "username": "hong",
                    "teachername": "rbq",
                    "content": test_words
                }
            
                exist = False
                for i in range(block_num):
                    form = page.getBlockForm(i)
                    equal = True
                    for key, value in exp_dict.items():
                        if form[key] != value:
                            equal = False
                            break
                    if equal:
                        exist = True
                        break
                if exist:
                    global_exist_flag = True
                    break
                
                page.nextSplit()
                now_index += 1
            self.assertTrue(global_exist_flag, "Submitted Comment not Exist.")


@tag(TAG_FRONT)
class FrontFuncRegistTC(FrontBasicTC):
    def test_regist_exist_user(self):
        page = HomePage(self.driver, self.domain)
        page = page.goRegistPage()
        page.fillForm(
            name="rbq",
            email="rbq@test.com",
            password="abc123!@#",
            repassword="abc123!@#",
        )
        page.submit() # Should still be RegistPage
        rs(min=3)
        page.checkIsSelf()

    @tag(TAG_DB_MODIFY)
    def test_regist_not_exist_user(self):
        test_name = "__TRNEU__"
        test_pw = "abc123!@#"
        page = HomePage(self.driver, self.domain)
        page = page.goRegistPage()
        page.fillForm(
            name=test_name,
            email="regist_not_exist_user@test.com",
            password=test_pw,
            repassword=test_pw,
        )
        page = page.submit()
        page.checkIsSelf()
        page = page.logIn(test_name, test_pw)
        page.checkIsSelf()
        self.driver.delete_all_cookies()


@tag(TAG_FRONT)
class FrontFuncLogOutTC(FrontBasicTC):
    def checkIsLogOut(self, page):
        btn = page.waitAppear_ID(page.login_page_btn_id)

    def test_home(self):
        page = HomePage(self.driver, self.domain)
        with LogStatus(page, "rbq", "rbq") as page:
            page = page.logout()
            page.checkIsSelf()
            self.checkIsLogOut(page)

    def test_search(self):
        page = HomePage(self.driver, self.domain)
        with LogStatus(page, "rbq", "rbq") as page:
            page = page.search("rbq")
            page = page.logout()
            page.checkIsSelf()
            self.checkIsLogOut(page)

    def test_detail(self):
        page = HomePage(self.driver, self.domain)
        with LogStatus(page, "rbq", "rbq") as page:
            page = page.search("rbq")
            page = page.goDetailPage(0)
            page = page.logout()
            page.checkIsSelf()
            self.checkIsLogOut(page)

    def test_comment(self):
        page = HomePage(self.driver, self.domain)
        with LogStatus(page, "rbq", "rbq") as page:
            page = page.search("rbq")
            page = page.goDetailPage(0)
            page = page.goCommentPage()
            page = page.logout()
            page.checkIsSelf()
            self.checkIsLogOut(page)


@tag(TAG_FRONT)
class FrontFuncSearchTC(FrontBasicTC):
    def checkCourseExist(self, page, course_name):
        # TODO change split to check all results
        return page.searchBlockByCourseName(course_name) != None

    def checkCourseNotExist(self, page, course_name):
        return not self.checkCourseExist(page, course_name)

    def checkNoResult(self, page):
        return page.isNoResult()

    def test_search_exist(self):
        page = HomePage(self.driver, self.domain)
        page = page.search("rbq")
        self.checkCourseExist(page, "rbq")

    def test_search_not_exist(self):
        page = HomePage(self.driver, self.domain)
        page = page.search("test_course_not_exist")
        self.checkNoResult(page)

    def test_no_spec(self):
        page = HomePage(self.driver, self.domain)
        page = page.search("")
        course_names_list = [
            "rbq",
            "论持久战",
            "第三次世界大战",
            "如何进牢子"
        ]
        for course_name in course_names_list:
            self.checkCourseExist(page, course_name)

    def test_only_spec_department(self):
        page = HomePage(self.driver, self.domain)
        page.selectDepartmentByText("派出所")
        page = page.search("")
        self.checkCourseExist(page, "如何进牢子")
        self.checkCourseNotExist(page, "rbq")
        self.checkCourseNotExist(page, "论持久战")

    def test_spec_depa_and_name_exist(self):
        page = HomePage(self.driver, self.domain)
        page.selectDepartmentByText("Office")
        page = page.search("第三次世界大战")
        self.checkCourseExist(page, "第三次世界大战")
        self.assertEqual(page.getCourseNum(), 1)

    def test_spec_depa_and_name_not_exist(self):
        page = HomePage(self.driver, self.domain)
        page.selectDepartmentByText("Office")
        page = page.search("如何进牢子")
        self.checkNoResult(page)


@tag(TAG_FRONT)
class FrontFuncSplitPageTC(FrontBasicTC):
    def setUp(self):
        super().setUp()

    def getBlockForms(self, page:SplitBasePage):
        res = []
        for i in range(page.getBlockNum()):
            res.append(page.getBlockForm(i))
        return res

    def generalTest(self, num_per_page:int, page:SplitBasePage):
        block_forms_1 = []
        block_forms_2 = []
        block_forms_3 = []

        with self.subTest(case_name="init"):
            self.assertEquals(page.getBlockNum(), num_per_page)
            block_forms_1 = self.getBlockForms(page)

        with self.subTest(case_name="next_page"):
            page.nextSplit()
            self.assertEquals(page.getBlockNum(), num_per_page)
            block_forms_2 = self.getBlockForms(page)
            self.assertNotEquals(block_forms_1, block_forms_2)

        with self.subTest(case_name="prev_page"):
            page.prevSplit()
            block_forms = self.getBlockForms(page)
            self.assertEquals(block_forms_1, block_forms)

        with self.subTest(case_name="jump_page"):
            page.jumpSplit(3)
            block_forms_3 = self.getBlockForms(page)
            self.assertNotEquals(block_forms_1, block_forms_3)
            self.assertNotEquals(block_forms_2, block_forms_3)

    def test_search_page(self):
        '''This testcase need at least three pages.
        '''
        page = HomePage(self.driver, self.domain)
        page = page.search("")
        self.generalTest(
            num_per_page=5,
            page=page,
        )

    @tag("kkk")
    def test_detail_page(self):
        '''This testcase need at least three pages.
        '''
        page = HomePage(self.driver, self.domain)
        page = page.search("rbq")
        page = page.goDetailPage(0)
        self.generalTest(
            num_per_page=5,
            page=page,
        )