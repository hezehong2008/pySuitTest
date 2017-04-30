#!/usr/bin/env python
# -*- coding: UTF-8 -*
import json

class JsonUtil(object):
    """
        JSON 对比的方式

    """
    JSON_CMP_MODEL = ["FULL", "KEY", "FULL_R"]
    def __init__(self):
        pass

    def cmpJosnFull(self, baseJson={}, cmpJson={}):
        """

        :param json:
        :param cmpJson:
        :return:
        """
        result = JsonCmpResult(result=True, Msg="")
        for item in baseJson.keys():
            if item in cmpJson.keys():
                if baseJson[item] != cmpJson[item]:
                    msg = "key:" + str(item)
                    result.setResult(False)
                    return result
            else:
                result = JsonCmpResult(result=False, Msg="")
                return result
        result.setMsg("")
        return result

    def comJsonKeys(self, baseJson={}, cmpJson={}):
        """
        :param json:
        :param cmpJson:
        :return:
        """
        for item in baseJson.keys():
            if item not in cmpJson.keys():
                return False
        return True

    def comJsonAllReg(self, baseJson={}, comJson={}):
        pass

    def exchangeStrToJson(self,message=None):
        pass

    @staticmethod
    def getInstance():
        return JsonUtil()


class JsonCmpResult(object):
    def __init__(self, result=False, Msg="", **kwargs):
        self.retul = result
        self.msg = Msg

    def setResult(self, result):
        self.result = result

    def getResult(self, result):
        return self.result

    def setMsg(self, msg):
        self.msg = msg

    def getMsg(self):
        return self.msg


if __name__ == "__main__":

    _json = {"name"}
    _str = '''{name:1, '项目':2}'''
    _str2 = '''{"name":false, "test":"@r=123"}'''
    # _str = json.dumps(_str)
    # json_string = json.dumps(_str2)
    j = json.loads(_str2)
    print(j)