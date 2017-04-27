#!/usr/bin/env python
# -*- coding: UTF-8 -*
import unittest
import sys
import os
sys.path.append(r'../../../test_suit/')
sys.path.append(r'../../../lib/')
from test_def import ApiTestSuit
try:
    from PyLogger import logging
except:
    import logging

# logger = logging.getLogger("GetFloorPlanTest")

class GetFloorPlanTest(ApiTestSuit):

    def setUp(self):
        ################################################################################
        self.script_dir = os.getcwd()
        self.script_file = __file__
        self.sub_class_name = GetFloorPlanTest.__name__
        self.testure_path = r"testure\ApiGetFloorPlanNormal.csv"
        self.config_path = r'''config.properties'''
        self.logger = logging.getLogger(self.__class__.__name__)
        self.initConfig()
        ################################################################################

    def beforeHttpTest(self, context):

        """
        :param context:
        :return:

        """
        self.logger.info("before HttpTest in this..............")

    def testGetFloorPlan(self):
        self.logger.info("********************************* Begin test **********************************")
        # self.logger.info(self.script_dir)
        self.startTest(runContext=self.runContext)
        # self.logger.info("tttttttttttttttttttttt")

    def afterHttpTest(self, context):
        self.logger.info("After HttpTest in this...............")

    def tearDown(self):
        self.logger.info("********************************* End test ************************************")


if __name__ == "__main__":
    unittest.main()