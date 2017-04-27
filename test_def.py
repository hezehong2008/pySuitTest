#!/usr/bin/env python
# -*- coding: UTF-8 -*

################################################################################
# Copyright (C), 2010, TP-LINK Technologies Co., Ltd.
#
# filename:     test_def.py
# version:      0.0.1
# description:  Test case and test suite management
# first create: hezehong
# history:
#       2017-04-12 | First created.
#                  | Using datebase to management the test case info
################################################################################

"""Module for test case and test suite management"""

import time
import sys
import traceback
import os
import types
import logging
import os
import types

try:
    from TestFrame.python_test_frame.interface.PyLogger import logger
except:
    import logging

# def loadTestsFromModule(self, module):
#     """Return a suite of all tests cases contained in the given module"""
#     tests = []
#     for name in dir(module):
#         obj = getattr(module, name)
#         if (isinstance(obj, (type, types.ClassType)) and
#             issubclass(obj, TestCase)):
#             tests.append(self.loadTestsFromTestCase(obj))
#     return self.suiteClass(tests)

class TestScript(object):
    # ScriptType = "HTTP"

    def __init__(self):
        # import sys;
        # if not "/home/a/" in sys.path:
        #     sys.path.append("/home/a/")
        # if not 'b' in sys.modules:
        #     b = __import__('b')
        # else:
        #     eval('import b')
        #     b = eval('reload(b)')
        self._import_class_name = None
        self._test_name = 'add_test'
        self._class_name = 'test'
        path = "D:\Users\Administrator\PycharmProjects\untitled\TestFrame\python_test_frame\interface\d_script"
        sys.path.append(path)
        self.script_path = path
        self.script_obj = None
        self.logger = logging.getLogger(self.__class__.__name__)

    def _import_script(self, mod_str, class_filter_name='test'):

        """

        :param mod_str:  the module name of the script
        :param class_filter_name:  the class filter name
        :return: return the script classes instance list
        a srcipt such as
        class testClass1():
            pass

        class testClass2():
            pass
        """
        try:
            exec('import %s' % (mod_str))
            result = eval('%s' % (mod_str))
        except Exception, ex:
            msg = 'import the script %s error! ignore it,then return None' % class_filter_name
            logger.warning(msg)
            return None
            # traceback(ex)
        obj_list = []
        for item in dir(result):
            attr = getattr(result, item)
            # print attr
            if isinstance(attr, (type, types.ClassType)):
                # get the class obj from the module obj
                testCaseNames = ['runTest']
                if class_filter_name in item.lower():
                    obj = attr()  # init a class object
                    msg = 'import the script %s and the class obj %s succeed!' % (mod_str, item)
                    logger.debug(msg)
                    obj_list.append(obj)
                else:
                    msg = ' The class name %s donnot match the filter name %s...' % (item, class_filter_name)
                    logger.warning(msg)
        if obj_list.__len__() == 0:
            logger.warning("Could not find suitable test script..." + mod_str)
        return obj_list
    #     # for item in dir(obj):
    #     #
    #     #     if 'test' in item:
    #     #         _attr = getattr(obj, item)
    #     #         if callable(_attr):
    #     #             print 'call method %s:' % item
    #     #             _attr()
    #     # testobj = map(attr, testCaseNames)
    #     # print type(item)
    #     # print dir(result)
    #
    # def _import_scripts_from_dir(self, path=None):
    #     if path is None:
    #         pass
    #
    #     pass

    def _save_script_to_db(self):
        pass

    def walk_dir(self, path):
        if not path in sys.path:
            sys.path.append(path)

        test_case_obj_list = []
        for _dir, files, names in os.walk(top=path):
            for item in names:
                _file = os.path.join(_dir, item)
                print _file
                result = self._import_script(mod_str=item)
                if result:

                    for _item in result:
                        test_case_obj_list.append(_item)
                else:
                    pass

        pass

    def testss(self):
        print 'tttttttt'


if __name__ == '__main__':
    _str = 'D:\Users\Administrator\PycharmProjects\untitled\Temp_Test\\test\\test_frame\\test_obj1.py'
    # print 'dddddddddddddddd'
    a = TestScript()
    a.walk_dir("d_script")
    # import "D:\Users\Administrator\PycharmProjects\untitled\TestFrame\python_test_frame\interface\d_script\\testCase1.py"
    a._import_script(mod_str="D:\Users\Administrator\PycharmProjects\untitled\TestFrame\python_test_frame\interface\d_script\\testCase1.py")
    # print 'ddddddddddd'
    # a.walk_dir("d_script")
    # _import_script(_str)
    # map()
    # suite = my_unittest.TestSuite()
    # suite.addTest(IntegerArithmenticTestCase)
    # suite.addTest(FloatTest)
    # my_unittest.main()
