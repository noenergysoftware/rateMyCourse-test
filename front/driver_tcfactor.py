from front_config import PROXY_COVER

from selenium import webdriver
from selenium.webdriver.common.proxy import Proxy, ProxyType
from selenium.webdriver import DesiredCapabilities

@classmethod
def chrome(cls):
    if PROXY_COVER:
        cap = DesiredCapabilities.CHROME.copy()
        prox = Proxy()
        prox.proxy_type = ProxyType.MANUAL
        sock = "127.0.0.1:3128"
        prox.http_proxy = sock
        prox.add_to_capabilities(cap)
        cls.driver = webdriver.Remote(desired_capabilities=cap)
    else:
        cls.driver = webdriver.Chrome()

# @classmethod
# def edge(cls):
    # cls.driver = webdriver.Edge()