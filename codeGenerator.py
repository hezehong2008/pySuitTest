#!/usr/bin/env python
# -*- coding: UTF-8 -*
import lib.csvUtil as csvutil
import logging
import os
import platform
import sys
import copy

logger = logging.getLogger("scriptGenerator")
logger.setLevel(logging.DEBUG)
NORMAL_TEST = "NormalTest"
EXCEPTION_TEST = "ExceptionTest"
CONFIG_FILE = "../config.properties"
CSV_FILE = "testure"
ApiFunctonNamePrefix = "test"
delemiter = "/"
ScriptSamplePath = "etc/scriptSample.txt"
ConfigSamplePath = "etc/config.properties"
if "Windows" in platform.system():
    delemiter = "\\"
elif "Linux" in platform.system():
    pass
_script_info = {
    "TopLevel": "{exTopLevel}",
    "ApiClassName": "{exApiClassName}",
    "CsvFilePath": "{exCsvFilePath}",
    "ApiTestFunction": "{exApiTestFunction}",
    "ConfigPath": "{exConfigPath}"
}


class scriptGenerator(object):
    def __init__(self):
        self.topLevel = 2
        self.script_info_normal = {}
        self.script_info_exception = {}
        self.script_info_temp = {
            "TopLevel": "{exTopLevel}",
            "ApiClassName": "{exApiClassName}",
            "CsvFilePath": "{exCsvFilePath}",
            "ApiTestFunction": "{exApiTestFunction}",
            "ConfigPath": "{exConfigPath}"
        }
        self.script_text = open(ScriptSamplePath, "r", encoding="utf-8").readlines()
        self.config_text = open(ConfigSamplePath, "r", encoding="utf-8").readlines()

    def buildScript(self, serverPath="ddss/aa", functionName="ApiGetFloorPlan", buildType="all"):
        """
        :param serverPath: str serverName
        :param functionName:
        :param buildType: str [all, normal, exception]
        :return:
        """
        script_info_normal = {
            "TopLevel": "{exTopLevel}",
            "ApiClassName": "{exApiClassName}",
            "CsvFilePath": "{exCsvFilePath}",
            "ApiTestFunction": "{exApiTestFunction}",
            "ConfigPath": "{exConfigPath}"
        }
        script_info_exception = {
            "TopLevel": "{exTopLevel}",
            "ApiClassName": "{exApiClassName}",
            "CsvFilePath": "{exCsvFilePath}",
            "ApiTestFunction": "{exApiTestFunction}",
            "ConfigPath": "{exConfigPath}"
        }

        if serverPath is None:
            serverPath = "default"
        topLevel = 2
        if "\\" not in serverPath and "/" not in serverPath:
            topLevel = 1

        self.topLevel = topLevel

        _dir = None

        if topLevel == 1:
            _dir = "test_case/" + serverPath
            script_info_normal["TopLevel"] = "../../"
            script_info_exception["TopLevel"] = "../../"
            script_info_normal["ConfigPath"] = "../config.properties"
            script_info_exception["ConfigPath"] = "../config.properties"
        elif topLevel == 2:
            if "\\" in serverPath:
                serverPath.replace("\\", "/")
            _dir = "test_case/" + serverPath
            if not os.path.exists(_dir):
                os.makedirs(_dir)

            script_info_normal["TopLevel"] = "../../../"
            script_info_normal["ConfigPath"] = "../config.properties"

            script_info_exception["TopLevel"] = "../../../"
            script_info_exception["ConfigPath"] = "../config.properties"

        script_info_normal["ApiClassName"] = functionName+ NORMAL_TEST
        script_info_exception["ApiClassName"] = functionName + EXCEPTION_TEST
        script_info_normal["ApiTestFunction"] = ApiFunctonNamePrefix + functionName+ "Normal"
        script_info_exception["ApiTestFunction"] = ApiFunctonNamePrefix + functionName + "Exception"
        script_info_normal["CsvFilePath"] = CSV_FILE + "/" + functionName + NORMAL_TEST + ".csv"
        script_info_exception["CsvFilePath"] = CSV_FILE + "/" + functionName + EXCEPTION_TEST + ".csv"
        self.script_info_normal = script_info_normal
        self.script_info_exception = script_info_exception

        script_file_normal = _dir + "/" + functionName + NORMAL_TEST + ".py"
        script_file_exception = _dir + "/" + functionName + EXCEPTION_TEST + ".py"
        config_file_path = os.path.join(_dir, CONFIG_FILE)
        csv_file_path_normal = _dir + "/" + CSV_FILE + "/" + functionName + NORMAL_TEST + ".csv"
        csv_file_path_exception = _dir + "/" + CSV_FILE + "/" + functionName + EXCEPTION_TEST + ".csv"

        logging.debug("生成配置文件:" + os.path.realpath(config_file_path))
        self.buildConfigFile(filePath=config_file_path)

        if buildType.lower() == "exception":
            self.buildExceptionScript(filePath=script_file_exception)
            self.buildCsvFileException(filePath=csv_file_path_exception)
        elif buildType.lower() == "normal":
            self.buildCsvFileNormal(filePath=csv_file_path_normal)
            self.buildNormalScript(filePath=script_file_normal)
        else:
            self.buildCsvFileNormal(filePath=csv_file_path_normal)
            self.buildNormalScript(filePath=script_file_normal)
            self.buildExceptionScript(filePath=script_file_exception)
            self.buildCsvFileException(filePath=csv_file_path_exception)

    def buildCsvFileNormal(self, filePath=None):
        logger.info("生成正常测试脚本CSV驱动数据文件..." + os.path.realpath(filePath))
        _dir = os.path.dirname(filePath)
        if not os.path.exists(_dir):
            os.makedirs(_dir)
        if os.path.exists(filePath):
            logging.warning("csv normal file is exits..." + os.path.realpath(filePath))
            return None
        else:
            # fp = open(os.path.realpath(filePath), "w")
            csvutil.csvWriterBase(filePath=os.path.abspath(filePath))

    def buildCsvFileException(self, filePath=None):
        logger.info("生成异常测试脚本CSV驱动数据文件..." + os.path.realpath(filePath))
        _dir = os.path.dirname(filePath)
        if not os.path.exists(_dir):
            os.makedirs(_dir)
        if os.path.exists(filePath):
            logging.warning("csv exception file is exits..." + os.path.realpath(filePath))
            return None
        else:
            # fp = open(os.path.realpath(filePath), encoding="utf-8", mode="w")
            csvutil.csvWriterBase(filePath=os.path.abspath(filePath))

    def buildScriptAll(self, filePath=None):
        os.path.dirname(filePath)

    def buildNormalScript(self, filePath=None):
        """

        :param filePath:
        :return:
        """
        logger.info("生成正常测试脚本..." + os.path.realpath(filePath))
        _dir = os.path.dirname(filePath)
        if not os.path.exists(_dir):
            os.makedirs(_dir)
        if os.path.exists(filePath):
            logging.warning("script file is exits..." + os.path.realpath(filePath))
            return None
        else:
            fp = open(os.path.realpath(filePath), encoding="utf-8", mode="w")
            s = copy.deepcopy(self.script_text)
            # s = s.encode("GBK")
            for i in range(len(s)):
                for key in self.script_info_temp.keys():
                    # s.replace(self.script_info_temp[key], self.script_info_normal[key])
                    if self.script_info_temp[key] in s[i]:
                        s[i] = s[i].replace(self.script_info_temp[key], self.script_info_normal[key])
            for i in range(len(s)):
                fp.write(s[i])
            # fp.write(s)
            fp.close()

    def buildConfigFile(self, filePath=None):
        logger.info("生成配置文件..." + os.path.realpath(filePath))
        _dir = os.path.dirname(filePath)
        if not os.path.exists(_dir):
            os.makedirs(_dir)
        if os.path.exists(filePath):
            logging.warning("script file is exits..." + os.path.realpath(filePath))
            return None
        else:
            fp = open(os.path.realpath(filePath), encoding="utf-8", mode="w")
            s = copy.deepcopy(self.config_text)
            # s = s.encode("GBK")
            for i in range(len(s)):
                fp.write(s[i])
            # fp.write(s)
            fp.close()

    def buildExceptionScript(self, filePath=None):
        logger.info("生成异常测试脚本..." + os.path.realpath(filePath))
        _dir = os.path.dirname(filePath)
        if not os.path.exists(_dir):
            os.makedirs(_dir)
        if os.path.exists(filePath):
            logging.warning("script file is exits..." + os.path.realpath(filePath))
            return None
        else:
            fp = open(os.path.realpath(filePath), encoding="utf-8", mode="w")
            s = copy.deepcopy(self.script_text)
            # s = s.encode("GBK")
            for i in range(len(s)):
                for key in self.script_info_temp.keys():
                    # s.replace(self.script_info_temp[key], self.script_info_normal[key])
                    if self.script_info_temp[key] in s[i]:
                        s[i] = s[i].replace(self.script_info_temp[key], self.script_info_exception[key])
            for i in range(len(s)):
                fp.write(s[i])
            # fp.write(s)
            fp.close()

if __name__ == "__main__":
    generator = scriptGenerator()
    generator.buildScript(serverPath="apiGetFloopPlan", functionName="ApiGetFloorPlan")