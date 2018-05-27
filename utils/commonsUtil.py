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

from xml.etree import ElementTree

def get_dbInfo(xmlStr,nodeStr):
    root = ElementTree.fromstring(xmlStr)
    node_find = root.find(nodeStr)
    if node_find is not None:
        return node_find.text
    else:
        return None

