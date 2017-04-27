#!/usr/bin/env python
# -*- coding: UTF-8 -*
import unittest
import sys
import os
sys.path.append('../../../test_suit/')
sys.path.append('../../../lib/')
from test_def import ApiTestScript
from test_def import runContext;
try:
    from PyLogger import logging
except:
    import logging

class GetFloorPlanTest(ApiTestScript):

    def setUp(self):
        ################################################################################
        self.script_path = os.getcwd()
        self.sub_class_name = GetFloorPlanTest.__name__
        self.logger = logging.getLogger(self.__class__.__name__)
        self.initConfig()
        ################################################################################

    def testGetFloorPlan(self):
        print("*********************************")
        print(self.script_path)
        self.startTest(runContext=self.runContext)
        self.logger.info("tttttttttttttttttttttt")

    def tearDown(self):
        print("clean test..........")


if __name__ == "__main__":
    unittest.main()
