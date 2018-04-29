# -*- coding: UTF-8 -*-
import sys
import wx

sys.path.append("..")
from DialogUtils import *
from utils.entity import shell_entity
from utils import config
from utils.dbHelper import DatabaseHelper


class ShellList(wx.Panel):
    def __init__(self, parent, log):

        self.currentItem=-1
        self.log = log
        self.parent=parent
        
        wx.Panel.__init__(self, parent, -1)
        
        self.Bind(wx.EVT_SIZE, self.OnSize)

        self.shellListCtrl = wx.ListCtrl(self, -1, style =wx.LC_REPORT| wx.BORDER_SUNKEN)

        self.shellListCtrl.InsertColumn(0,u'Shell地址',format=wx.LIST_FORMAT_CENTER)
        self.shellListCtrl.InsertColumn(1,u"Shell密码",format=wx.LIST_FORMAT_CENTER,width=100)
        self.shellListCtrl.InsertColumn(2,u"脚本类型",format=wx.LIST_FORMAT_CENTER,width=100)
        self.shellListCtrl.InsertColumn(3,u"编码类型", format=wx.LIST_FORMAT_CENTER, width=100)
        self.shellListCtrl.InsertColumn(4,u"数据库配置", format=wx.LIST_FORMAT_CENTER, width=100)
        self.shellListCtrl.InsertColumn(5,u"备注", format=wx.LIST_FORMAT_CENTER, width=200)
        self.shellListCtrl.InsertColumn(6,u"创建时间",format=wx.LIST_FORMAT_CENTER,width=200)

        #####事件绑定

        #for MSW
        self.shellListCtrl.Bind(wx.EVT_COMMAND_RIGHT_CLICK, self.OnRightClick)
        # for wxGTK
        self.shellListCtrl.Bind(wx.EVT_RIGHT_UP, self.OnRightClick)

        self.shellListCtrl.Bind(wx.EVT_LEFT_DCLICK, self.OnDoubleClick)

        self.Bind(wx.EVT_LIST_ITEM_SELECTED, self.OnItemSelected, self.shellListCtrl)
        self.Bind(wx.EVT_LIST_ITEM_DESELECTED, self.OnItemDeselected, self.shellListCtrl)
        #####

        self.shellManageMenu = wx.Menu()
        for text in config.SHELL_MANAGE_MENU.split():
            item = self.shellManageMenu.Append(-1, text)
            self.shellListCtrl.Bind(wx.EVT_MENU, self.OnShellManageMenuItemSelected, item)

        self.manageMenu = wx.Menu()
        for text in config.MANAGE_MENU.split():
            item = self.manageMenu.Append(-1, text)
            self.shellListCtrl.Bind(wx.EVT_MENU, self.OnManageMenuItemSelected, item)

        self.UpdateShellList()

    def UpdateShellList(self):
        self.shellEntityList = DatabaseHelper.getShellEntityList()
        self.shellListCtrl.DeleteAllItems()
        for shellEntity in self.shellEntityList:
            index = self.shellListCtrl.InsertItem(self.shellListCtrl.GetItemCount(), shellEntity.shell_address)
            self.shellListCtrl.SetItem(index, 1, shellEntity.shell_password)
            self.shellListCtrl.SetItem(index, 2, shellEntity.shell_script_type)
            self.shellListCtrl.SetItem(index, 3, shellEntity.shell_encode_type)
            self.shellListCtrl.SetItem(index, 4, shellEntity.database_info)
            self.shellListCtrl.SetItem(index, 5, shellEntity.shell_remark)
            self.shellListCtrl.SetItem(index, 6, shellEntity.createTime)
            self.shellListCtrl.SetItemData(index,shellEntity.shell_id)
        self.shellListCtrl.SetColumnWidth(0, wx.LIST_AUTOSIZE)

    def ShowShellManageDialog(self,shellEntity=None):
        dlg = ShellManageDialog(self, -1, "Shell设置", size=(500, -1), style=wx.DEFAULT_DIALOG_STYLE,shellEntity=shellEntity)
        dlg.CenterOnScreen()
        code=dlg.ShowModal()
        if code:
            self.UpdateShellList()

    def ShowHttpSettingDialog(self,shellEntity=None):
        dlg = HttpSettingDialog(self, "Http设置",shellEntity)
        dlg.CenterOnScreen()
        code=dlg.ShowModal()

    def ShowTunnelSettingDialog(self,shellEntity=None):
        dlg = TunnelSettingDialog(self, "Tunnel设置",shellEntity)
        dlg.CenterOnScreen()
        code=dlg.ShowModal()

    def OnManageMenuItemSelected(self, event):
        item = self.manageMenu.FindItemById(event.GetId())
        text = item.GetText()
        if text == u'添加':
            self.ShowShellManageDialog()
        else:
            wx.MessageBox('For小落落，也许有一天你能用的到！\r\n\r\n——laochao爸爸')

    def OnShellManageMenuItemSelected(self, event):
        item = self.shellManageMenu.FindItemById(event.GetId())
        text = item.GetText()

        if text == u'添加':
            self.ShowShellManageDialog()

        if text==u'编辑':
            self.ShowShellManageDialog(self.shellEntityList[self.currentItem])

        if text ==u'删除':
            DatabaseHelper.deleteShellEntityByID(self.shellListCtrl.GetItemData(self.currentItem))
            self.UpdateShellList()

        if text==u'虚拟终端':
            self.parent.OpenVirtualConsole(self.shellEntityList[self.currentItem])

        if text==u'数据库管理':
            self.parent.OpenDatabaseManager(self.shellEntityList[self.currentItem])

        if text==u'文件管理':
            shellEntity = self.shellEntityList[self.currentItem]
            self.parent.OpenFileTree(shellEntity)

        if text==u'HTTP参数':
            self.ShowHttpSettingDialog(self.shellEntityList[self.currentItem])

        if text==u'内网通道':
            self.ShowTunnelSettingDialog(self.shellEntityList[self.currentItem])

    #选中条目
    def OnItemSelected(self, event):
        self.currentItem = event.Index

    #条目失去选中
    def OnItemDeselected(self,event):
        self.currentItem=-1

    #双击条目
    def OnDoubleClick(self, evt):
        shellEntity=self.shellEntityList[self.currentItem]
        self.parent.OpenFileTree(shellEntity)

    #右键条目或空白区域
    def OnRightClick(self, evt):
        if self.currentItem!=-1:
            self.shellListCtrl.PopupMenu(self.shellManageMenu)
        else:
            self.shellListCtrl.PopupMenu(self.manageMenu)

    def OnSize(self, evt):
        self.shellListCtrl.SetSize(self.GetSize())
