from unittest import skip

from django.test import tag

from test.front.page_objects import *
from test.front.user_actions import *
from .front_basic import FrontBasicTC, TAG_DB_MODIFY

class FrontContentCheckTC(FrontBasicTC):
    def test_detail_course(self):
        page = HomePage(self.driver, self.domain)
        page = page.searchEnter("论持久战")
        page = page.goDetailPage(0)
        page.checkIsSelf()

        self.IDCheck(page, 
            {
                page.name_text_id: "论持久战",
                page.credit_text_id: "1",
                page.type_text_id: "必修",
                page.school_text_id: "Office",
                page.description_text_id: "猫真可爱"
            }
        )

    def test_detail_comment(self):
        page = HomePage(self.driver, self.domain)
        page = page.searchEnter("论持久战")
        page = page.goDetailPage(0)
        page.checkIsSelf()

        # TODO check comment content