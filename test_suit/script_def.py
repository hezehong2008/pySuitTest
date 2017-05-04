#!/usr/bin/env python
# -*- coding: UTF-8 -*

###############################################################################
# Copyright (C), 2017 heZehong
#
# Filename:     test_def.py
# Version:      1.0.0
# Description:  Module for pySuit frame to manage the test procedure
# Author:       he zehong
# History:
#   1. 2017-04-25  he zehong, first create
###############################################################################

"""
    testModel---

        testCase ---

    testRuner---

    testResult---

    testLogger---

    testReporter --- html, log, file , db
"""
import os
import sys


class TestScript(object):

    def runTest(self):
        pass
    pass


class TestModel(object):
    def __init__(self, fileName):
        try:
            model = exec ("import %s" % fileName)
            a = 2
        except Exception:
            pass

    pass


class TestCase(object):
    pass

