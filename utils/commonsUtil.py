# coding=utf-8

"""
@version: 1.0
@author: chaowei
@file: commonUtil.py
@time: 2018/3/27 20:12
"""

def isDirectory(itemName):
    if ((itemName.rfind('/') == len(itemName) - 1) or (itemName.rfind('\\') == len(itemName) - 1)):
        return True
    else:
        return False

from threading import Thread


class ThreadWithReturnValue(Thread):
    def __init__(self, target, args=()):
        super(ThreadWithReturnValue, self).__init__()
        self._target=target
        self._args=args
        self._return = None

    def run(self):
        if self._target is not None:
            self._return = self._target(*self._args)

    def join(self,timeout=None):
        Thread.join(self,timeout=timeout)
        return self._return