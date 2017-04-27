import unittest
import sys
import time
import os
import traceback
import copy
from enum import Enum
sys.path.append(r'../lib/')
sys.path.append(r'../http/')
sys.path.append(r"D:\Users\admin\PycharmProjects\PyTestFrame\interface\http")
from csvUtil import csvutil as PrepareDataUtil
from configUtil import configParser
from httpRequest import http_request
from httpRequest import httpResult
try:
    import PyLogger as pylogger
    from PyLogger import logging
except:
    import logging
logger = logging.getLogger("ApiTestSuit")
logger.setLevel(logging.DEBUG)
STEP = 25 # between INFO and WARN


class ApiTestSuit(unittest.TestCase):

    def initConfig(self):
        self.step = """
                            Step1 初始化运行上下文对象 initContext
                            Step2 加载测试配置文件config，包含登陆信息、域名信息等
                            Step3 加载测试脚本的数据csv文件，并且生成测试用例,每一个用例包含一个context对象
                            Step4 根据生成测试用例调用runHttpTest
                            Step5 根据csv文件对比返回结果
        """
        """
        PySuit
        1.技术方案选型
        2.python，java
        3.后端、前端
        4.设计思路、思想
        5.数据结构设计
        6.流程图设计
        """
        """
            runContext ---

        """

        self.setLogger()

        logger.step(self.step)
        logger.step("初始化上下文对象....")
        logger.debug("创建全局runContext对象.....")

        self.runContext = runContext()
        if os.name == "nt":
            pass
        _path = os.path.join(os.path.dirname(self.script_dir), self.config_path)
        # print(os.path.dirname(self.script_dir))
        logger.debug("初始化配置数据,生成configData对象..." + _path)
        self.runContext.configData = ConfigData(configPath=_path)
        logger.debug("加载配置文件成功..." + str(self.runContext.configData))
        obs_path = os.path.abspath(self.script_file)
        if obs_path.endswith(".py"):
            obs_path = os.path.dirname(obs_path)
        _path = os.path.join(obs_path, self.testure_path)
        logger.step("加载csv数据文件，生成prepareDataList对象...." + _path)
        self.caseNum = PrepareData(csv_file_path=_path, index=0).caseNum
        self.runContext.prepareDataList = []
        for i in range(self.caseNum):
            self.runContext.prepareDataList.append(PrepareData(csv_file_path=_path, index=i))
        logger.debug("加载csv数据文件成功...." + str(self.runContext.prepareDataList[0]) + "...")
        # self.runContext.prepareDataList = PrepareData(csv_file_path=_path, index=0)
        logger.debug("创建全局runContext对象成功.....包含csv数据、配置数据信息...")
        logger.debug("创建运行的http_request对象.....httpClient")
        self.httpClient = http_request()

    def getScriptServerName(self, file_path):
        _path = os.path.dirname(file_path)
        return os.path.basename(_path)

    def getScriptFileName(self, file_path):
        return os.path.basename(file_path)

    def startTest(self , runContext):
        logger.debug("start run test...." + self.__class__.__name__)
        # self.beforeClassTest(Context=runContext)
        logger.debug("")
        result = True
        logger.step("开始运行测试用例.....共有" + str(self.caseNum) + "个测试用例")
        for i in range(len(self.runContext.prepareDataList)):
            logger.step("开始运行第 " + str(i+1) + " 个测试用例")

            self.currentContex = Context(runContext.prepareDataList[i], runContext.configData)
            self.currentContex.httpClient = self.httpClient
            self.beforeHttpTest(context=self.currentContex)
            self.runHttpTest(context=self.currentContex)
            self.afterHttpTest(context=self.currentContex)
            # try:
            #     self.beforeHttpTest(context=self.currentContex)
            #     self.runHttpTest(context=self.currentContex)
            #     self.afterHttpTest(context=self.currentContex)
            # except Exception:
            #     result = False
            #     logger.warning("TestCase error....")
            #     logger.error(traceback.print_exc(Exception))
            # finally:
            runContext.currentCaseNum += 1


        self.afterClassTest(context=Context)

        self.assertTrue(result, "Test Result ....")

    def beforeHttpTest(self, context):
        pass
        # print(sys._getframe().f_code.co_name)

    def afterHttpTest(self, context):
        pass
        # print(sys._getframe().f_code.co_name)

    def beforeClassTest(self, context):
        pass
        # print(sys._getframe().f_code.co_name)

    def afterClassTest(self, context):
        pass
        # print(sys._getframe().f_code.co_name)

    def runHttpTest(self, context):
        # print(Context.isNeedLogin)
        if not context.isNeedLoginFirst():
            logger.info("当前用例不需要登录....跳过登录")
        else:
            # logger.debug()
            logger.debug("开始登录....")
            _str = str(self.doLogin(Context))
            logger.debug("登录成功....返回:" + _str)
        logger.info("开始执行http方法....")

        strMsg = context.getStrSendText()
        headers = context.getHttpSendHeaders()
        httpType = context.getHttpType()

        url = context.getBaseUrl() + context.getHttpSendUrl()
        if httpType is None or httpType == "":
            logger.warning("httpType is none")
            httpType = HttpMethod.GET

        httpResult = None

        if httpType.upper() == HttpMethod.GET.value:
            httpResult = context.httpClient.requestWithGet(url=url, headers=headers, isLogin=False, entity=None)
        elif httpType.upper() == str(HttpMethod.POST.value):
            httpResult = context.httpClient.requestWithPost(url=url, headers=headers, isLogin=False, entity=strMsg)
        elif httpType.upper() == HttpMethod.HEAD.value:
            httpResult = context.httpClient.requestWithHead(url=url, headers=headers, isLogin=False, entity=strMsg)
        elif httpType.upper() == HttpMethod.OPTIONS.value:
            httpResult = context.httpClient.requestWithOption(url=url, headers=headers, isLogin=False, entity=strMsg)
        elif httpType.upper() == HttpMethod.DELETE.value:
            httpResult = context.httpClient.requestWithDelete(url=url, headers=headers, isLogin=False, entity=strMsg)
        elif httpType.upper() == HttpMethod.PUT.value:
            httpResult = context.httpClient.requestWithPut(url=url, headers=headers, isLogin=False, entity=strMsg)
        else:
            pass
            # raise RuntimeError("httpType do not exit..." + httpType)
        context.setHttpResult(httpResult)

        self.checkResult(context=context)
        logger.info("执行完毕....")

    def doLogin(self, Context):
        pass
        #_str = Context.

    def setLogger(self):
        self.logger = logging.getLogger(self.sub_class_name)
        ISOTIMEFORMAT ='%Y-%m-%d_%H_%M_%S'
        _time = time.strftime(ISOTIMEFORMAT, time.localtime())
        # self.logger = logger
        logger.step = self.logger_step
        serverNmae = self.getScriptServerName(self.script_dir)
        file_name = self.getScriptFileName(self.script_dir)
        logger_name = self.sub_class_name + "_" + _time + ".log"
        log_ = r"../../../log/%s/%s/" % (serverNmae, file_name)
        log_ = log_ + logger_name
        self.log_file = os.path.abspath(log_)
        log_file = os.path.join(os.getcwd(), log_)
        pylogger.set_logger_config(logger=logger, filepath=self.log_file)

    def logger_step(self, message, *args, **kws):
        # Yes, logger takes its '*args' as 'args'.
        if logger.isEnabledFor(STEP):
            logger._log(STEP, message, args, **kws)

    def getRelativePath(self, fatherPath, subPath):
        pass

    # def runTest(self):
    #     logger.info("PASSS")

    def checkResult(self, context):
        pass

    def checkDb(self, context):
        pass

    def checkJson(self, context):
        pass


