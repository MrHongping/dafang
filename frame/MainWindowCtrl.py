# coding=utf-8

"""
@version: 1.0
@author: chaowei
@file: DafangMainWindow.py
@time: 2018/4/2 16:55
"""
import sys

import wx
import wx.aui as aui

import wx.lib.agw.customtreectrl as CT

sys.path.append("..")

import ShellListCtrl
import FileManagerCtrl
import FileEditorCtrl
import VirtualConsoleCtrl
import DatabaseManagerCtrl

from utils import config


class MainWindow(wx.Frame):
    def __init__(self, parent,log,title):

        wx.Frame.__init__(self, None,title=title)

        self.log = log

        self.Maximize(True)

        self._mgr = aui.AuiManager()

        self._mgr.SetManagedWindow(self)

        self.notebookCtrl = aui.AuiNotebook(self)

        self.shellPage = ShellListCtrl.ShellList(self, log)

        self.notebookCtrl.AddPage(self.shellPage, 'Shell',True,wx.ArtProvider.GetBitmap(wx.ART_GO_HOME,client=wx.ART_FRAME_ICON))

        self._mgr.AddPane(self.notebookCtrl, aui.AuiPaneInfo().Name("mainWindow").
                          CenterPane())

        self.treeCtrlStatus = wx.TreeCtrl(self, id=wx.ID_ANY, pos=wx.DefaultPosition, size=(100, 150),
                                                style=wx.TR_DEFAULT_STYLE|wx.TR_HIDE_ROOT | wx.TR_NO_LINES|wx.TR_HAS_BUTTONS|wx.TR_HAS_VARIABLE_ROW_HEIGHT)
        self.treeCtrlStatusRoot=self.treeCtrlStatus.AddRoot('hideRoot')

        self._mgr.AddPane(self.treeCtrlStatus, aui.AuiPaneInfo().
                          Name("statusWindow").Caption("状态信息").
                          Bottom().Layer(1).Position(1).CloseButton(True).MaximizeButton(True))

        self._mgr.Update()

        self.tabManageMenu = wx.Menu()
        for text in config.TAB_MANAGE_MENU.split():
            item = self.tabManageMenu.Append(-1, text)
            self.notebookCtrl.Bind(wx.EVT_MENU, self.OnTabManageMenuItemSelected, item)

        self.notebookCtrl.Bind(wx.aui.EVT_AUINOTEBOOK_TAB_RIGHT_UP,self.OnTabRightClick)
        self.Bind(wx.EVT_CLOSE, self.OnClose)

        self.taskStatusList={}

    def OnTabRightClick(self,event):
        self.selectTab=event.GetSelection()
        self.notebookCtrl.PopupMenu(self.tabManageMenu)

    def OnTabManageMenuItemSelected(self, event):

        item = self.tabManageMenu.FindItemById(event.GetId())

        text = item.GetText()

        if text == u'关闭当前选项卡':
            self.notebookCtrl.DeletePage(self.selectTab)

        if text == u'关闭其他选项卡':
            pageCount = self.notebookCtrl.GetPageCount()
            for page in range(self.selectTab + 1, pageCount):
                self.notebookCtrl.DeletePage(self.selectTab + 1)

            for page in range(0,self.selectTab):
                self.notebookCtrl.DeletePage(0)

        if text == u'关闭右侧所有选项卡':
            pageCount = self.notebookCtrl.GetPageCount()
            for page in range(self.selectTab+1, pageCount):
                self.notebookCtrl.DeletePage(self.selectTab+1)

        if text == u'关闭左侧所有选项卡':
            for page in range(0,self.selectTab):
                self.notebookCtrl.DeletePage(0)

        if text == u'关闭所有选项卡':
            pageCount = self.notebookCtrl.GetPageCount()
            for page in range(0, pageCount):
                self.notebookCtrl.DeletePage(0)

    def OpenFileTree(self, shellEntity):
        fileTreePage = FileManagerCtrl.FileManager(self, self.log, shellEntity)
        self.notebookCtrl.AddPage(fileTreePage, shellEntity.shell_host,True,wx.ArtProvider.GetBitmap(wx.ART_FOLDER,client=wx.ART_FRAME_ICON,size=(20,20)))
        pageIndex=self.notebookCtrl.GetSelection()
        self.notebookCtrl.SetPageToolTip(pageIndex,shellEntity.shell_address)
        fileTreePage.OnInit()

    def OpenFileEditor(self, fileName, filePath,shellEntity):
        fileEditorPage = FileEditorCtrl.FileEditor(self, shellEntity,self.log, filePath)
        self.notebookCtrl.AddPage(fileEditorPage, fileName,True,wx.ArtProvider.GetBitmap(wx.ART_NORMAL_FILE,client=wx.ART_FRAME_ICON,size=(20,20)))
        pageIndex=self.notebookCtrl.GetSelection()
        self.notebookCtrl.SetPageToolTip(pageIndex, shellEntity.shell_address)
        fileEditorPage.OnInit()

    def OpenVirtualConsole(self,shellEntity):
        virtualConsolePage = VirtualConsoleCtrl.VirtualConsole(self, shellEntity,self.log)
        self.notebookCtrl.AddPage(virtualConsolePage, shellEntity.shell_host,True,wx.ArtProvider.GetBitmap(wx.ART_EXECUTABLE_FILE,client=wx.ART_FRAME_ICON))
        pageIndex=self.notebookCtrl.GetSelection()
        self.notebookCtrl.SetPageToolTip(pageIndex, shellEntity.shell_address)
        virtualConsolePage.OnInit()

    def OpenDatabaseManager(self,shellEntity):
        databaseManagerPage = DatabaseManagerCtrl.DatabaseManager(self, shellEntity,self.log)
        self.notebookCtrl.AddPage(databaseManagerPage, shellEntity.shell_host,True,wx.ArtProvider.GetBitmap(wx.ART_HELP_BOOK,client=wx.ART_FRAME_ICON))
        pageIndex=self.notebookCtrl.GetSelection()
        self.notebookCtrl.SetPageToolTip(pageIndex, shellEntity.shell_address)
        databaseManagerPage.OnInit()

    def __GetStatusParam(self,taskEntity):

        statusAction=''
        if taskEntity.taskType==config.TASK_GET_START:
            statusAction='初始化请求'
        elif taskEntity.taskType==config.TASK_GET_DIRECTORY_CONTENT:
            statusAction='目录列表请求（{0}）'.format(taskEntity.taskContent)
        elif taskEntity.taskType==config.TASK_GET_FILE_CONTENT:
            statusAction='文件内容请求（{0}）'.format(taskEntity.taskContent)
        elif taskEntity.taskType==config.TASK_CREATE_FILE:
            statusAction='创建文件请求（{0}）'.format(taskEntity.taskContent)
        elif taskEntity.taskType==config.TASK_UPLOAD_FILE:
            statusAction='上传文件请求（{0}）'.format(taskEntity.taskContent)
        elif taskEntity.taskType==config.TASK_DOWNLOAD_FILE:
            statusAction='下载文件请求（{0}）'.format(taskEntity.taskContent)
        elif taskEntity.taskType==config.TASK_DELETE_FILE_OR_DIRECTORY:
            statusAction='删除文件请求（{0}）'.format(taskEntity.taskContent)
        elif taskEntity.taskType==config.TASK_EXCUTE_COMMAND:
            statusAction='执行命令请求（{0}）'.format(taskEntity.taskContent)
        elif taskEntity.taskType==config.TASK_GET_DATABASES:
            statusAction='获取数据库列表请求'
        elif taskEntity.taskType==config.TASK_GET_TABLES:
            statusAction='获取数据库表名请求（{0}）'.format(taskEntity.taskContent)
        elif taskEntity.taskType==config.TASK_GET_COLUMNS:
            statusAction='获取数据表列名请求（{0}）'.format(taskEntity.taskContent)
        elif taskEntity.taskType==config.TASK_EXCUTE_SQLQUERY:
            statusAction='执行SQL语句请求（{0}）'.format(taskEntity.taskContent)

        statusString=''
        itemColor=wx.BLACK

        if taskEntity.taskStatus == config.SUCCESS_RESPONSE:
            statusString = '请求成功'
            itemColor=wx.GREEN
        elif taskEntity.taskStatus == config.REQUESTS_SENDING:
            statusString='请求发送中'
        elif taskEntity.taskStatus==config.ERROR_DAFANG:
            statusString='请求发送失败'
            itemColor=wx.RED
        elif taskEntity.taskStatus==config.ERROR_RESPONSE_NO_SYMBOL:
            statusString='请求未生效,远程脚本错误\r\n'+taskEntity.taskResult
            itemColor=wx.RED
        elif taskEntity.taskStatus==config.ERROR_RESPONSE_WITH_SYMBOL:
            statusString='请求成功，但有错误发生\r\n'+taskEntity.taskResult
            itemColor=wx.RED
        elif taskEntity.taskStatus==config.FILE_DOWNLOADING:
            statusString='下载中'+taskEntity.taskResult
            itemColor=wx.BLACK
        elif taskEntity.taskStatus==config.FILE_DOWNLOAD_SUCCESS:
            statusString='下载成功（{0}）'.format(taskEntity.taskResult)
            itemColor=wx.GREEN
        elif taskEntity.taskStatus==config.FILE_DOWNLOAD_ERROR:
            statusString='下载出错\r\n'+taskEntity.taskResult
            itemColor=wx.RED

        return statusAction,statusString,itemColor

    def SetStatus(self,taskEntity):

        statusAction,statusString, itemColor = self.__GetStatusParam(taskEntity)

        if taskEntity.taskID not in self.taskStatusList:

            taskItem=self.treeCtrlStatus.AppendItem(self.treeCtrlStatusRoot,taskEntity.taskAddress+' '+statusAction)
            statusItem=self.treeCtrlStatus.AppendItem(taskItem,'状态:'+statusString)
            self.treeCtrlStatus.SetItemTextColour(statusItem,itemColor)
            self.treeCtrlStatus.Expand(taskItem)
            self.taskStatusList[taskEntity.taskID]=taskItem
            self.treeCtrlStatus.ScrollTo(statusItem)
        else:

            taskItem=self.taskStatusList[taskEntity.taskID]
            childItem,cookie=self.treeCtrlStatus.GetFirstChild(taskItem)
            if childItem:
                self.treeCtrlStatus.SetItemText(childItem,'状态:'+statusString)
                self.treeCtrlStatus.SetItemTextColour(childItem, itemColor)

    def OnClose(self,event):
        self._mgr.UnInit()
        del self._mgr
        self.Destroy()