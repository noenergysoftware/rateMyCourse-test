from unittest import TestCase

from selenium import webdriver
from selenium.webdriver.common.proxy import Proxy, ProxyType
from selenium.webdriver import DesiredCapabilities
from cover_saver import *

import random
from time import sleep, time

PROXY_COVER = False # Still not avaliable.

TAG_DB_MODIFY = "db_modify"
TAG_FRONT = "front"

def rs(min=1, max=5):
    '''randomly sleep for some time
    '''
    sleep_time = random.uniform(min, max)
    sleep(sleep_time)

class FrontBasicTC(TestCase):
    @classmethod
    def setUpClass(cls):
        super().setUpClass()
        if PROXY_COVER:
            cap = DesiredCapabilities.EDGE.copy()
            prox = Proxy()
            prox.proxy_type = ProxyType.MANUAL
            sock = "127.0.0.1:3128"
            prox.http_proxy = sock
            prox.add_to_capabilities(cap)
            cls.driver = webdriver.Remote(desired_capabilities=cap)
        else:
            cls.driver = webdriver.Chrome()
            cls.driver.implicitly_wait(20)

    @classmethod
    def tearDownClass(cls):
        if FS_COVER:
            cover_saver.trySaveCoverageReport(cls.driver)
        cls.driver.close()
        super().tearDownClass()

    def setUp(self):
        self.domain = "ratemycourse.tk"

    def IDCheck(self, page, id_text_dict):
        for text_id, exp_text in id_text_dict.items():
            element = page.waitAppear_ID(text_id)
            text = element.text
            self.assertEqual(text, exp_text)