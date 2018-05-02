# coding=utf-8

"""
@version: 1.0
@author: chaowei
@file: FileEditorCtrl.py
@time: 2018/4/1 20:16
"""
import  wx,sys
import wx.richtext as rt

sys.path.append("..")

class FileEditor(wx.Panel):

    def __init__(self, parent, log,fileContent):
        self.log = log
        wx.Panel.__init__(self, parent, -1)

        bSizerMain = wx.BoxSizer(wx.VERTICAL)

        bSizerTop = wx.BoxSizer(wx.HORIZONTAL)

        self.buttonLoad = wx.Button(self, wx.ID_ANY, u"载入", wx.DefaultPosition, wx.DefaultSize, 0)
        bSizerTop.Add(self.buttonLoad, 0, wx.ALL, 5)

        self.m_textCtrl2 = wx.TextCtrl(self, wx.ID_ANY, wx.EmptyString, wx.DefaultPosition, wx.DefaultSize, 0)
        bSizerTop.Add(self.m_textCtrl2, 1, wx.ALL | wx.ALIGN_CENTER_VERTICAL, 5)

        self.buttonSave = wx.Button(self, wx.ID_ANY, u"保存", wx.DefaultPosition, wx.DefaultSize, 0)
        bSizerTop.Add(self.buttonSave, 0, wx.ALL, 5)

        bSizerMain.Add(bSizerTop, 0, wx.EXPAND, 5)

        self.textCtrlFileContent = wx.TextCtrl(self, wx.ID_ANY, wx.EmptyString, wx.DefaultPosition, wx.DefaultSize,
                                               wx.HSCROLL | wx.TE_MULTILINE | wx.TE_WORDWRAP)
        bSizerMain.Add(self.textCtrlFileContent, 1, wx.ALL | wx.EXPAND, 5)

        self.SetSizer(bSizerMain)

        self.textCtrlFileContent.SetValue(fileContent)
