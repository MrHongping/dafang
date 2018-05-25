# coding=utf-8

"""
@version: 1.0
@author: chaowei
@file: FileEditorCtrl.py
@time: 2018/4/1 20:16
"""
import  wx,sys

sys.path.append("..")

from utils import config
from WorkThread import HttpRequestThread

class FileEditor(wx.Panel):

    def __init__(self, parent, shellEntity,log,filePath):

        self.parent=parent
        self.shellEntity=shellEntity
        self.log = log
        self.filePath=filePath

        wx.Panel.__init__(self, parent, -1)

        bSizerMain = wx.BoxSizer(wx.VERTICAL)

        bSizerTop = wx.BoxSizer(wx.HORIZONTAL)

        self.buttonLoad = wx.Button(self, wx.ID_ANY, u"载入", wx.DefaultPosition, (50,-1), 0)
        bSizerTop.Add(self.buttonLoad, 0, wx.ALL, 2)

        self.textCtrlFilePath = wx.TextCtrl(self, wx.ID_ANY, wx.EmptyString, wx.DefaultPosition, wx.DefaultSize, 0)
        bSizerTop.Add(self.textCtrlFilePath, 1, wx.ALIGN_CENTER_VERTICAL)

        self.buttonSave = wx.Button(self, wx.ID_ANY, u"保存", wx.DefaultPosition, (50,-1), 0)
        bSizerTop.Add(self.buttonSave, 0, wx.ALL, 2)

        bSizerMain.Add(bSizerTop, 0, wx.EXPAND, 5)

        self.textCtrlFileContent = wx.TextCtrl(self, wx.ID_ANY, wx.EmptyString, wx.DefaultPosition, wx.DefaultSize,
                                               wx.HSCROLL | wx.TE_MULTILINE | wx.TE_WORDWRAP)
        bSizerMain.Add(self.textCtrlFileContent, 1, wx.ALL | wx.EXPAND, 5)

        self.SetSizer(bSizerMain)

        self.buttonSave.Bind(wx.EVT_BUTTON,self.OnSaveBtnClick)
        self.buttonLoad.Bind(wx.EVT_BUTTON,self.OnLoadBtnClick)

    def OnInit(self):

        self.textCtrlFilePath.SetValue(self.filePath)

        self.ShowFileContent(self.filePath)

    def ShowFileContent(self,filePath):
        HttpRequestThread(config.TASK_GET_FILE_CONTENT,shellEntity=self.shellEntity,path=filePath,callBack=self.Callback_getFileContent,statusCallback=self.parent.SetStatus).start()

    def Callback_getFileContent(self,resultCode,resultContent):
        if resultCode:
            self.textCtrlFileContent.SetValue(resultContent)

    def OnSaveBtnClick(self,event):

        filePath = self.textCtrlFilePath.GetValue()

        fileContent=self.textCtrlFileContent.GetValue()

        if filePath:
            HttpRequestThread(config.TASK_CREATE_FILE, shellEntity=self.shellEntity, path=filePath,content=fileContent,callBack=None, statusCallback=self.parent.SetStatus).start()

    def OnLoadBtnClick(self,event):

        filePath=self.textCtrlFilePath.GetValue()

        if filePath:
            self.ShowFileContent(filePath)
        else:
            wx.MessageBox('文件路径不能为空')