class runContext(object):
    def __init__(self):
        """
                runContext 代表一个脚本中的运行上下文

        """
        # *** 当前http返回的结果
        self.currentHttpResult = None  # a obj of httpResult
        # *** 所有的http 返回结果
        self.httpResultList = None  # a list of currentHttpResult list
        # *** 当前csv配置数据
        self.currentPareData = None
        # *** 所有的csv 配置文件 parepareDataList, a [] for obj parepareData
        self.prepareDataList = None  # a list of PrepareData object
        # ***
        # 服务中的配置文件
        self.configData = None
        #
        # 当前用例运行的位置 【】
        self.currentCaseNum = 0
        #
        self.contextList = []

        self.currentContext = None

    def isNeedLoginFirst(self):
        pass

    def getConfigData(self):
        return self.configData

    def setConfigData(self, configData):
        self.configData = configData

    def __setitem__(self, key, value):
        if key not in self.__dict__.keys():
            raise RuntimeError("Could not define the key by yourself "
                               "in runContext obj..." + key)
        self.__dict__[key] = value

    def __getitem__(self, item):
        return self.__dict__[item]

    def __getattr__(self, item):
        if item.startswith("get"):
            _str = ""
            item = item[3:len(item)]
            _str = item[0].lower() + item[1:len(item)]
            if hasattr(self, _str):
                obj = getattr(self, _str)
                if callable(obj):
                    pass  # skip callable object
                else:
                    return lambda: self.__getitem__(_str)
            else:
                # print(hasattr(self, _str))
                raise AttributeError("The param do not exit in PrepareData object..." + _str)
        elif item.startswith("set"):
            _str = ""
            item = item[3:len(item)]
            _str = item[0].lower() + item[1:len(item)]
            if hasattr(self, _str):
                obj = getattr(self, _str)
                if callable(obj):
                    pass  # skip callable object
                else:
                    return lambda word: self.__setitem__(_str, word)
            else:
                # print(hasattr(self, _str))
                raise AttributeError("The param do not exit in PrepareData object..." + _str)

        else:
            raise AttributeError("The param do not exit in PrepareData object..." + item)

    def __repr__(self):
        return ""


