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


class MainWindow(wx.Panel):
    def __init__(self, parent,main_app,log):
        self.main_app=main_app
        self.log = log
        wx.Panel.__init__(self, parent, -1)

        sizer = wx.BoxSizer(wx.HORIZONTAL)

        self.nb = wx.aui.AuiNotebook(self)

        win = ShellListCtrl.ShellList(self, log)

        self.nb.AddPage(win, 'Shell',True,wx.ArtProvider.GetBitmap(wx.ART_GO_HOME,client=wx.ART_FRAME_ICON))

        sizer.Add(self.nb, 5, wx.EXPAND)

        bSizer2 = wx.BoxSizer(wx.VERTICAL)

        sbSizer1 = wx.StaticBoxSizer(wx.StaticBox(self, wx.ID_ANY, u"内网通道列表"), wx.VERTICAL)

        self.listCtrlTunnel = wx.ListCtrl(sbSizer1.GetStaticBox(), wx.ID_ANY, wx.DefaultPosition, wx.DefaultSize,
                                          wx.LC_ICON)
        sbSizer1.Add(self.listCtrlTunnel, 1, wx.ALL | wx.EXPAND, 5)

        bSizer2.Add(sbSizer1, 1, wx.EXPAND|wx.ALL, 5)

        sbSizer2 = wx.StaticBoxSizer(wx.StaticBox(self, wx.ID_ANY, u"请求响应状态："), wx.VERTICAL)

        self.textCtrlResponseStatus = wx.TextCtrl(sbSizer2.GetStaticBox(), wx.ID_ANY, wx.EmptyString,
                                                  wx.DefaultPosition, wx.DefaultSize, wx.TE_MULTILINE|wx.TE_READONLY)
        sbSizer2.Add(self.textCtrlResponseStatus, 1, wx.ALL | wx.EXPAND, 5)

        bSizer2.Add(sbSizer2, 1, wx.EXPAND|wx.ALL, 5)

        sizer.Add(bSizer2, 1, wx.EXPAND, 5)

        self.SetSizer(sizer)

        wx.CallAfter(self.nb.SendSizeEvent)

    def SetRequestStatusText(self,text):
        self.textCtrlResponseStatus.SetValue(text)

    def OpenFileTree(self, shellEntity):
        win = FileManagerCtrl.FileManager(self, self.log, shellEntity)
        index = self.nb.AddPage(win, shellEntity.shell_host,True,wx.ArtProvider.GetBitmap(wx.ART_FOLDER,client=wx.ART_FRAME_ICON,size=(20,20)))

    def OpenFileEditor(self, fileName, fileContent):
        win = FileEditorCtrl.FileEditor(self, self.log, fileContent)
        index = self.nb.AddPage(win, fileName,True,wx.ArtProvider.GetBitmap(wx.ART_NORMAL_FILE,client=wx.ART_FRAME_ICON,size=(20,20)))

    def OpenVirtualConsole(self,shellEntity):
        win = VirtualConsoleCtrl.VirtualConsole(self, shellEntity,self.log)
        index = self.nb.AddPage(win, shellEntity.shell_host,True,wx.ArtProvider.GetBitmap(wx.ART_EXECUTABLE_FILE,client=wx.ART_FRAME_ICON))

    def OpenDatabaseManager(self,shellEntity):
        win = DatabaseManagerCtrl.DatabaseManager(self, shellEntity,self.log)
        index = self.nb.AddPage(win, shellEntity.shell_host,True,wx.ArtProvider.GetBitmap(wx.ART_HELP_BOOK,client=wx.ART_FRAME_ICON))