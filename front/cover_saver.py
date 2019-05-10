import os
from test.front.personal_config import coverage_dir

class CoverSaver:
    def __init__(self):
        self.count = 0
        if not os.path.exists(coverage_dir):
            os.mkdir(coverage_dir)

    def trySaveCoverageReport(self, driver, name=None):
        json_str = driver.execute_script("return jscoverage_serializeCoverageToJSON();")

        sub_dir = str(self.count)
        if name != None:
            sub_dir = name

        if not os.path.exists(coverage_dir + sub_dir):
            os.mkdir(coverage_dir + sub_dir)

        with open(coverage_dir + sub_dir + "/jscoverage.json", "w") as fd:
            fd.write(json_str)

        self.count += 1

cover_saver = CoverSaver()
