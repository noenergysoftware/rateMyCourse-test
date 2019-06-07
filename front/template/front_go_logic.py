from unittest import skip
from contextlib import contextmanager

from django.test import tag

from test.front.page_objects import *
from test.front.user_actions import *
from .front_basic import FrontBasicTC, TAG_DB_MODIFY

class FrontHomeGoLogicTC(FrontBasicTC):
    def createInitPage(self):
        return HomePage(self.driver, self.domain)

    def test_login(self):
        page = self.createInitPage()
        loginpage = page.goLoginPage()
        loginpage.checkIsSelf()

    def test_regist(self):
        page = self.createInitPage()
        registpage = page.goRegistPage()
        registpage.checkIsSelf()

    def test_search_enter(self):
        page = self.createInitPage()
        searchpage = page.searchEnter("rbq")
        searchpage.checkIsSelf()

    def test_search_button(self):
        page = self.createInitPage()
        searchpage = page.searchButton("rbq")
        searchpage.checkIsSelf()

    def test_person(self):
        page = self.createInitPage()
        with LogStatus(page, "rbq", "rbq") as page:
            page = page.goPersonPage()
            page.checkIsSelf()


class FrontSearchGoLogicTC(FrontBasicTC):
    def createInitPage(self):
        homepage = HomePage(self.driver, self.domain)
        searchpage = homepage.searchEnter("rbq")
        searchpage.checkIsSelf()
        return searchpage

    def test_home(self):
        searchpage = self.createInitPage()
        homepage = searchpage.goHomePage()
        homepage.checkIsSelf()

    def test_login(self):
        searchpage = self.createInitPage()
        loginpage = searchpage.goLoginPage()
        loginpage.checkIsSelf()

    def test_regist(self):
        searchpage = self.createInitPage()
        registpage = searchpage.goRegistPage()
        registpage.checkIsSelf()

    def test_detail(self):
        searchpage = self.createInitPage()
        detailpage = searchpage.goDetailPage(0)
        detailpage.checkIsSelf()

    def test_person(self):
        page = self.createInitPage()
        with LogStatus(page, "rbq", "rbq") as page:
            page = page.goPersonPage()
            page.checkIsSelf()


class FrontDetailGoLogicTC(FrontBasicTC):
    def createInitPage(self):
        homepage = HomePage(self.driver, self.domain)
        searchpage = homepage.searchEnter("rbq")
        detailpage = searchpage.goDetailPage("0")
        detailpage.checkIsSelf()
        return detailpage

    def test_home(self):
        page = self.createInitPage()
        homepage = page.goHomePage()
        homepage.checkIsSelf()

    def test_login(self):
        page = self.createInitPage()
        loginpage = page.goLoginPage()
        loginpage.checkIsSelf()

    def test_regist(self):
        page = self.createInitPage()
        registpage = page.goRegistPage()
        registpage.checkIsSelf()

    def test_search(self):
        # TODO need more spec
        pass

    def test_person(self):
        page = self.createInitPage()
        with LogStatus(page, "rbq", "rbq") as page:
            page = page.goPersonPage()
            page.checkIsSelf()

    def test_comment(self):
        page = self.createInitPage()
        commentpage = page.goCommentPage()
        commentpage.checkIsSelf()


class FrontCommentGoLogicTC(FrontBasicTC):
    def goInitPage(self, homepage):
        searchpage = homepage.search("rbq")
        detailpage = searchpage.goDetailPage("0")
        commonpage = detailpage.goCommentPage()
        return commonpage

    def createInitPage(self):
        homepage = HomePage(self.driver, self.domain)
        return self.goInitPage(homepage)

    def test_home(self):
        page = self.createInitPage()
        homepage = page.goHomePage()
        homepage.checkIsSelf()

    def test_login(self):
        page = self.createInitPage()
        loginpage = page.goLoginPage()
        loginpage.checkIsSelf()

    def test_regist(self):
        page = self.createInitPage()
        registpage = page.goRegistPage()
        registpage.checkIsSelf()

    def test_person(self):
        page = self.createInitPage()
        with LogStatus(page, "rbq", "rbq") as page:
            page = page.goPersonPage()
            page.checkIsSelf()

    @tag(TAG_DB_MODIFY)
    def test_detail(self):
        page = HomePage(self.driver, self.domain)
        with LogStatus(page, "rbq", "rbq") as page:
            page = self.goInitPage(page)
            page.selectTeacher(0)
            page.editComment("kkkkkkkkkk")
            page = page.submitComment()
            page.checkIsSelf()


class FrontRegistGoLogicTC(FrontBasicTC):
    def createInitPage(self):
        homepage = HomePage(self.driver, self.domain)
        return homepage.goRegistPage()

    def test_home(self):
        page = self.createInitPage()
        page = page.goHomePage()
        page.checkIsSelf()

    def test_login_normal(self):
        page = self.createInitPage()
        page = page.goLoginPage()
        page.checkIsSelf()

    @tag(TAG_DB_MODIFY)
    def test_login_submit(self):
        page = self.createInitPage()
        page.fillForm(
            name="test_regist_login",
            email="test_regist_login@test.com",
            password="test_regist_login_233",
            repassword="test_regist_login_233",
        )
        page = page.submit()
        page.checkIsSelf()


class FrontLoginGoLogicTC(FrontBasicTC):
    def createInitPage(self):
        homepage = HomePage(self.driver, self.domain)
        return homepage.goLoginPage()

    def test_home_normal(self):
        page = self.createInitPage()
        page = page.goHomePage()
        page.checkIsSelf()

    def test_home_submit(self):
        page = self.createInitPage()
        with LogStatus(page, "rbq", "rbq") as page:
            page.checkIsSelf()

    def test_regist(self):
        page = self.createInitPage()
        page = page.goRegistPage()
        page.checkIsSelf()


class FrontPersonGoLogicTC(FrontBasicTC):
    @contextmanager
    def LogAndOpenPerson(self, name, password):
        try:
            page = HomePage(self.driver, self.domain)
            with LogStatus(page, name, password) as page:
                yield page.goPersonPage()
        finally:
            pass

    def test_home(self):
        with self.LogAndOpenPerson("ming", "ming") as page:
            page = page.goHomePage()
            page.checkIsSelf()

    def test_self_normal(self):
        with self.LogAndOpenPerson("ming", "ming") as page:
            page = page.goPersonPage()
            page.checkIsSelf()

    def test_self_submit(self):
        with self.LogAndOpenPerson("ming", "ming") as page:
            page.submit()
            page.checkIsSelf()
    