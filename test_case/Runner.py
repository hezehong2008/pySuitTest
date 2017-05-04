# coding = utf-8
import sys
sys.path.append(r'../../')
import unittest
from lib import HTMLTestRunner
import time, os

listcasedir = r"D:\Users\admin\PycharmProjects\git\pySuitTest\test_case\dds\ApiGetFloorPlan"


def creatsuitel():
    testunit = unittest.TestSuite()
    # discover方法定义
    discover = unittest.defaultTestLoader.discover(listcasedir, pattern='*.py', top_level_dir=None)

    # discover 方法筛选出来的用例，循环添加到测试套件中
    for test_suite in discover:
        for test_case in test_suite:
            testunit.addTests(test_case)
            print(testunit)
    return testunit


alltestnames = creatsuitel()

now = time.strftime("%Y-%m-%M-%H_%M_%S", time.localtime(time.time()))
filename = r"D:\Users\admin\PycharmProjects\git\pySuitTest\test_case\dds\ApiGetFloorPlan\{0}result.html".format(now)
print(filename)
fp = open(filename, 'wb')
# 执行测试用例
runner = HTMLTestRunner.HTMLTestRunner(stream=fp, title='百度搜索测试报告', description='测试执行情况')
runner.run(alltestnames)