# coding=utf-8

"""
@version: 1.0
@author: chaowei
@file: DatabaseManager.py
@time: 2018/4/28 16:01
"""
import wx,sys

sys.path.append("..")

from DialogUtils import DatabaseSettingDialog
from utils.shell import ShellTools

class DatabaseManager(wx.Panel):

    def __init__(self,parent,shellEntity,log):
        wx.Panel.__init__(self, parent, -1, wx.DefaultPosition, wx.DefaultSize)
        self.parent=parent
        self.log=log
        self.shellEntity=shellEntity

        self.SetSizeHints(wx.DefaultSize, wx.DefaultSize)

        bSizer1 = wx.BoxSizer(wx.VERTICAL)

        bSizer2 = wx.BoxSizer(wx.HORIZONTAL)

        self.buttonSetting = wx.Button(self, wx.ID_ANY, u"配置", wx.DefaultPosition, wx.DefaultSize, 0)
        bSizer2.Add(self.buttonSetting, 0, wx.ALL, 5)

        m_comboBox1Choices = []
        self.comboBoxSqlQueryString = wx.ComboBox(self, wx.ID_ANY, wx.EmptyString, wx.DefaultPosition, wx.DefaultSize,
                                       m_comboBox1Choices, 0)
        bSizer2.Add(self.comboBoxSqlQueryString, 1, wx.ALL | wx.ALIGN_CENTER_VERTICAL, 5)

        self.buttonQuery = wx.Button(self, wx.ID_ANY, u"查询", wx.DefaultPosition, wx.DefaultSize, 0)
        bSizer2.Add(self.buttonQuery, 0, wx.ALL, 5)

        bSizer1.Add(bSizer2, 0, wx.EXPAND, 5)

        bSizer3 = wx.BoxSizer(wx.HORIZONTAL)

        self.treeCtrlDatabaseShow = wx.TreeCtrl(self, wx.ID_ANY, wx.DefaultPosition, wx.DefaultSize,
                                                wx.TR_HIDE_ROOT)
        bSizer3.Add(self.treeCtrlDatabaseShow, 1, wx.ALL | wx.EXPAND, 5)

        self.listCtrlTableShow = wx.ListCtrl(self, wx.ID_ANY, wx.DefaultPosition, wx.DefaultSize, wx.LC_ICON)
        bSizer3.Add(self.listCtrlTableShow, 3, wx.ALL | wx.EXPAND, 5)

        bSizer1.Add(bSizer3, 1, wx.EXPAND, 5)

        self.SetSizer(bSizer1)
        self.Layout()

        self.Centre(wx.BOTH)

        isz = (16, 16)
        imageList = wx.ImageList(isz[0], isz[1])
        self.tableImg = imageList.Add(wx.ArtProvider.GetBitmap(wx.ART_REPORT_VIEW, wx.ART_OTHER, isz))
        self.databaseImg = imageList.Add(wx.ArtProvider.GetBitmap(wx.ART_HELP_BOOK, wx.ART_OTHER, isz))

        self.treeCtrlDatabaseShow.SetImageList(imageList)
        self.imageList=imageList

        self.OnInit()

    def OnInit(self):
        if self.shellEntity.database_info:
            connectInfo=self.shellEntity.database_info.split('<X>')[1].replace('</X>','').strip()
            self.shellTools=ShellTools.getShellTools(self.shellEntity)
            code,queryResult=self.shellTools.getDatabases(connectInfo)
            if code:
                self.root = self.treeCtrlDatabaseShow.AddRoot('root')
                databaseNameList=queryResult.split('\t')
                for databaseName in databaseNameList:
                    if databaseName:
                        databaseItem=self.treeCtrlDatabaseShow.AppendItem(self.root, databaseName)
                        self.treeCtrlDatabaseShow.SetItemImage(databaseItem,self.databaseImg, wx.TreeItemIcon_Normal)
                self.treeCtrlDatabaseShow.ExpandAll()
            else:
                wx.MessageBox(queryResult)
                self.comboBoxSqlQueryString.SetValue('访问出错')
        else:
            self.parent.SetRequestStatusText('Error:数据配置信息为空')

    def __del__(self):
        pass
