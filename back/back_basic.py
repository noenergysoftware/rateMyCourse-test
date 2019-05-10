import json
from unittest import skip, skipIf

import django.db
from django.contrib.sessions.models import Session
from django.test import Client, TestCase, tag

from .db_checker import DBChecker
from .test_logger import log
from .login_status import LoginStatus


class BackBasicTestCase(TestCase):
    # Prepare the database by using fixture.
    fixtures = ["back_fixture.json"]

    def logError(self, error_msg, case_name=None, response=None):
        if case_name and response:
            log.error("(%s) Test Fail. Response is [%s].\n\t%s", case_name, response.content, error_msg)
        elif case_name and not response:
            log.error("(%s) Test Fail. \n\t%s", case_name, error_msg)
        elif not case_name and response:
            log.error("Test Fail. Response is [%s].\n\t%s", response.content, error_msg)
        else:
            log.error("Test Fail. \n\t%s", error_msg)

    def checkDictEntry(self, dicta, dictb):
        for key, value in dictb.items():
            if not key in dicta.keys():
                return False
            if dicta[key] != dictb[key]:
                return False
        return True

    def response2JSON(self, response):
        return json.loads(response.content)

    def getJsonBody(self, url, form=None):
        response = self.client.get(url, form)
        try:
            self.assertEqual(response.status_code, 200)
            body = self.response2JSON(response)
            self.assertEqual(body["status"], 1)
            retlist = body["body"]
        except Exception as e:
            log.error("Error when checking response. The response is %s", response.content)
            raise e
        return (body, retlist, response)

    def getErrorTest(self, url, form=None):
        response = self.client.get(url, form)
        try:
            body = self.response2JSON(response)
            self.assertLess(body["status"], 0)
        except Exception as e:
            log.error("Error when checking response. The response is %s", response.content)
            raise e
        return response

    def assertDictEntry(self, dicta, dictb):
        for key, value in dictb.items():
            self.assertTrue(key in dicta.keys())
            self.assertEquals(dicta[key], dictb[key])

    def postContainTest(self, url, form, text=""):
        # Send Request
        #   Specify the interface to test by assigning the url.
        #   With the form attached.
        response = self.client.post(url, form)
                    
        # Response Check
        #   Check the status code(default 200) 
        #   and whether contain text in body.
        try:
            body = self.response2JSON(response)
            self.assertEqual(body["status"], 1)
            self.assertContains(response, text)
        except Exception as e:
            log.error("Error when checking response. The response is %s", response.content)
            raise e
        return response

    def postErrorTest(self, url, form):
        response = self.client.post(url, form)

        try:
            body = self.response2JSON(response)
            self.assertLess(body["status"], 0)
        except Exception as e:
            log.error("Error when checking response. The response is %s", response.content)
            raise e
        return response


class BackPostCheckDBTC(BackBasicTestCase):
    def setUp(self):
        self.checker = DBChecker(
            django.db.connection,
            self,
            "rateMyCourse"
        )
        super().setUp()

    def postAndCheck(self, url, model_name, prop_dict, text=""):
        # Send Request & Response Check
        response = self.postContainTest(url, prop_dict, text=text)
        # Side Effect Check
        #   Check whether the side effects take place.
        try:
            self.checker.check(model_name, prop_dict)
        except Exception as e:
            log.error("Error when checking body. Response is %s", response.content)
            raise e

    def autoTest(self, testcase_file):
        # Read Testcases from json
        testcases = None
        with open(testcase_file, "r", encoding="utf-8") as fd:
            testcases = json.load(fd)

        for case in testcases:
            # Load json data
            case_name = case[0]
            url = case[1]
            model_name = case[2]
            prop_dict = case[3]
            addition = {}
            if len(case) > 4:
                addition = case[4]

            # Do Test
            with self.subTest(case_name=case_name):
                try:
                    if addition and ("auth" in addition.keys()):
                        auth_info = addition["auth"]
                        with LoginStatus(self, auth_info["username"], auth_info["password"]):
                            self.postAndCheck(
                                url,
                                model_name,
                                prop_dict
                            )
                    else:
                        self.postAndCheck(
                            url,
                            model_name,
                            prop_dict
                        )
                except Exception as e:
                    self.logError(str(e), case_name)
                    raise e


class BackGetCheckBodyTC(BackBasicTestCase):
    def setUp(self):
        super().setUp()

    def getAndCheck(self, url, prop_dict, length, exp_list=[]):
        body, retlist, response = self.getJsonBody(url, prop_dict)
        try:
            self.assertDictEntry(
                body,
                {
                    "length": length
                }
            )
            for i in range(len(exp_list)):
                exist = False
                for j in range(len(retlist)):
                    if self.checkDictEntry(retlist[j], exp_list[i]):
                        exist = True
                        break
                self.assertTrue(exist)
        except Exception as e:
            log.error("Error when checking body. Response is %s", response.content)
            raise e


    def autoTest(self, testcase_file):
        # Read Testcases from json
        testcases = None
        with open(testcase_file, "r", encoding="utf-8") as fd:
            testcases = json.load(fd)

        for case in testcases:
            # Load json data
            case_name = case[0]
            url = case[1]
            prop_dict = case[2]
            length = case[3]
            exp_list = []
            if len(case) > 4:
                exp_list = case[4]

            # Do Test
            with self.subTest(case_name=case_name):
                try:
                    self.getAndCheck(
                        url,
                        prop_dict,
                        length,
                        exp_list
                    )
                except Exception as e:
                    self.logError(str(e), case_name)
                    raise e