class Context(object):
    def __init__(self, PrepareDataObj, ConfigDataObj):
        self.prepareData = PrepareDataObj
        self.configDataObj = ConfigDataObj
        # *************   当前用例的http配置  ****************
        #             Http类型，头部，body，url部分
        self.httpType = PrepareDataObj["httpType"]
        # http发送的
        self.strSendText = PrepareDataObj["strSendText"]
        # http的发送的url链接
        self.httpSendUrl = PrepareDataObj["httpSendUrl"]
        #
        self.httpSendHeaders = PrepareDataObj["httpSendHeaders"]
        #
        self.isRun = PrepareDataObj["isRun"]
        #
        self.httpClient = None
        #
        # ************ 当前用例的登录配置  ****************
        self.isNeedLogin = PrepareDataObj["isNeedLogin"]
        # ***
        self.caseId = PrepareDataObj["caseId"]
        # ***
        self.baseUrl = ConfigDataObj["reomveUrl"]
        self.loginUrl = ConfigDataObj["loginUrl"]
        # ************ 结果返回配置   ******************
        self.httpResult = httpResult()
        #
    def getBaseUrl(self):
        return self.baseUrl
    
    def isNeedLoginFirst(self):
        return self.isNeedLogin

    def getHttpResult(self):
        return self.httpResult

    def setHttpResult(self, httpResult):
        self.httpResult = httpResult

    def getStrSendText(self):
        return self.strSendText

    def setStrSendText(self, text):
        self.strSendText = text

    def getHttpSendUrl(self):
        return self.httpSendUrl

    def setHttpSendUrl(self, url):
        self.httpSendUrl = url

    def getHttpSendHeaders(self):
        return self.httpSendHeaders

    def setHttpSendHeaders(self, headers):
        self.httpSendHeaders = headers

    def getHttpType(self):
        return self.httpType

    def setHttpType(self, httpType):
        self.httpType = httpType


