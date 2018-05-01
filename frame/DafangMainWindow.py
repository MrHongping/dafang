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

        self.nb.AddPage(win, 'Shell',True,wx.ArtProvider.GetBitmap(wx.ART_GO_HOME,size=(20,20)))

        sizer.Add(self.nb, 4, wx.EXPAND)

        self.SetSizer(sizer)

        wx.CallAfter(self.nb.SendSizeEvent)

    def SetRequestStatusText(self,text):
        self.main_app.SetRequestStatusText(text)

    def SetHostSelectedStatusText(self,text):
        self.main_app.SetRequestStatusText(text)

    def SetTunnelStatusText(self,text):
        self.main_app.SetRequestStatusText(text)

    def OpenFileTree(self, shellEntity):
        win = FileManagerCtrl.FileManager(self, self.log, shellEntity)
        index = self.nb.AddPage(win, shellEntity.shell_host,True,wx.ArtProvider.GetBitmap(wx.ART_FOLDER,size=(20,20)))

    def OpenFileEditor(self, fileName, fileContent):
        win = FileEditorCtrl.FileEditor(self, self.log, fileContent)
        index = self.nb.AddPage(win, fileName,True,wx.ArtProvider.GetBitmap(wx.ART_NORMAL_FILE,size=(20,20)))

    def OpenVirtualConsole(self,shellEntity):
        win = VirtualConsoleCtrl.VirtualConsole(self, shellEntity,self.log)
        index = self.nb.AddPage(win, 'console',True,wx.ArtProvider.GetBitmap(wx.ART_EXECUTABLE_FILE,size=(20,20)))

    def OpenDatabaseManager(self,shellEntity):
        win = DatabaseManagerCtrl.DatabaseManager(self, shellEntity,self.log)
        index = self.nb.AddPage(win, shellEntity.shell_host,True,wx.ArtProvider.GetBitmap(wx.ART_HELP_BOOK,size=(20,20)))