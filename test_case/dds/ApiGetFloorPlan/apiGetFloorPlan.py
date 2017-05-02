#!/usr/bin/env python
# -*- coding: UTF-8 -*
import unittest
import sys
import os
sys.path.append(r'../../../')
from test_suit.test_def import ApiTestSuit
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
        self.testure_path = r"testure/ApiPostFloorPlanNormarlTest.csv"
        self.config_path = r'''../config.properties'''
        self.logger = logging.getLogger(self.__class__.__name__)
        self.initConfig()
        ################################################################################

    def beforeHttpTest(self, context):

        """
        :param context:
        :return:

        """
        self.logger.info("before HttpTest in this..............")
        # context.getHttpSendUrl
        self.logger.debug(context.getHttpSendUrl())

    def testGetFloorPlan(self):
        self.logger.info("********************************* Begin test ***********************************")
        self.startTest(runContext=self.runContext)

    def afterHttpTest(self, context):
        self.logger.info("After HttpTest in this...............")

    def tearDown(self):
        self.logger.info("********************************* End test *************************************")


if __name__ == "__main__":
    # unittest.main()
    suite = unittest.TestLoader().loadTestsFromTestCase(GetFloorPlanTest)
    test_result = unittest.TextTestRunner(verbosity=2).run(suite)
    a = 3