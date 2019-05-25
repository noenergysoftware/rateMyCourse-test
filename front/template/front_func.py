from contextlib import contextmanager
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

    @skip
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
    @tag(TAG_DB_MODIFY)
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

    @contextmanager
    def LogAndCheckLogOut(self, name="rbq", password="rbq") -> HomePage:
        try:
            page = HomePage(self.driver, self.domain)
            with LogStatus(page, name, password) as page:
                yield page
                page = page.logout()
                page.checkIsSelf()
                self.checkIsLogOut(page)
        finally:
            pass

    def test_home(self):
        with self.LogAndCheckLogOut() as page:
            pass

    def test_search(self):
        with self.LogAndCheckLogOut() as page:
            page = page.search("rbq")

    def test_detail(self):
        with self.LogAndCheckLogOut() as page:
            page = page.search("rbq")
            page = page.goDetailPage(0)

    def test_comment(self):
        with self.LogAndCheckLogOut() as page:
            page = page.search("rbq")
            page = page.goDetailPage(0)
            page = page.goCommentPage()

    def test_person(self):
        with self.LogAndCheckLogOut() as page:
            page = page.goPersonPage()


@tag(TAG_FRONT)
class FrontFuncSearchTC(FrontBasicTC):
    def checkCourseExist(self, page, course_name):
        # TODO change split to check all results
        return page.searchBlockByCourseName(course_name) != None

    def checkCourseNotExist(self, page, course_name):
        return not self.checkCourseExist(page, course_name)

    def checkNoResult(self, page):
        return page.isNoResult()

    def test_spec_no(self):
        page = HomePage(self.driver, self.domain)
        page = page.search("")
        course_names_list = [
            "rbq",
            "论持久战",
            "第三次世界大战",
            "如何进牢子"
        ]
        rs()
        for course_name in course_names_list:
            self.checkCourseExist(page, course_name)

    def test_spec_depa_exist(self):
        page = HomePage(self.driver, self.domain)
        page.selectDepartmentByText("派出所")
        page = page.search("")
        self.checkCourseExist(page, "如何进牢子")
        self.checkCourseNotExist(page, "rbq")
        self.checkCourseNotExist(page, "论持久战")

    def test_spec_name_not_exist(self):
        page = HomePage(self.driver, self.domain)
        page = page.search("test_course_not_exist")
        self.checkNoResult(page)

    def test_spec_name_exist_single(self):
        page = HomePage(self.driver, self.domain)
        page = page.search("rbq")
        self.checkCourseExist(page, "rbq")

    def test_spec_depa_name_not_exist_not_belong(self):
        page = HomePage(self.driver, self.domain)
        page.selectDepartmentByText("Office")
        page = page.search("如何进牢子")
        self.checkNoResult(page)

    def test_spec_depa_name_exist_single(self):
        page = HomePage(self.driver, self.domain)
        page.selectDepartmentByText("Office")
        page = page.search("第三次世界大战")
        self.checkCourseExist(page, "第三次世界大战")
        self.assertEqual(page.getCourseNum(), 1)


@tag(TAG_FRONT)
class FrontFuncSplitPageTC(FrontBasicTC):
    '''This testcase need at least 9 pages.
    '''

    def setUp(self):
        super().setUp()

    def getBlockForms(self, page:SplitBasePage):
        res = []
        for i in range(page.getBlockNum()):
            res.append(page.getBlockForm(i))
        return res

    def generalTest(self, num_per_page:int, page:SplitBasePage):
        block_forms_list = {}

        rs()
        with self.subTest(case_name="init"):
            self.assertEquals(page.getBlockNum(), num_per_page)
            block_forms_list[1] = self.getBlockForms(page)

            page.checkBtnShow()

        with self.subTest(case_name="next_page"):
            # Operation
            page.nextSplit()

            # Content Check
            self.assertEquals(page.getBlockNum(), num_per_page)
            block_forms_list[2] = self.getBlockForms(page)
            self.assertNotEquals(block_forms_list[1], block_forms_list[2])

            # Split btn show check
            page.checkBtnShow()

        with self.subTest(case_name="prev_page"):
            page.prevSplit()

            block_forms = self.getBlockForms(page)
            self.assertEquals(block_forms_list[1], block_forms)

            page.checkBtnShow()

        # with self.subTest(case_name="jump_page"):
            # page.jumpSplit(3)
            # block_forms_3 = self.getBlockForms(page)
            # self.assertNotEquals(block_forms_1, block_forms_3)
            # self.assertNotEquals(block_forms_2, block_forms_3)
        
        with self.subTest(case_name="first2last_page"):
            page.jumpSplit(page.getMaxIndex())

            block_forms_list[page.getMaxIndex()] = self.getBlockForms(page)
            self.assertNotEquals(block_forms_list[page.getMaxIndex()], block_forms_list[1])

            page.checkBtnShow()

        with self.subTest(case_name="last2first_page"):
            page.jumpSplit(1)

            block_forms = self.getBlockForms(page)
            self.assertEquals(block_forms, block_forms_list[1])

            page.checkBtnShow()

        with self.subTest(case_name="middle_page"):
            page.jumpSplit(5)

            block_forms_list[5] = self.getBlockForms(page)
            for index, forms in block_forms_list.items():
                if index == 5:
                    continue
                self.assertNotEquals(forms, block_forms_list[5])

            page.checkBtnShow()

        with self.subTest(case_name="middle2first_page"):
            page.jumpSplit(1)

            block_forms = self.getBlockForms(page)
            self.assertEquals(block_forms, block_forms_list[1])

            page.checkBtnShow()

        with self.subTest(case_name="middle2last_page"):
            page.jumpSplit(5)
            page.jumpSplit(page.getMaxIndex())

            block_forms_list[page.getMaxIndex()] = self.getBlockForms(page)
            self.assertNotEquals(block_forms_list[page.getMaxIndex()], block_forms_list[1])

            page.checkBtnShow()

    def test_search_page(self):
        page = HomePage(self.driver, self.domain)
        page = page.search("")
        self.generalTest(
            num_per_page=5,
            page=page,
        )

    @skip
    def test_detail_page(self):
        page = HomePage(self.driver, self.domain)
        page = page.search("rbq")
        page = page.goDetailPage(0)
        self.generalTest(
            num_per_page=5,
            page=page,
        )


