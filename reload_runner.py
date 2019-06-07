#!/usr/bin/env python
import os

import test_settings
from .rmc_test_logger import log
from django.conf import settings
from django.test.runner import DiscoverRunner
from django.core.management.commands import loaddata, flush

class ReloadTestRunner(DiscoverRunner):
    '''This TestRunner will flush and load database before testting.'''

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        db_name = settings.DATABASES["default"]["NAME"]
        if test_settings.DATABASES["default"]["NAME"] != db_name:
            raise Exception("Please test from test_manage.py, because of an independent test database needed for front testing.")

        # Flush test database
        log.info("Start flushing database [{0}]...".format(db_name))
        flush_cmd = flush.Command()
        flush_cmd.run_from_argv([
            "test/test_manage.py",
            "flush",
            "--noinput",
        ])
        log.info("Finished flushing!")

        # Load fixture
        log.info("Start installing fixture on database [{}] from [{}]...".format(db_name, test_settings.FRONT_FIXTURE))
        load_cmd = loaddata.Command()
        load_cmd.run_from_argv([
            "test/test_manage.py",
            "loaddata",
            test_settings.FRONT_FIXTURE,
        ])
        log.info("Finished installing.")