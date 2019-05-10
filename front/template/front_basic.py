from unittest import TestCase

from selenium import webdriver
from selenium.webdriver.common.proxy import Proxy, ProxyType
from selenium.webdriver import DesiredCapabilities

from test.front.cover_saver import cover_saver
from test.front.front_config import FS_COVER, PROXY_COVER

TAG_DB_MODIFY = "db_modify"
TAG_FRONT = "front"
TAG_SPLIT = "split"

class FrontBasicTC(TestCase):
    @classmethod
    def setUpClass(cls):
        super().setUpClass()
        cls.initDriver()
        cls.driver.implicitly_wait(20)

    @classmethod
    def tearDownClass(cls):
        if FS_COVER:
            cover_saver.trySaveCoverageReport(cls.driver, name=cls.__name__)
        cls.driver.close()
        super().tearDownClass()

    def setUp(self):
        self.domain = "ratemycourse.tk"

    def IDCheck(self, page, id_text_dict):
        for text_id, exp_text in id_text_dict.items():
            element = page.waitAppear_ID(text_id)
            text = element.text
            self.assertEqual(text, exp_text)