class FrontFuncPersonInfoTC(FrontBasicTC):
    @tag(TAG_DB_MODIFY)
    def test_modify_form(self):
        page = HomePage(self.driver, self.domain)
        with LogStatus(page, "rbq", "rbq") as page:
            page = page.goPersonPage()

            old_form = page.getForm()
            test_form = {
                "role": "S",
                "gender": "M",
                "intro": "__test_modify_form__"
            }

            page.setForm(test_form)
            page.submit()
            self.assertDictEntry(page.getForm(), test_form)

            page.setForm(old_form)
            page.submit()
            self.assertDictEntry(page.getForm(), old_form)

    @tag(TAG_DB_MODIFY)
    def test_modify_photo(self):
        page = HomePage(self.driver, self.domain)
        with LogStatus(page, "rbq", "rbq") as page:
            page = page.goPersonPage()

            rs()
            old_url = page.getImageURL()
            test_path = "D:/code_concerned/ruangong/rateMyCourse_back/test/front/test_image.png" # TODO Move out

            page.uploadPage_wholeProcess(test_path)
            rs()
            new_url = page.getImageURL()

            self.assertIsNotNone(old_url)
            self.assertIsNotNone(new_url)
            self.assertNotEquals(old_url, new_url)
            # Maybe We can check photo's content. 
            # However the photo may be editted or compressed, 
            # so it seems impossible.

class FrontFuncRateCommentTC(FrontBasicTC):
    def goDetailPage(self, page:HomePage) -> DetailPage:
        page = page.search("rbq")
        page = page.goDetailPage(0)
        return page

    def checkRateState(self, page:DetailPage, index:int, is_up:bool, is_down:bool, rate_rank:int):
        self.assertEquals(page.isThumbUp(index), is_up)
        self.assertEquals(page.isThumbDown(index), is_down)
        self.assertEquals(page.getCommentRateRank(index), rate_rank)

    @tag(TAG_DB_MODIFY)
    def test_rate_comment(self):
        '''This testcase takes very long time, at least 20s'''
        page = HomePage(self.driver, self.domain)
        with LogStatus(page, "rbq", "rbq") as page:
            page = self.goDetailPage(page)
            tci = 0 # target comment index

            with self.subTest(case_name="init"):
                self.checkRateState(
                    page,
                    tci,
                    False,
                    False,
                    0
                )

            with self.subTest(case_name="agree_no2agree"):
                page.clickThumbUp(tci)
                rs()
                self.checkRateState(
                    page,
                    tci,
                    True,
                    False,
                    1
                )

            with self.subTest(case_name="agree_agree2no"):
                page.clickThumbUp(tci)
                rs()
                self.checkRateState(
                    page,
                    tci,
                    False,
                    False,
                    0
                )

            with self.subTest(case_name="disagree_no2disagree"):
                page.clickThumbDown(tci)
                rs()
                self.checkRateState(
                    page,
                    tci,
                    False,
                    True,
                    -1
                )

            with self.subTest(case_name="disagree_disagree2no"):
                page.clickThumbDown(tci)
                rs()
                self.checkRateState(
                    page,
                    tci,
                    False,
                    False,
                    0
                )

            with self.subTest(case_name="agree_again_no2agree"):
                page.clickThumbUp(tci)
                rs()
                self.checkRateState(
                    page,
                    tci,
                    True,
                    False,
                    1
                )

            with self.subTest(case_name="disagree_agree2disagree"):
                page.clickThumbDown(tci)
                rs()
                self.checkRateState(
                    page,
                    tci,
                    False,
                    True,
                    -1
                )

            with self.subTest(case_name="agree_disagree2agree"):
                page.clickThumbUp(tci)
                rs()
                self.checkRateState(
                    page,
                    tci,
                    True,
                    False,
                    1
                )

            with self.subTest(case_name="agree_reset_agree2no"):
                page.clickThumbUp(tci)
                rs()
                self.checkRateState(
                    page,
                    tci,
                    False,
                    False,
                    0
                )
