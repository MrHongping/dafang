# coding=utf-8

"""
@version: 1.0
@author: chaowei
@file: logger.py
@time: 2018/5/13 15:23
"""

import logging.handlers

class RuntimeLogger(object):
    def __init__(self, path='runtime.log'):
        self.__path = path

        self.__logger = logging.getLogger('RuntimeLogger')
        # midnight:午夜进行新的日志文件生成，1:一天一个,30:最多存放30个文件，超过则从最早的开始删除
        hdlr = logging.handlers.TimedRotatingFileHandler(path, 'midnight', 7, 30)
        formatter = logging.Formatter('%(asctime)s %(levelname)s %(message)s')
        hdlr.setFormatter(formatter)
        self.__logger.addHandler(hdlr)
        self.__logger.setLevel(logging.INFO)

    def d(self, msg=''):
        if not isinstance(msg, basestring):
            msg = str(msg)
        self.__logger.info(msg)

    def i(self, msg=''):
        if not isinstance(msg, basestring):
            msg = str(msg)
        self.__logger.info(msg)

    def e(self, msg=''):
        if not isinstance(msg, basestring):
            msg = str(msg)
        self.__logger.exception(msg)


log = RuntimeLogger('runtime.log');
log.i("-----------------RUNTIME LOG initialized----------------------")