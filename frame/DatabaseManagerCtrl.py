# coding=utf-8

"""
@version: 1.0
@author: chaowei
@file: DatabaseManager.py
@time: 2018/4/28 16:01
"""
import wx,sys

sys.path.append("..")

from utils import config
from utils.shell import ShellTools

class DatabaseManager(wx.Panel):

    def __init__(self,parent,shellEntity,log):
        wx.Panel.__init__(self, parent, -1, wx.DefaultPosition, wx.DefaultSize)

        self.log=log
        self.shellEntity=shellEntity

        self.SetSizeHintsSz(wx.DefaultSize, wx.DefaultSize)

        bSizer1 = wx.BoxSizer(wx.VERTICAL)

        bSizer2 = wx.BoxSizer(wx.HORIZONTAL)

        self.buttonSetting = wx.Button(self, wx.ID_ANY, u"配置", wx.DefaultPosition, wx.DefaultSize, 0)
        bSizer2.Add(self.buttonSetting, 0, wx.ALL, 5)

        m_comboBox1Choices = []
        self.m_comboBox1 = wx.ComboBox(self, wx.ID_ANY, u"Combo!", wx.DefaultPosition, wx.DefaultSize,
                                       m_comboBox1Choices, 0)
        bSizer2.Add(self.m_comboBox1, 1, wx.ALL | wx.ALIGN_CENTER_VERTICAL, 5)

        self.buttonQuery = wx.Button(self, wx.ID_ANY, u"查询", wx.DefaultPosition, wx.DefaultSize, 0)
        bSizer2.Add(self.buttonQuery, 0, wx.ALL, 5)

        bSizer1.Add(bSizer2, 0, wx.EXPAND, 5)

        bSizer3 = wx.BoxSizer(wx.HORIZONTAL)

        self.treeCtrlDatabaseShow = wx.TreeCtrl(self, wx.ID_ANY, wx.DefaultPosition, wx.DefaultSize,
                                                wx.TR_DEFAULT_STYLE)
        bSizer3.Add(self.treeCtrlDatabaseShow, 1, wx.ALL | wx.EXPAND, 5)

        self.listCtrlTableShow = wx.ListCtrl(self, wx.ID_ANY, wx.DefaultPosition, wx.DefaultSize, wx.LC_ICON)
        bSizer3.Add(self.listCtrlTableShow, 3, wx.ALL | wx.EXPAND, 5)

        bSizer1.Add(bSizer3, 1, wx.EXPAND, 5)

        self.SetSizer(bSizer1)
        self.Layout()

        self.Centre(wx.BOTH)

        self.OnInit()

    def OnInit(self):
        connectInfo='''com.mysql.jdbc.Driver
jdbc:mysql://localhost/test?user=root&password=pa55w0rd'''
        self.shellTools=ShellTools.getShellTools(self.shellEntity)
        code,queryResult=self.shellTools.getDatabases(connectInfo)
        print queryResult
        pass

    def __del__(self):
        pass
