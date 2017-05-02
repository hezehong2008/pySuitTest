#
#
#
#

#!/usr/bin/env python
# -*- coding: UTF-8 -*


class TestResult(object):
    result = ["PASS", "NEF", "FAIL", "NONE"]
    FAIL = "FAIL"     # 测试失败
    PASS = "PASS"     # 测试通过
    NAN = "NAN"       # 无结果...（无校验数据）
    ERROR = "ERROR"  # 表示有异常....

    def __init__(self, result, comment="", detail=""):
        self.comment = comment
        self.result = result
        self.detail = detail

    def setResult(self, result):
        self.result = result

    def getResult(self):
        return self.result

    def getComment(self):
        return self.comment

    def setComment(self, comment):
        self.comment = comment

    def getDetail(self):
        return self.detail

    def setDetail(self, detail):
        self.detail = detail

    @classmethod
    def getTestResult(cls, result, comment=None, detail=None):
        return TestResult(result=result, comment=comment, detail=detail)
