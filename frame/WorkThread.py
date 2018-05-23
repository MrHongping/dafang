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

    def run(self):

        self.taskEntity.taskStatus = config.REQUESTS_SENDING
        resultCode,resultContent=None,None

        path=''
        if 'path' in self.kwargs:
            path = self.kwargs['path']
            self.taskEntity.taskContent=path

        wx.CallAfter(self.statusCallback, self.taskEntity)

        if self.action==config.TASK_GET_START:
            resultCode, resultContent=self.parseResponse(self.shellTools.getStart())
        elif self.action==config.TASK_GET_DIRECTORY_CONTENT:
            resultCode, resultContent = self.parseResponse(self.shellTools.getDirectoryContent(path))

        if self.callBack:
            wx.CallAfter(self.callBack, resultCode, resultContent)