class ConfigData(object):
    def __init__(self, configPath=""):
        self.configPath = configPath
        self.loginUrl = None
        self.reomveUrl = None
        self.dbType = None
        self.dbPassword = None
        self.dbUsername = None
        self.dbUrl = None
        self.usernameInfo = None  # a dirt such as {"account":ApiTest@163.com}
        self.passwordInfo = None    # a dirt such as {"password":"1233456"}
        self.username = None
        self.password = None
        self.configParase = configParser(configPath=configPath)
        self.initParam()

    def initParam(self):
        if not os.path.isfile(self.configPath):
            raise RuntimeError("配置文件路径错误..." + self.configPath)
        _parse = self.configParase
        self.loginUrl =  _parse["loginHost"]
        self.reomveUrl = _parse["remoteUrl"]
        self.dbUrl = _parse["db_url"]
        self.dbUsername = _parse["db_username"]
        self.dbPassword = _parse["db_password"]

        self.passwordInfo = _parse["logginPassword"]
        self.usernameInfo = _parse["logginName"]
        if ":" in self.passwordInfo:
            self.usernameInfo = self.usernameInfo.replace(" ", "")
            self.username = self.usernameInfo.split(":")[1]
            # self.usernameInfo = {self.username}
        else:
            self.username = self.usernameInfo

        if ":" in self.passwordInfo:
            self.passwordInfo = self.passwordInfo.replace(" ", "")
            self.password = self.passwordInfo.split(":")[1]
        else:
            self.password = self.passwordInfo

    def getLoginDict(self):
        pass

    def getLoginUrl(self):
        return self.loginUrl

    def setLoginUrl(self, url):
        self.loginUrl = url

    def __setitem__(self, key, value):
        if key not in self.__dict__.keys():
            raise RuntimeError("Could not define the key by yourself "
                               "in runContext obj..." + key)
        self.__dict__[key] = value

    def __getitem__(self, item):
        return self.__dict__[item]

    def __str__(self):
        return str(self.__dict__)


