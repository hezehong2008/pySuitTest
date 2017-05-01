#!/usr/bin/env python
# -*- coding: UTF-8 -*
import logging
import os
import time
import sys
# sys.setdefaultencoding('gbk')
CRITICAL    = logging.CRITICAL
FATAL       = CRITICAL
ERROR       = logging.ERROR
WARNING     = logging.WARNING
WARN        = WARNING
INFO        = logging.INFO
DEBUG       = logging.DEBUG
NOTSET      = logging.NOTSET
TESTCASE    = 60
TESTSUITE   = 70
STEP        = 25 # between INFO and WARN

conf_file_path = '../etc/logger.conf'
LOGGING_LEVEL = logging.DEBUG
LOGGING_FORMATTER = "%(asctime)s - %(name)s - %(levelname)s - %(message)s"

# logging.config.fileConfig(conf_file_path)
logging.addLevelName(TESTCASE, 'TESTCASE')
logging.addLevelName(TESTSUITE, 'TESTSUITE')
logging.addLevelName(STEP, 'STEP')

# logging.basicConfig(level=logging.DEBUG,
#                     format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
#                     filename="test.log",
#                     filemode='w')
# logger.setLevel(logging.DEBUG)
# create console handler and set level to debug
# ch = logging.StreamHandler()
# ch.setLevel(logging.NOTSET)
# # create formatter
# formatter = logging.Formatter("%(asctime)s - %(name)s - %(levelname)s - %(message)s")
# # add formatter to ch
# ch.setFormatter(formatter)
# add ch to logger
# logger.addHandler(ch)


def set_logging_file(filepath=None):
    if os.path.isfile(filepath):
        if os.path.exists(filepath):
            pass
        else:
            os.makedirs(os.path.dirname(filepath))
    # os.makedirs(os.path.dirname(filepath))
    time.sleep(1)
    if not os.path.isfile(filepath):
        logging.warning("The config filepath %s is not exit, then create...." % filepath)
        # os.makedirs(os.path.dirname(filepath))
    logging.debug("************************")
    logger = logging.getLogger("test")
    logger.debug("tttttttttttttt")
    logging.basicConfig(level=logging.DEBUG,
                        format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
                        filename=filepath,
                        filemode='w')
    logging.debug("************************")


def add_logger_hander(logger, filepath):
    fh = logging.FileHandler(filepath)
    fh.setLevel(LOGGING_LEVEL)
    fh.setFormatter(LOGGING_FORMATTER)
    cn = logging.StreamHandler()
    cn.setLevel(LOGGING_LEVEL)
    cn.setFormatter(LOGGING_FORMATTER)

# logging.getLogger().handlers = []
def set_logger_config(logger, filepath):

    if not os.path.isfile(filepath):
        _dir = os.path.dirname(filepath)
        if os.path.exists(filepath):
            pass
        else:
            if not os.path.exists(os.path.dirname(filepath)):
                os.makedirs(os.path.dirname(filepath))
    # os.makedirs(os.path.dirname(filepath))
    time.sleep(1)
    if not os.path.isfile(filepath):
        logger.warning("The config filepath %s is not exit, then create...." % filepath)
        # os.makedirs(os.path.dirname(filepath))
    logging.basicConfig(level=logging.DEBUG,
                        format=LOGGING_FORMATTER,
                        filename=filepath,
                        filemode='w')
    formatter = logging.Formatter(LOGGING_FORMATTER)
    fh = logging.FileHandler(filepath)
    fh.setLevel(LOGGING_LEVEL)
    fh.setFormatter(formatter)

    # logger.addHandler(fh)
    # logger.addHandler(cn)
    # logger.setp = logger_step
    logging.getLogger().addHandler(fh) # add root hander

    # aa = logging.getLogger().handlers


def setSreamHandler():
    cn = logging.StreamHandler()
    cn.setLevel(LOGGING_LEVEL)
    cn.setFormatter(logging.Formatter(LOGGING_FORMATTER))
    logging.getLogger().addHandler(cn)

def logger_step(logger, message, *args, **kws):
    # Yes, logger takes its '*args' as 'args'.
    if logger.isEnabledFor(STEP):
        logger._log(STEP, message, args, **kws)


class pyLogger(object):
    logger = None
    logger_list = []
    @classmethod
    def getLogger(cls, name=None):
        if pyLogger.logger is None:
            pass
# logging.basicConfig(level=logging.DEBUG,
#                     format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
#                     filename="test.log",
#                     filemode='w')
# logging.root.setLevel(logging.DEBUG)
# # create console handler and set level to debug
# ch = logging.StreamHandler()
# ch.setLevel(logging.DEBUG)
# # create formatter
# formatter = logging.Formatter("%(asctime)s - %(name)s - %(levelname)s - %(message)s")
# # add formatter to ch
# ch.setFormatter(formatter)
# # add ch to logger
# logging.root.addHandler(ch)


# def logger_step_method(self, message, *args, **kws):
#     if not hasattr(self, "isEnableFor"):
#         # print("abcdef")
#         self.isEnableFor = logging.Logger.isEnabledFor
#     self.debug(message)
    # if self.isEnableFor(level=STEP):
    #     self._log(STEP, message, args, **kws)

# logging.Logger.step = logger_step_method
# logger = logging.getLogger("logger")
# logger.setLevel(logging.DEBUG)
# # create console handler and set level to debug
# ch = logging.StreamHandler()
# ch.setLevel(logging.DEBUG)
# # create formatter
# formatter = logging.Formatter("%(asctime)s - %(name)s - %(levelname)s - %(message)s")
# # add formatter to ch
# ch.setFormatter(formatter)
# # add ch to logger
# logger.addHandler(ch)
# logger.debug("dffffffffffffffffff")