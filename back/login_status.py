from django.test import Client
from http.cookies import SimpleCookie
import hashlib

def getmd5(s):
    md5 = hashlib.md5()
    md5.update(s.encode("utf-8"))
    return md5.hexdigest()

class LoginStatus:
    def __init__(self, testcaseobj, username, password):
        self.testcaseobj = testcaseobj
        self.username = username
        self.password = password

    def __enter__(self):
        client = self.testcaseobj.client
        client.cookies = SimpleCookie(
            {
                "username": self.username,
                "password": getmd5(self.password)
            }
        )
        session = client.session
        session["auth_sess"] = self.username
        session.save()
        return self

    def __exit__(self, exc_type, exc_value, exc_tb):
        self.testcaseobj.client.session.flush()
        self.testcaseobj.client = Client()
        return False