class PrepareData(object):
    def __init__(self, csv_file_path, index):
        # / ** 测试用例ID * /
        self.caseId = None
        # / ** 测试用例详情 * /
        self.caseDesc = ""
        # / ** 当前用例是否运行 * /
        self.isRun = True
        # /** 测试用例优先级，P0做为冒烟测试用例 */
        self.priority = None
        # /**  HTTP请求方式  */
        self.httpType = None
        # /**  请求服务 */
        self.apiPath = None  # str
        # /**  发送请求的参数 */
        self.mapSendParam = None  # dict
        # /**  post请求中，直接在url中的参数 */
        self.mapPostUrlParam = None   # dict
        # /**  发送请求的http 的Header参数 */
        self.mapHttpHeadParam = None  # dict
        # /**  需要比较的JSON内容  */
        self.retMapJsonAssert = None
        # /**  其他需要的参数  */
        self.mapUserParam = None  # dict
        # /**  期望返回的返回码  */
        self.exceptRetCode = None  # int
        # /** 是否需要登录
        self.isNeedLogin = True
        # / **　期望比较的json 对象
        self.verfiyJson = {
            "rkey-key1": "rVal-Value1",
            "key-key1": "Val-Value1"
        }
        # key/rkey 代表键对、正则表达式
        # 同理 val/rVal 代表普通对比、正则表达式

        # / ** 期望对比结果方式
        self.compareJsonType = ["OnlyKey", "ALL", "R"]
        # 1.对比是否包含json的key
        # 2.对比包含json 的 key--value
        # 3.对比正则表达式匹配json的 key -- value 字段

        # /**** http param ******/
        self.strSendText = None
        # / **url, headers={} , entity=None
        self.httpSendUrl = None
        # /
        self.httpSendHeaders = None  # {} dict
        # /
        # ***************  not user *************************************
        # /**  需要先进行构造的数据库数据  */
        self.mapInsertDb = None
        # /**  需要比较的数据库  */
        self.retMapDbAssert = None
        # ***************  not user *************************************
        self.csvList = None
        self._prepareDataUtil = PrepareDataUtil(csv_file_path)
        self.caseNum = len(self._prepareDataUtil.csv_list)
        self.initParam(csv_file_path=csv_file_path, index=index)

     # ***************************  not finish ***************************************

    def initParam(self, csv_file_path="", index=0):
        """

        :param csv_file_path:
        :param index:
        :return:
        """
        if self._prepareDataUtil:
            _prepareData = PrepareDataUtil(csv_file_path)
        else:
            _prepareData = self._prepareDataUtil

        self.setCaseId(_prepareData.getCaseId(index=index))
        self.caseDesc = _prepareData.getCaseDesc(index=index)
        self.isRun = _prepareData.getIsRun(index=index)
        self.priority = _prepareData.getPriority(index=index)
        self.httpType = _prepareData.getHttpType(index=index)
        self.apiPath = _prepareData.getApiPath(index=index)
        self.exceptRetCode = _prepareData.getVerifyReCode(index=index)
        self.mapSendParam = _prepareData.getMapSendParam(index=index)

        self.mapUserParam = _prepareData.getMapUserParam(index=index)
        self.verfiyJson = _prepareData.getVerfiyJson(index=index)
        self.mapHttpHeadParam = _prepareData.getMapHttpHeadParam(index=index)
        self.mapPostUrlParam = _prepareData.getMapPostUrlParam(index=index)
        self.strSendText = _prepareData.getStrSendText(index=index)
        self.httpSendHeaders = _prepareData.getHttpSendHeaders(index=index)
        self.httpSendUrl = _prepareData.getHttpSendUrl(index=index)
        self.isNeedLogin = _prepareData.getIsLogin(index=index)

    def getInstance(self, index=0):
        pass

    def getMapSendParamFromCsv(self, csv_list, index):
        """

        :param csv_list:   LIST 、                this list for csv file
        :param index:      int  、                the index of row for the csv file
        :return:           Objcet(PrepaareData)、 the PrepareData Objcet

        """
        pass

    def getCaseIdFromCsv(self, csv_list, index):
        pass

    def getPrepareDataObjFromCsv(self, csv_list, index):
        pass

    def __setitem__(self, key, value):
        if key not in self.__dict__.keys():
            raise RuntimeError("Could not define the key by yourself "
                               "in runContext obj..." + key)
        self.__dict__[key] = value

    def __getitem__(self, item):

        return self.__dict__[item]

    def __getattr__(self, item):
        if item.startswith("get"):
            _str = ""
            item = item[3:len(item)]
            _str = item[0].lower() + item[1:len(item)]
            if hasattr(self, _str):
                obj = getattr(self, _str)
                if callable(obj):
                    pass  # skip callable object
                else:
                    return lambda: self.__getitem__(_str)
            else:
                # print(hasattr(self, _str))
                raise AttributeError("The param do not exit in PrepareData object..." + _str)
        elif item.startswith("set"):
            _str = ""
            item = item[3:len(item)]
            _str = item[0].lower() + item[1:len(item)]
            if hasattr(self, _str):
                obj = getattr(self, _str)
                if callable(obj):
                    pass  # skip callable object
                else:
                    return lambda word: self.__setitem__(_str, word)
            else:
                # print(hasattr(self, _str))
                raise AttributeError("The param do not exit in PrepareData object..." + _str)

        else:
            raise AttributeError("The param do not exit in PrepareData object..." + item)

    def __str__(self):
        return str(self.__dict__)


class HttpMethod(Enum):
    GET = "GET"
    POST = "POST"
    HEAD = "HEAD"
    OPTIONS = "OPTIONS"
    PUT = "PUT"
    DELETE = "DELETE"
    TRACE = "TRACE"


if __name__ == "__main__":
    context = runContext()
    print(type(HttpMethod.POST), str(HttpMethod.POST.name))
    print(HttpMethod.POST.value)
    # context["baseUrl"] = "aaa"
    # file_path = "D:\\Users\Administrator\PycharmProjects\\untitled\TestFrame\python_test_frame\interface\\test_case\dds\ApiGetFloorPlan\\testure\ApiGetFloorPlanNormal.csv"
    # pare = PrepareData(csv_file_path=file_path, index=0)
    # print(pare.getCaseDesc())
    # print(pare.getCaseDesc())
    # print(pare.setCaseDesc("test"))
    # print(pare.getCaseDesc())
    # print(ConfigData)

    # print(pare.getCaseDesc3())
    # print(context["caseId"])
    pass