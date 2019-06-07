import json
from unittest import skip, skipIf

import django.db
from django.contrib.sessions.models import Session
from django.test import Client, TestCase, tag

from .db_checker import DBChecker
from .login_status import LoginStatus


class BackBasicTestCase(TestCase):
    # Prepare the database by using fixture.
    fixtures = ["back_fixture.json"]

    def checkDictEntry(self, dicta, dictb):
        for key, value in dictb.items():
            if not key in dicta.keys():
                return False
            if dicta[key] != dictb[key]:
                return False
        return True

    def response2JSON(self, response):
        return json.loads(response.content)

    def assertDictEntry(self, dicta, dictb):
        for key, value in dictb.items():
            self.assertTrue(key in dicta.keys())
            self.assertEquals(dicta[key], dictb[key])


class BackPostCheckDBTC(BackBasicTestCase):
    def setUp(self):
        self.checker = DBChecker(
            django.db.connection,
            self,
            "rateMyCourse"
        )
        super().setUp()

    def postContainTest(self, url, form, text=""):
        # Send Request
        #   Specify the interface to test by assigning the url.
        #   With the form attached.
        response = self.client.post(url, form)
                    
        # Response Check
        #   Check the status code(default 200) 
        #   and whether contain text in body.
        body = self.response2JSON(response)
        self.assertEqual(body["status"], 1)
        self.assertContains(response, text)
        return response

    def postErrorTest(self, url, form):
        response = self.client.post(url, form)

        body = self.response2JSON(response)
        self.assertLess(body["status"], 0)
        return response

    def postAndCheck(self, url, model_name, prop_dict, text=""):
        # Send Request & Response Check
        response = self.postContainTest(url, prop_dict, text=text)
        # Side Effect Check
        #   Check whether the side effects take place.
        self.checker.check(model_name, prop_dict)

class BackGetCheckBodyTC(BackBasicTestCase):
    def setUp(self):
        super().setUp()

    def getJsonBody(self, url, form=None):
        response = self.client.get(url, form)

        self.assertEqual(response.status_code, 200)
        body = self.response2JSON(response)
        self.assertEqual(body["status"], 1)
        retlist = body["body"]

        return (body, retlist, response)

    def getErrorTest(self, url, form=None):
        response = self.client.get(url, form)

        body = self.response2JSON(response)
        self.assertLess(body["status"], 0)

        return response

    def getAndCheck(self, url, prop_dict, exp_list=[]):
        body, retlist, response = self.getJsonBody(url, prop_dict)

        for i in range(len(exp_list)):
            exist = False
            for j in range(len(retlist)):
                if self.checkDictEntry(retlist[j], exp_list[i]):
                    exist = True
                    break
            self.assertTrue(exist)

