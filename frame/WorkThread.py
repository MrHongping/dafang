# coding=utf-8

"""
@version: 1.0
@author: chaowei
@file: WorkThread.py
@time: 2018/5/21 9:29
"""
import wx, sys, os,threading,random

sys.path.append("..")
from utils.shell import ShellTools
from utils import commonsUtil,config,entity

class HttpRequestThread(threading.Thread):

    def __init__(self, action,**kwargs):
        threading.Thread.__init__(self)
        self.action=action
        self.kwargs = kwargs
        self.callBack=kwargs['callBack']
        self.statusCallback = kwargs['statusCallback']
        self.shellEntity=kwargs['shellEntity']
        self.shellTools=ShellTools.getShellTools(self.shellEntity)
        self.taskEntity=entity.TaskEntity(self.getTaskID(),self.shellEntity.shell_address,self.action)

    def getTaskID(self):
        seed = "1234567890abcdef"
        taskID = ''
        for i in range(32):
            taskID+=random.choice(seed)
        return taskID

    def parseResponse(self,response):
        if response!=None:
            responseText=response.text
            if config.SPLIT_SYMBOL_LEFT in responseText and config.SPLIT_SYMBOL_RIGHT in responseText:
                resultText=responseText[responseText.find(config.SPLIT_SYMBOL_LEFT)+len(config.SPLIT_SYMBOL_LEFT):responseText.find(config.SPLIT_SYMBOL_RIGHT)]
                if config.ERROR_LABEL in resultText:

                    self.taskEntity.taskStatus=config.ERROR_RESPONSE_WITH_SYMBOL
                    self.taskEntity.taskResult=resultText
                    wx.CallAfter(self.statusCallback, self.taskEntity)

                    return False,None

                self.taskEntity.taskStatus = config.SUCCESS_RESPONSE
                wx.CallAfter(self.statusCallback, self.taskEntity)

                return True,resultText
            else:

                self.taskEntity.taskStatus = config.ERROR_RESPONSE_NO_SYMBOL
                self.taskEntity.taskResult='错误码：{0}\r\n消息体：{1}'.format(response.status_code,response.text.replace('\r','\r\n'))
                wx.CallAfter(self.statusCallback, self.taskEntity)

                return False,None
        else:

            self.taskEntity.taskStatus = config.ERROR_DAFANG
            wx.CallAfter(self.statusCallback, self.taskEntity)

            return False, None

    def _downloadRemoteFile(self):
        path = ''
        if 'path' in self.kwargs:
            path = self.kwargs['path']
            self.taskEntity.taskContent = path

        localPath = ''
        if 'localPath' in self.kwargs:
            localPath = self.kwargs['localPath']

        fileLength = ''
        if 'fileLength' in self.kwargs:
            fileLength = self.kwargs['fileLength']

        self.taskEntity.taskStatus = config.FILE_DOWNLOADING

        count = 0
        try:
            with open(localPath, 'ab') as file:
                for data in self.shellTools.downloadFile(path):
                    if len(data) > 0:
                        # 删掉菜刀响应标识符，文件前三个字节和后三个字节
                        if count == 0:
                            data = data[len(config.SPLIT_SYMBOL_LEFT):]
                        elif count + len(data) > fileLength:
                            data = data[:fileLength - count]

                        file.write(data)

                        count += len(data)

                        self.taskEntity.taskResult = str(count) + '/' + str(fileLength)
                        wx.CallAfter(self.statusCallback, self.taskEntity)
            self.taskEntity.taskStatus = config.FILE_DOWNLOAD_SUCCESS
            self.taskEntity.taskResult=localPath
        except Exception as e:
            self.taskEntity.taskStatus = config.FILE_DOWNLOAD_ERROR
        wx.CallAfter(self.statusCallback, self.taskEntity)

    def run(self):

        self.taskEntity.taskStatus = config.REQUESTS_SENDING
        resultCode,resultContent=None,None

        path=''
        if 'path' in self.kwargs:
            path = self.kwargs['path']
            self.taskEntity.taskContent=path

        content = ''
        if 'content' in self.kwargs:
            content = self.kwargs['content']

        commandZ1 = ''
        if 'commandZ1' in self.kwargs:
            commandZ1 = self.kwargs['commandZ1']

        commandZ2 = ''
        if 'commandZ2' in self.kwargs:
            commandZ2 = self.kwargs['commandZ2']

        command = ''
        if 'command' in self.kwargs:
            command = self.kwargs['command']
            self.taskEntity.taskContent=command

        connectInfo=''
        if 'connectInfo' in self.kwargs:
            connectInfo = self.kwargs['connectInfo']

        databaseName = ''
        if 'databaseName' in self.kwargs:
            databaseName = self.kwargs['databaseName']
            self.taskEntity.taskContent = databaseName

        tableName = ''
        if 'tableName' in self.kwargs:
            tableName = self.kwargs['tableName']
            self.taskEntity.taskContent += ' : '+tableName

        queryString = ''
        if 'queryString' in self.kwargs:
            queryString = self.kwargs['queryString']
            self.taskEntity.taskContent += ' : ' + queryString


        wx.CallAfter(self.statusCallback, self.taskEntity)

        if self.action==config.TASK_GET_START:
            resultCode, resultContent=self.parseResponse(self.shellTools.getStart())
        elif self.action==config.TASK_GET_DIRECTORY_CONTENT:
            resultCode, resultContent = self.parseResponse(self.shellTools.getDirectoryContent(path))
        elif self.action==config.TASK_GET_FILE_CONTENT:
            resultCode, resultContent = self.parseResponse(self.shellTools.getFileContent(path))
        elif self.action==config.TASK_CREATE_FILE:
            resultCode, resultContent = self.parseResponse(self.shellTools.createFile(path,content))
        elif self.action==config.TASK_DELETE_FILE_OR_DIRECTORY:
            resultCode, resultContent = self.parseResponse(self.shellTools.deleteFileOrDirectory(path))
        elif self.action==config.TASK_UPLOAD_FILE:
            resultCode, resultContent = self.parseResponse(self.shellTools.uploadFile(path,content))
        elif self.action==config.TASK_DOWNLOAD_FILE:
            self._downloadRemoteFile()
        elif self.action==config.TASK_EXCUTE_COMMAND:
            resultCode, resultContent = self.parseResponse(self.shellTools.excuteCommand(commandZ1,commandZ2))
        elif self.action==config.TASK_GET_DATABASES:
            resultCode, resultContent = self.parseResponse(self.shellTools.getDatabases(connectInfo))
        elif self.action==config.TASK_GET_TABLES:
            resultCode, resultContent = self.parseResponse(self.shellTools.getTables(connectInfo,databaseName))
        elif self.action==config.TASK_GET_COLUMNS:
            resultCode, resultContent = self.parseResponse(self.shellTools.getColumns(connectInfo,databaseName,tableName))
        elif self.action==config.TASK_EXCUTE_SQLQUERY:
            resultCode, resultContent = self.parseResponse(self.shellTools.excuteSqlQuery(connectInfo,databaseName,queryString))

        if self.callBack:
            wx.CallAfter(self.callBack, resultCode, resultContent)