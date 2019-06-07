import os
from test.front.front_config import COVERAGE_DIR, MUST_FS_COVER

class CoverSaver:
    def __init__(self):
        self.count = 0
        if not os.path.exists(COVERAGE_DIR):
            os.mkdir(COVERAGE_DIR)

    def trySaveCoverageReport(self, driver, name=None):
        has_jscover = driver.execute_script("return (typeof jscoverage_serializeCoverageToJSON) != \"undefined\"")
        if not has_jscover:
            if MUST_FS_COVER:
                raise Exception("websites' code must be instrumented by JSCOVER since you have set MUST_FS_COVER true.")
            return

        json_str = driver.execute_script("return jscoverage_serializeCoverageToJSON();")

        sub_dir = str(self.count)
        if name != None:
            sub_dir = name

        if not os.path.exists(COVERAGE_DIR + sub_dir):
            os.mkdir(COVERAGE_DIR + sub_dir)

        with open(COVERAGE_DIR + sub_dir + "/jscoverage.json", "w") as fd:
            fd.write(json_str)

        self.count += 1

cover_saver = CoverSaver()
