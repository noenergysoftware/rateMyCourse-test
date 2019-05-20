#!/usr/bin/env python
import os
import sys
import urllib.request
import ssl

# Note:
#   You should call this file from django's root directory, just like the manage.py
#       python test/test_manage.py ...
#   In this way, the top directory can be automatically added into sys.path

if __name__ == "__main__":
    # Set proxy which leads to Fiddler
    # and Fiddler will forward urllib's requests.
    proxy = urllib.request.ProxyHandler({"https": "https://127.0.0.1:8888"})
    opener = urllib.request.build_opener(proxy)
    urllib.request.install_opener(opener)

    # Remove SSL verify, since we are just testing.
    ssl._create_default_https_context = ssl._create_unverified_context

    # Set secret keys for test env
    os.environ.setdefault("DJANGOAID", "233")
    os.environ.setdefault("DJANGOASK", "hhh")
    os.environ.setdefault("DJANGOSK", "Good_Boy")

    # django
    os.environ.setdefault("DJANGO_SETTINGS_MODULE", "test.test_settings")
    try:
        from django.core.management import execute_from_command_line
    except ImportError:
        # The above import may fail for some other reason. Ensure that the
        # issue is really that Django is missing to avoid masking other
        # exceptions on Python 2.
        try:
            import django
        except ImportError:
            raise ImportError(
                "Couldn't import Django. Are you sure it's installed and "
                "available on your PYTHONPATH environment variable? Did you "
                "forget to activate a virtual environment?"
            )
        raise
    execute_from_command_line(sys.argv)
