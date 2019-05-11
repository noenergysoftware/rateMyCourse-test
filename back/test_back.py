import os
from http.cookies import SimpleCookie

from django.test import Client, tag

from .back_basic import BackBasicTestCase, BackGetCheckBodyTC, BackPostCheckDBTC
from .login_status import LoginStatus, getmd5
from rateMyCourse.models import (Comment, Course, MakeComment, TeachCourse,
                                 Teacher, User, Rank, MakeRank, RankCache, 
                                 RateComment, )

BACK_TEST_DIR = os.path.dirname(os.path.abspath(__file__))

# Test Cases
@tag("back")
class BackCreateTC(BackPostCheckDBTC):
    @tag("auto")
    def test_auto(self):
        self.autoTest(os.path.join(BACK_TEST_DIR, "test_create.pd.json"))

    def test_sign_up(self):
        self.postContainTest(
        "/signUp/",
            {
            "username": "test",
            "password": "123",
            "mail": "test@test.com",
            "Ticket": "0",
            "Randstr": "0",
            "IP": "127.0.0.1"
            }
        )
        self.assertTrue(
            User.objects.filter(
                username="test",
                password="123",
                mail="test@test.com"
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
                "username": "test",
                "Ticket": "0",
                "RandStr": "0",
                "IP": "127.0.0.1"
            }
        )

    def test_sign_up_dup_mail(self):
        self.postErrorTest(
            "/signUp/",
            {
                "username": "test_dup_mail",
                "mail": "ming@test.com",
                "password": "kkk",
                "Ticket": "0",
                "RandStr": "0",
                "IP": "127.0.0.1"
            }
        )

    def test_sign_up_dup_username(self):
        self.postErrorTest(
            "/signUp/",
            {
                "username": "ming",
                "mail": "test_dup_username@test.com",
                "password": "kkk",
                "Ticket": "0",
                "RandStr": "0",
                "IP": "127.0.0.1"
            }
        )

    @tag("foreign")
    def test_make_rank(self):
        with LoginStatus(self, "hong", "hong"):
            self.postContainTest(
                "/makeRank/",
                {
                    "username": "hong",
                    "course_ID": "000000",
                    "difficulty_score": 2,
                    "funny_score": 2,
                    "gain_score": 2,
                    "recommend_score": 2
                }
            )
        self.assertTrue(
            Rank.objects.filter(
                difficulty_score=2,
                funny_score=2,
                gain_score=2,
                recommend_score=2,
            ).exists()
        )
        self.assertTrue(
            MakeRank.objects.filter(
                user__username="hong",
                course__course_ID="000000",
                rank__difficulty_score=2,
                rank__funny_score=2,
                rank__gain_score=2,
                rank__recommend_score=2,
            ).exists()
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

    def test_rate_comment(self):
        comment_ID = Comment.objects.get(content="rbq").id

        def checkRate(username, password, rtype, comment_rate, rate_rate):
            with LoginStatus(self, username, password):
                self.postContainTest(
                    "/rateComment/",
                    {
                        "username": username,
                        "comment_ID": comment_ID,
                        "type": rtype,
                    }
                )
            self.assertTrue(
                RateComment.objects.filter(
                    user__username=username,
                    comment__id=comment_ID,
                    comment__rate=comment_rate,
                    rate=rate_rate,
                )
            )

        with self.subTest(case_name="create"):
            checkRate(
                "rbq",
                "rbq",
                "agree",
                1,
                1
            )
        
        with self.subTest(case_name="another_agree"):
            checkRate(
                "ming",
                "ming",
                "agree",
                2,
                1
            )

        with self.subTest(case_name="reverse_agree2disagree"):
            checkRate(
                "rbq",
                "rbq",
                "disagree",
                0,
                -1
            )

        with self.subTest(case_name="cancel_disagree"):
            checkRate(
                "rbq",
                "rbq",
                "disagree",
                1,
                0
            )

        with self.subTest(case_name="agree_again"):
            checkRate(
                "rbq",
                "rbq",
                "agree",
                2,
                1
            )

        with self.subTest(case_name="cancel_agree"):
            checkRate(
                "rbq",
                "rbq",
                "agree",
                1,
                0
            )

        with self.subTest(case_name="disagree_again"):
            checkRate(
                "rbq",
                "rbq",
                "disagree",
                0,
                -1
            )
        
        with self.subTest(case_name="reverse_disagree2agree"):
            checkRate(
                "rbq",
                "rbq",
                "agree",
                2,
                1
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

    @tag("foreign")
    def test_make_rank(self):
        with LoginStatus(self, "rbq", "rbq"):
            self.postContainTest(
                "/makeRank/",
                {
                    "username": "rbq",
                    "course_ID": "000000",
                    "difficulty_score": 4,
                    "funny_score": 3,
                    "gain_score": 2,
                    "recommend_score": 1
                }
            )
        self.assertTrue(
            Rank.objects.filter(
                difficulty_score=4,
                funny_score=3,
                gain_score=2,
                recommend_score=1,
            ).exists()
        )
        self.assertTrue(
            MakeRank.objects.filter(
                user__username="rbq",
                course__course_ID="000000",
                rank__difficulty_score=4,
                rank__funny_score=3,
                rank__gain_score=2,
                rank__recommend_score=1,
            ).exists()
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

    def test_get_rank_by_course_zero(self):
        body, retdict, response = self.getJsonBody(
            "/getRankByCourse/",
            {
                "course_ID": "0"
            }
        )
        self.checkDictEntry(
            retdict,
            {
                "difficulty_score": 0,
                "funny_score": 0,
                "gain_score": 0,
                "recommend_score": 0,
            }
        )

    def test_get_rank_by_course_single(self):
        body, retdict, response = self.getJsonBody(
            "/getRankByCourse/",
            {
                "course_ID": "110"
            }
        )
        self.checkDictEntry(
            retdict,
            {
                "difficulty_score": 5,
                "funny_score": 5,
                "gain_score": 5,
                "recommend_score": 5,
            }
        )

    def test_get_rank_by_course_multi(self):
        body, retdict, response = self.getJsonBody(
            "/getRankByCourse/",
            {
                "course_ID": "1"
            }
        )
        self.checkDictEntry(
            retdict,
            {
                "difficulty_score": 2,
                "funny_score": 3,
                "gain_score": 4,
                "recommend_score": 5,
            }
        )

    def checkRankDictComplete(self, rank_dict):
        key_list = [
            "difficulty_score",
            "funny_score",
            "gain_score",
            "recommend_score",
            "rank_number",
        ]
        for key in key_list:
            self.assertTrue(key in rank_dict.keys())

    def test_get_all_rank(self):
        body, retdict, response = self.getJsonBody(
            "/getAllRank/",
        )
        # Note here we do not check whether rank is correctly calculated,
        #   that part is checked in BackCalRankTC.
        self.assertEquals(len(retdict), 4)
        id_list = [
            "000000",
            "110",
            "1",
            "0",
        ]
        for id in id_list:
            self.assertTrue(id in retdict.keys())
            rank_dict = retdict[id]
            self.checkRankDictComplete(rank_dict)
        
    def test_get_rank_by_sorted_course(self):
        body, retdict, response = self.getJsonBody(
            "/getRankBySortedCourse/",
        )
        # TODO 
        
    def test_get_rank_by_sorted_teacher(self):
        body, retdict, response = self.getJsonBody(
            "/getRankBySortedTeacher/",
        )
        # TODO 

    def test_get_rate_comment(self):
        comment_ID = Comment.objects.get(content="我成功进去啦！").id
        body, retdict, response = self.getJsonBody(
            "/getRateComment/",
            {
                "comment_ID": comment_ID,
            }
        )
        self.assertEquals(retdict["rate"], 0)


@tag("back")
class BackHotCommentTC(BackGetCheckBodyTC):
    def test_get_hot_comment(self):
        course_ID = "110"

        with self.subTest(case_name="<3"):
            body, retlist, response = self.getJsonBody(
                "/getHotComment/",
                {
                    "course_ID": course_ID,
                }
            )
            self.assertTrue(len(retlist), 1)
            self.checkDictEntry(
                retlist[0],
                {
                    "username": "police",
                    "content": "那你很棒棒哦",
                    "commentID": 2,
                    "teacher": "police",
                    "parent_comment": 1,
                    "rate": 1
                }
            )

        course_ID = "000000"
        for i in range(5):
            comment = Comment.objects.create(
                content=str(i),
                rate=6,
                teacher=Teacher.objects.get(name="rbq")
            )
            MakeComment.objects.create(
                user=User.objects.get(username="rbq"),
                course=Course.objects.get(course_ID=course_ID),
                comment=comment
            )

        with self.subTest(case_name=">3"):
            body, retlist, response = self.getJsonBody(
                "/getHotComment/",
                {
                    "course_ID": course_ID,
                }
            )
            self.assertTrue(len(retlist), 3)
            for item in retlist:
                self.checkDictEntry(
                    item,
                    {
                        "username": "rbq",
                        "teacher": "rbq",
                        "parent_comment": -1,
                        "rate": 6
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


@tag("back")
class BackCalRankTC(BackBasicTestCase):
    def test_simple_flush_rank(self):
        course_ID = "165486"
        course = Course.objects.create(
            name="flush_course",
            course_ID=course_ID,
            credit=2,
        )
        self.client.get(
            "/flushRank/"
        )
        self.assertTrue(
            RankCache.objects.filter(
                course__course_ID=course_ID,
            ).exists()
        )

    # TODO more specific test
