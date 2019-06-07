# This file is not being used.
# Because I have not found a good way to record log info.
# However, the logger in this module can work well.
# Sample Code:
#   from .test_logger import log
#   log.error("(%s) Test Fail. Response is [%s].\n\t%s", case_name, response.content, error_msg)

import logging
import sys
import os

log = logging.getLogger("rateMyCourse_test")
log.setLevel(logging.DEBUG)

formatter = logging.Formatter("[%(levelname)s] %(message)s")

file_handler = logging.FileHandler("test/test.log", "wt")
file_handler.setLevel(logging.DEBUG)
file_handler.setFormatter(formatter)
log.addHandler(file_handler)

stream_handler = logging.StreamHandler(sys.stdout)
stream_handler.setLevel(logging.INFO)
stream_handler.setFormatter(formatter)
log.addHandler(stream_handler)
