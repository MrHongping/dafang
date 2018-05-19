# coding=utf-8

"""
@version: 1.0
@author: chaowei
@file: DafangMainWindow.py
@time: 2018/4/2 16:55
"""
import sys

import wx
import wx.aui

sys.path.append("..")

import ShellListCtrl
import FileManagerCtrl
import FileEditorCtrl
import VirtualConsoleCtrl
import DatabaseManagerCtrl

from utils import config


class MainWindow(wx.Panel):
    def __init__(self, parent,main_app,log):
        self.main_app=main_app
        self.log = log
        wx.Panel.__init__(self, parent, -1)

        mainSizer = wx.BoxSizer(wx.HORIZONTAL)

        bSizerLeft = wx.BoxSizer(wx.VERTICAL)

        self.notebookCtrl = wx.aui.AuiNotebook(self)

        win = ShellListCtrl.ShellList(self, log)

        self.notebookCtrl.AddPage(win, 'Shell',True,wx.ArtProvider.GetBitmap(wx.ART_GO_HOME,client=wx.ART_FRAME_ICON))

        bSizerLeft.Add(self.notebookCtrl, 1, wx.EXPAND)

        mainSizer.Add(bSizerLeft, 5, wx.EXPAND)

        bSizerRight = wx.BoxSizer(wx.VERTICAL)

        sbSizerTunnel = wx.StaticBoxSizer(wx.StaticBox(self, wx.ID_ANY, u"内网通道列表"), wx.VERTICAL)

        self.listCtrlTunnel = wx.ListCtrl(sbSizerTunnel.GetStaticBox(), wx.ID_ANY, wx.DefaultPosition, wx.DefaultSize,
                                          wx.LC_REPORT)
        sbSizerTunnel.Add(self.listCtrlTunnel, 1, wx.ALL | wx.EXPAND, 5)

        bSizerRight.Add(sbSizerTunnel, 1, wx.EXPAND|wx.ALL, 5)

        sbSizerStatus = wx.StaticBoxSizer(wx.StaticBox(self, wx.ID_ANY, u"请求响应状态："), wx.VERTICAL)

        self.textCtrlResponseStatus = wx.TextCtrl(sbSizerStatus.GetStaticBox(), wx.ID_ANY, wx.EmptyString,
                                                  wx.DefaultPosition, wx.DefaultSize, wx.TE_MULTILINE|wx.TE_READONLY)
        sbSizerStatus.Add(self.textCtrlResponseStatus, 1, wx.ALL | wx.EXPAND, 5)

        bSizerRight.Add(sbSizerStatus, 1, wx.EXPAND|wx.ALL, 5)

        mainSizer.Add(bSizerRight, 1, wx.EXPAND, 5)

        self.SetSizer(mainSizer)
        self.Layout()

        self.Centre(wx.BOTH)

        self.tabManageMenu = wx.Menu()
        for text in config.TAB_MANAGE_MENU.split():
            item = self.tabManageMenu.Append(-1, text)
            self.notebookCtrl.Bind(wx.EVT_MENU, self.OnTabManageMenuItemSelected, item)

        self.notebookCtrl.Bind(wx.aui.EVT_AUINOTEBOOK_TAB_RIGHT_UP,self.OnTabRightClick)

        self.Ontest()

    def OnTabRightClick(self,event):
        self.selectTab=event.GetSelection()
        self.notebookCtrl.PopupMenu(self.tabManageMenu)

    def OnTabManageMenuItemSelected(self, event):

        item = self.tabManageMenu.FindItemById(event.GetId())

        text = item.GetText()

        if text == u'关闭当前选项卡':
            self.notebookCtrl.DeletePage(self.selectTab)

        if text == u'关闭其他选项卡':
            print self.selectTab
            pageCount = self.notebookCtrl.GetPageCount()
            for page in range(self.selectTab + 1, pageCount):
                self.notebookCtrl.DeletePage(self.selectTab + 1)

            for page in range(0,self.selectTab):
                self.notebookCtrl.DeletePage(0)

        if text == u'关闭右侧所有选项卡':
            pageCount = self.notebookCtrl.GetPageCount()
            for page in range(self.selectTab+1, pageCount):
                print page
                self.notebookCtrl.DeletePage(self.selectTab+1)

        if text == u'关闭左侧所有选项卡':
            for page in range(0,self.selectTab):
                self.notebookCtrl.DeletePage(0)

        if text == u'关闭所有选项卡':
            pageCount = self.notebookCtrl.GetPageCount()
            for page in range(0, pageCount):
                self.notebookCtrl.DeletePage(0)

    def Ontest(self):
        # self.listCtrlTunnel

        self.listCtrlTunnel.InsertColumn(0, u'侦听地址')
        self.listCtrlTunnel.InsertColumn(1, u"流量")

    def SetRequestStatusText(self,text):
        self.textCtrlResponseStatus.SetValue(text)

    def OpenFileTree(self, shellEntity):
        win = FileManagerCtrl.FileManager(self, self.log, shellEntity)
        index = self.notebookCtrl.AddPage(win, shellEntity.shell_host,True,wx.ArtProvider.GetBitmap(wx.ART_FOLDER,client=wx.ART_FRAME_ICON,size=(20,20)))
        win.OnInit()

    def OpenFileEditor(self, fileName, filePath,shellEntity):
        win = FileEditorCtrl.FileEditor(self, shellEntity,self.log, filePath)
        index = self.notebookCtrl.AddPage(win, fileName,True,wx.ArtProvider.GetBitmap(wx.ART_NORMAL_FILE,client=wx.ART_FRAME_ICON,size=(20,20)))
        win.OnInit()

    def OpenVirtualConsole(self,shellEntity):
        win = VirtualConsoleCtrl.VirtualConsole(self, shellEntity,self.log)
        index = self.notebookCtrl.AddPage(win, shellEntity.shell_host,True,wx.ArtProvider.GetBitmap(wx.ART_EXECUTABLE_FILE,client=wx.ART_FRAME_ICON))

    def OpenDatabaseManager(self,shellEntity):
        win = DatabaseManagerCtrl.DatabaseManager(self, shellEntity,self.log)
        index = self.notebookCtrl.AddPage(win, shellEntity.shell_host,True,wx.ArtProvider.GetBitmap(wx.ART_HELP_BOOK,client=wx.ART_FRAME_ICON))
        win.OnInit()