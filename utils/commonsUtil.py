# coding=utf-8

"""
@version: 1.0
@author: chaowei
@file: commonUtil.py
@time: 2018/3/27 20:12
"""

def isDirectory(itemName):
    result=True if (itemName.rfind('/') == len(itemName) - 1) else False
    return result