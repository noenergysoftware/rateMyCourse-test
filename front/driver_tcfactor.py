from test.front.front_config import PROXY_COVER

from selenium import webdriver
from selenium.webdriver.common.proxy import Proxy, ProxyType
from selenium.webdriver import DesiredCapabilities

# Note: We now not using proxy jscover and remote selenium,
#   while we may use one of them some day,
#   so I comment these codes for future.
#   You can just ignore these now.
# @classmethod
# def chrome(cls):
    # if PROXY_COVER:
        # cap = DesiredCapabilities.CHROME.copy()
        # prox = Proxy()
        # prox.proxy_type = ProxyType.MANUAL
        # sock = "127.0.0.1:3128"
        # prox.http_proxy = sock
        # prox.add_to_capabilities(cap)
        # cls.driver = webdriver.Remote(desired_capabilities=cap)
    # else:
        # cls.driver = webdriver.Chrome()

@classmethod
def chrome(cls):
    cls.driver = webdriver.Chrome()

# @classmethod
# def edge(cls):
    # cls.driver = webdriver.Edge()

# @classmethod
# def firefox(cls):
    # cls.driver = webdriver.Firefox()

# Note: All of mobile tests are based on Chorme's [Mobile Emulation](https://sites.google.com/a/chromium.org/chromedriver/mobile-emulation), 
#   which has its own shortcomings.
# @classmethod
# def mobile_iphone(cls):
    # mobileEmulation = {
        # "deviceName": "iPhone 6/7/8"
    # }
    # options = webdriver.ChromeOptions()
    # options.add_experimental_option("mobileEmulation", mobileEmulation)
    # cls.driver = webdriver.Chrome(chrome_options=options)