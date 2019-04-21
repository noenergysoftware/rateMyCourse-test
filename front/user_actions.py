from page_objects import *
from contextlib import contextmanager

@contextmanager
def LogStatus(page, name, password):
    try:
        driver = page.driver
        if not isinstance(page, LoginPage):
            page = page.goLoginPage()
        yield page.logIn(name, password)
    finally:
        driver.delete_all_cookies()