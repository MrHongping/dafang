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

sys.path.append("..")

import ShellListCtrl
import FileManagerCtrl
import FileEditorCtrl
import VirtualConsoleCtrl
import DatabaseManagerCtrl

from utils import config

ID_HTTP_STATUS_WINDOW = wx.NewId()
ID_TUNNEL_STATUS_WINDOW = wx.NewId()


class MainWindow(wx.Frame):
    def __init__(self, parent,log,title):

        wx.Frame.__init__(self, None,title=title)

        self.log = log

        self.Maximize(True)

        self._mgr = aui.AuiManager()

        self._mgr.SetManagedWindow(self)

        self.notebookCtrl = aui.AuiNotebook(self)

        self.shellPage = ShellListCtrl.ShellList(self, self.log)
        self.notebookCtrl.AddPage(self.shellPage, 'Shell', True,
                                  wx.ArtProvider.GetBitmap(wx.ART_GO_HOME, client=wx.ART_FRAME_ICON))

        self._mgr.AddPane(self.notebookCtrl, aui.AuiPaneInfo().Name("mainWindow").
                          CenterPane())

        self.treeCtrlHttpStatus = wx.TreeCtrl(self, id=wx.ID_ANY, pos=wx.DefaultPosition, size=(-1, 150),
                                          style=wx.TR_DEFAULT_STYLE | wx.TR_HIDE_ROOT | wx.TR_NO_LINES | wx.TR_HAS_BUTTONS | wx.TR_HAS_VARIABLE_ROW_HEIGHT)
        self.treeCtrlHttpStatusRoot = self.treeCtrlHttpStatus.AddRoot('hideRoot')

        self._mgr.AddPane(self.treeCtrlHttpStatus, aui.AuiPaneInfo().
                          Name("HttpStatusWindow").Caption("请求状态信息").
                          Bottom().Layer(1).Position(1).CloseButton(True).MaximizeButton(True).MinimizeButton(True))

        self.treeCtrlTunnelStatus = wx.TreeCtrl(self, id=wx.ID_ANY, pos=wx.DefaultPosition, size=(300, -1),
                                              style=wx.TR_DEFAULT_STYLE | wx.TR_HIDE_ROOT | wx.TR_NO_LINES | wx.TR_HAS_BUTTONS | wx.TR_HAS_VARIABLE_ROW_HEIGHT)
        self.treeCtrlTunnelStatusRoot = self.treeCtrlTunnelStatus.AddRoot('hideRoot')

        self._mgr.AddPane(self.treeCtrlTunnelStatus, aui.AuiPaneInfo().
                          Name("TunnelStatusWindow").Caption("隧道状态信息").
                          Right().Layer(1).Position(1).CloseButton(True).MaximizeButton(True).MinimizeButton(True).Hide())

        self._mgr.Update()

        self.notebookCtrl.Bind(wx.aui.EVT_AUINOTEBOOK_TAB_RIGHT_UP,self.OnTabRightClick)

        self.Bind(wx.EVT_CLOSE, self.OnClose)

        self.taskStatusList={}
        self.sessionBelongList = {}

        self.OnInitMenu()

    def OnInitMenu(self):

        self.tabManageMenu = wx.Menu()
        for text in config.TAB_MANAGE_MENU.split():
            item = self.tabManageMenu.Append(-1, text)
            self.notebookCtrl.Bind(wx.EVT_MENU, self.OnTabManageMenuItemSelected, item)

        self.menubar = wx.MenuBar()

        self.shellTabManageMenu = wx.Menu()
        for text in config.TAB_MANAGE_MENU.split():
            item = self.shellTabManageMenu.Append(-1, text)
            self.Bind(wx.EVT_MENU, self.OnTabManageMenuItemSelected, item)
        self.menubar.Append(self.shellTabManageMenu, '&标签页')

        self.windowMenu = wx.Menu()

        self.windowMenu.AppendCheckItem(ID_HTTP_STATUS_WINDOW, 'Http请求状态窗体')
        self.windowMenu.AppendCheckItem(ID_TUNNEL_STATUS_WINDOW, '内网隧道状态窗体')

        self.windowMenu.Check(ID_HTTP_STATUS_WINDOW, True)

        self.Bind(wx.EVT_MENU, self.OnWindowMenu, id=ID_HTTP_STATUS_WINDOW)
        self.Bind(wx.EVT_MENU, self.OnWindowMenu, id=ID_TUNNEL_STATUS_WINDOW)

        self.menubar.Append(self.windowMenu, '&窗体')

        self.aboutMenu = wx.Menu()

        item=self.aboutMenu.Append(-1, '关于大方')

        self.Bind(wx.EVT_MENU, self.OnAboutMenu, item)

        self.menubar.Append(self.aboutMenu, '&关于')

        self.SetMenuBar(self.menubar)

    def OnTabRightClick(self,event):
        self.notebookCtrl.PopupMenu(self.tabManageMenu)

    def OnAboutMenu(self,event):
        # 如果要更改代码请保留此处，嗯，这是约定
        wx.MessageBox('献给小落落，也许有一天你会用到！')

    def AddNewShellPage(self):
        self.shellPage = ShellListCtrl.ShellList(self, self.log)
        self.notebookCtrl.AddPage(self.shellPage, 'Shell', True,
                                  wx.ArtProvider.GetBitmap(wx.ART_GO_HOME, client=wx.ART_FRAME_ICON))

    def OnTabManageMenuItemSelected(self, event):

        item = self.tabManageMenu.FindItemById(event.GetId())
        
        if not item:
            item=self.shellTabManageMenu.FindItemById(event.GetId())

        text = item.GetText()


        if text == u'打开新的Shell选项卡':
            self.AddNewShellPage()

        if text == u'关闭当前选项卡':
            self.notebookCtrl.DeletePage(self.notebookCtrl.GetSelection())

        if text == u'关闭其他选项卡':
            pageCount = self.notebookCtrl.GetPageCount()
            for page in range(self.notebookCtrl.GetSelection() + 1, pageCount):
                self.notebookCtrl.DeletePage(self.notebookCtrl.GetSelection() + 1)

            for page in range(0,self.notebookCtrl.GetSelection()):
                self.notebookCtrl.DeletePage(0)

        if text == u'关闭右侧所有选项卡':
            pageCount = self.notebookCtrl.GetPageCount()
            for page in range(self.notebookCtrl.GetSelection()+1, pageCount):
                self.notebookCtrl.DeletePage(self.notebookCtrl.GetSelection()+1)

        if text == u'关闭左侧所有选项卡':
            for page in range(0,self.notebookCtrl.GetSelection()):
                self.notebookCtrl.DeletePage(0)

        if text == u'关闭所有选项卡':
            pageCount = self.notebookCtrl.GetPageCount()
            for page in range(0, pageCount):
                self.notebookCtrl.DeletePage(0)

    def OnWindowMenu(self,event):
        eid = event.GetId()
        if eid==ID_HTTP_STATUS_WINDOW:
            if self.windowMenu.IsChecked(ID_HTTP_STATUS_WINDOW):
                self._mgr.GetPane("HttpStatusWindow").Show().Bottom().Layer(1).Position(1)
            else:
                self._mgr.GetPane("HttpStatusWindow").Hide()
        if eid==ID_TUNNEL_STATUS_WINDOW:
            if self.windowMenu.IsChecked(ID_TUNNEL_STATUS_WINDOW):
                self._mgr.GetPane("TunnelStatusWindow").Show().Right().Layer(1).Position(1)
            else:
                self._mgr.GetPane("TunnelStatusWindow").Hide()
        self._mgr.Update()

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

    def _GetHttpStatusParam(self,taskEntity):

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
            statusString='请求未生效,远程脚本错误（{0}）'.format(taskEntity.taskResult)
            itemColor=wx.RED
        elif taskEntity.taskStatus==config.ERROR_RESPONSE_WITH_SYMBOL:
            statusString='请求成功，但有错误发生（{0}）'.format(taskEntity.taskResult)
            itemColor=wx.RED
        elif taskEntity.taskStatus==config.FILE_DOWNLOADING:
            statusString='下载中'+taskEntity.taskResult
            itemColor=wx.BLACK
        elif taskEntity.taskStatus==config.FILE_DOWNLOAD_SUCCESS:
            statusString='下载成功（{0}）'.format(taskEntity.taskResult)
            itemColor=wx.GREEN
        elif taskEntity.taskStatus==config.FILE_DOWNLOAD_ERROR:
            statusString='下载出错（{0}）'.format(taskEntity.taskResult)
            itemColor=wx.RED

        return statusAction,statusString,itemColor

    def SetHttpStatus(self,taskEntity):

        statusAction,statusString, itemColor = self._GetHttpStatusParam(taskEntity)

        if taskEntity.taskID not in self.taskStatusList:

            taskItem=self.treeCtrlHttpStatus.AppendItem(self.treeCtrlHttpStatusRoot,taskEntity.taskAddress+' '+statusAction)
            statusItem=self.treeCtrlHttpStatus.AppendItem(taskItem,'状态:'+statusString)
            self.treeCtrlHttpStatus.SetItemTextColour(statusItem,itemColor)
            self.treeCtrlHttpStatus.Expand(taskItem)
            self.taskStatusList[taskEntity.taskID]=taskItem
            self.treeCtrlHttpStatus.ScrollTo(statusItem)
        else:

            taskItem=self.taskStatusList[taskEntity.taskID]
            childItem,cookie=self.treeCtrlHttpStatus.GetFirstChild(taskItem)
            if childItem:
                self.treeCtrlHttpStatus.SetItemText(childItem,'状态:'+statusString)
                self.treeCtrlHttpStatus.SetItemTextColour(childItem, itemColor)

    def _GetTunnelStatusParam(self,sessionEntity):


        itemColor=wx.BLACK

        if sessionEntity.sessionStatus == config.SESSION_INFO_MESSAGE:
            itemColor=wx.GREEN
        elif sessionEntity.sessionStatus == config.SESSION_DEBUG_MESSAGE:
            itemColor=wx.GREEN
        elif sessionEntity.sessionStatus == config.SESSION_ERROR_MESSAGE:
            itemColor=wx.RED

        sessionMessage=sessionEntity.sessionMessage

        return sessionMessage,itemColor

    def SetTunnelStatus(self,sessionEntity):

        sessionMessage, itemColor = self._GetTunnelStatusParam(sessionEntity)

        print 'start'

        if sessionEntity.sessionBelong not in self.sessionBelongList:
            print 'start1'+sessionEntity.sessionBelong
            sessionItem=self.treeCtrlTunnelStatus.AppendItem(self.treeCtrlTunnelStatusRoot,sessionEntity.sessionBelong)
            self.treeCtrlHttpStatus.Expand(sessionItem)
            self.sessionBelongList[sessionEntity.sessionBelong]=sessionItem
            self.treeCtrlHttpStatus.ScrollTo(sessionItem)
            print 'end1'
        else:
            print 'start2'+sessionEntity.sessionBelong
            sessionItem=self.sessionBelongList[sessionEntity.sessionBelong]
            childItem=self.treeCtrlTunnelStatus.AppendItem(sessionItem,sessionMessage)
            self.treeCtrlHttpStatus.SetItemTextColour(childItem, itemColor)
            print 'end2'

        print 'end'

    def OnClose(self,event):
        self._mgr.UnInit()
        del self._mgr
        self.Destroy()