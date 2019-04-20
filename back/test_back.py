import os
from http.cookies import SimpleCookie

from django.test import Client, tag

from back_basic import BackBasicTestCase, BackGetCheckBodyTC, BackPostCheckDBTC
from login_status import LoginStatus, getmd5
from rateMyCourse.models import (Comment, Course, MakeComment, TeachCourse,
                                 Teacher, User)

BACK_TEST_DIR = os.path.dirname(os.path.abspath(__file__))

# Test Cases
@tag("back")
class BackCreateTC(BackPostCheckDBTC):
    @tag("auto")
    def test_auto(self):
        self.autoTest(os.path.join(BACK_TEST_DIR, "test_create.pd.json"))

    @tag("foreign")
    def test_add_teach_course(self):
        with LoginStatus(self, "rbq", "rbq"):
            self.postContainTest(
                "/addTeachCourse/",
                {
                    "teacher_list": ["rbq"],
                    "course": "rbq",
                    "department": "rbq"
                }
            )
        self.assertTrue(
            TeachCourse.objects.filter(
                teachers__name="rbq",
                course__name="rbq",
                department__name="rbq"
            ).exists()
        )

    @tag("foreign")
    def test_make_comment(self):
        with LoginStatus(self, "hong", "hong"):
            self.postContainTest(
                "/makeComment/",
                {
                    "username": "hong",
                    "course_ID": "0",
                    "content": "hong test comment",
                    "teacher_name": "qiang"
                }
            )
        self.assertTrue(
            Comment.objects.filter(
                content="hong test comment",
            ).exists()
        )
        self.assertTrue(
            MakeComment.objects.filter(
                user__username="hong",
                course__course_ID="0",
                comment__content="hong test comment"
            ).exists()
        )

    def test_sign_up_not_complete(self):
        self.postErrorTest(
            "/signUp/",
            {
                "username": "test"
            }
        )

    def test_sign_up_dup_mail(self):
        self.postErrorTest(
            "/signUp/",
            {
                "username": "test_dup_mail",
                "mail": "ming@test.com",
                "password": "kkk"
            }
        )

    def test_sign_up_dup_username(self):
        self.postErrorTest(
            "/signUp/",
            {
                "username": "ming",
                "mail": "test_dup_username@test.com",
                "password": "kkk"
            }
        )


@tag("back")
class BackUpdateTC(BackPostCheckDBTC):
    @tag("auto")
    def test_auto(self):
        self.autoTest(os.path.join(BACK_TEST_DIR, "test_update.pd.json"))

    @tag("foreign")
    def test_edit_comment(self):
        comment_ID = Comment.objects.get(content="rbq").id
        with LoginStatus(self, "rbq", "rbq"):
            self.postContainTest(
                "/editComment/",
                {
                    "comment_ID": comment_ID,
                    "content": "changed",
                    "teacher_name": "qiang"
                }
            )
            self.assertTrue(
                MakeComment.objects.filter(
                    comment__content="changed",
                ).exists()
            )

    def test_update_user_not_complete(self):
        with LoginStatus(self, "rbq", "rbq"):
            self.postErrorTest(
                "/updateUser/",
                {
                    "username": "rbq",
                    "gender": "M"
                }
            )


@tag("back")
class BackSearchTC(BackGetCheckBodyTC):
    @tag("auto")
    def test_auto(self):
        self.autoTest(os.path.join(BACK_TEST_DIR, "test_search.gb.json"))

    def test_get_user_detail(self):
        body, retdict, response = self.getJsonBody(
            "/getUserDetail/",
            {
                "username": "ming"
            }
        )
        self.checkDictEntry(
            retdict,
            {
                "username": "ming",
                "mail": "ming@test.com",
                "role": "S",
                "gender": "M",
                "self_introduction": "mingming"
            }
        )
        


@tag("back")
class BackAuthTC(BackBasicTestCase):
    def test_sign_in_with_username(self):
        try:
            self.postContainTest(
                "/signIn/",
                {
                    "username": "rbq",
                    "password": getmd5("rbq")
                }
            )
            sess_content = self.client.session.get("auth_sess")
            self.assertEqual(sess_content, "rbq")
        finally:
            self.client.session.flush()
            self.client = Client()

    def test_sign_in_with_mail(self):
        try:
            self.postContainTest(
                "/signIn/",
                {
                    "mail": "rbq@test.com",
                    "password": getmd5("rbq")
                }
            )
            sess_content = self.client.session.get("auth_sess")
            self.assertEqual(sess_content, "rbq")
        finally:
            self.client.session.flush()
            self.client = Client()

    def test_sign_in_no_mail_username(self):
        try:
            self.postErrorTest(
                "/signIn/",
                {
                    "password": getmd5("rbq")
                }
            )
        finally:
            self.client.session.flush()
            self.client = Client()

    def test_sign_in_username_not_exist(self):
        try:
            self.postErrorTest(
                "/signIn/",
                {
                    "username": "test_username_not_exist",
                    "password": getmd5("rbq")
                }
            )
        finally:
            self.client.session.flush()
            self.client = Client()

    def test_sign_in_mail_not_exist(self):
        try:
            self.postErrorTest(
                "/signIn/",
                {
                    "mail": "test_mail_not_exist@test.com",
                    "password": getmd5("rbq")
                }
            )
        finally:
            self.client.session.flush()
            self.client = Client()

    def test_sign_in_wrong_password(self):
        try:
            self.postErrorTest(
                "/signIn/",
                {
                    "username": "ming",
                    "password": getmd5("ming_wrong")
                }
            )
        finally:
            self.client.session.flush()
            self.client = Client()

    def test_log_out(self):
        try:
            self.client.cookies = SimpleCookie(
                {
                    "username": "rbq",
                    "password": getmd5("rbq")
                }
            )
            session = self.client.session
            session["auth_sess"] = "rbq"
            session.save()

            self.postContainTest(
                "/logout/",
                {
                    "username": "rbq"
                }
            )
            sess_content = self.client.session.get("auth_sess")
            self.assertIsNone(sess_content)
        finally:
            self.client.session.flush()
            self.client = Client()
