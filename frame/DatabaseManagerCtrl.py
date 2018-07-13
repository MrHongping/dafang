# coding=utf-8

"""
@version: 1.0
@author: chaowei
@file: DatabaseManager.py
@time: 2018/4/28 16:01
"""
import wx,sys

sys.path.append("..")
from utils import config,commonsUtil,entity
from WorkThread import HttpRequestThread

class DatabaseManager(wx.Panel):

    def __init__(self,parent,shellEntity,log):
        wx.Panel.__init__(self, parent, -1, wx.DefaultPosition, wx.DefaultSize)

        self.parent=parent
        self.log=log
        self.shellEntity=shellEntity
        self.selectedItem=None

        isz = (16, 16)
        imageList = wx.ImageList(isz[0], isz[1])
        self.tableImg = imageList.Add(wx.ArtProvider.GetBitmap(wx.ART_REPORT_VIEW, wx.ART_OTHER, isz))
        self.databaseImg = imageList.Add(wx.ArtProvider.GetBitmap(wx.ART_HELP_BOOK, wx.ART_OTHER, isz))
        self.columnImg = imageList.Add(wx.ArtProvider.GetBitmap(wx.ART_TICK_MARK, wx.ART_OTHER, isz))

        self.imageList = imageList

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

        self.listCtrlTableShow = wx.ListCtrl(self, wx.ID_ANY, wx.DefaultPosition, wx.DefaultSize, wx.LC_REPORT)
        bSizer3.Add(self.listCtrlTableShow, 3, wx.ALL | wx.EXPAND, 5)

        bSizer1.Add(bSizer3, 1, wx.EXPAND, 5)

        self.SetSizer(bSizer1)
        self.Layout()

        self.Centre(wx.BOTH)

        self.treeCtrlDatabaseShow.SetImageList(imageList)

        self.treeCtrlDatabaseShow.Bind(wx.EVT_LEFT_DCLICK,self.OnTreeItemDoubleClick)
        self.treeCtrlDatabaseShow.Bind(wx.EVT_LEFT_DOWN,self.OnTreeItemClick)
        self.buttonQuery.Bind(wx.EVT_BUTTON,self.OnButtonQueryClick)

    def OnInit(self):
        if self.shellEntity.database_info:
            connectInfo=None
            xmlStr='<root>{0}</root>'.format(self.shellEntity.database_info.replace('&','&amp;'))
            if self.shellEntity.shell_script_type=='JSP':
                connectInfo=commonsUtil.get_dbInfo(xmlStr,'X')
            elif self.shellEntity.shell_script_type=='PHP':
                dbAddress=commonsUtil.get_dbInfo(xmlStr,'H')
                dbUser = commonsUtil.get_dbInfo(xmlStr, 'U')
                dbPassword = commonsUtil.get_dbInfo(xmlStr, 'P')
                connectInfo=entity.DBConnectEntity(dbAddress,dbUser,dbPassword)
            if connectInfo:
                HttpRequestThread(action=config.TASK_GET_DATABASES, connectInfo=connectInfo,
                                  shellEntity=self.shellEntity, callBack=self.Callback_getDatabases,
                                  statusCallback=self.parent.SetHttpStatus).start()

    def Callback_getDatabases(self,resultCode, resultContent):
        if resultCode:
            self.root = self.treeCtrlDatabaseShow.AddRoot('root')
            databaseNameList=resultContent.split('\t')
            for databaseName in databaseNameList:
                if databaseName:
                    databaseItem=self.treeCtrlDatabaseShow.AppendItem(self.root, databaseName,data='database')
                    self.treeCtrlDatabaseShow.SetItemImage(databaseItem,self.databaseImg, wx.TreeItemIcon_Normal)
            self.treeCtrlDatabaseShow.ExpandAll()

    def OnTreeItemDoubleClick(self,event):
        connectInfo = None
        xmlStr = '<root>{0}</root>'.format(self.shellEntity.database_info.replace('&','&amp;'))
        if self.shellEntity.shell_script_type == 'JSP':
            connectInfo = commonsUtil.get_dbInfo(xmlStr, 'X')
        elif self.shellEntity.shell_script_type == 'PHP':
            dbAddress = commonsUtil.get_dbInfo(xmlStr, 'H')
            dbUser = commonsUtil.get_dbInfo(xmlStr, 'U')
            dbPassword = commonsUtil.get_dbInfo(xmlStr, 'P')
            connectInfo = entity.DBConnectEntity(dbAddress, dbUser, dbPassword)

        itemType=self.treeCtrlDatabaseShow.GetItemData(self.selectedItem)


        if itemType=='database':

            databaseName = self.treeCtrlDatabaseShow.GetItemText(self.selectedItem)

            HttpRequestThread(action=config.TASK_GET_TABLES,shellEntity=self.shellEntity,connectInfo=connectInfo,databaseName=databaseName,callBack=self.Callback_getTables,statusCallback=self.parent.SetHttpStatus).start()

        elif itemType=='table':

            databaseName = self.treeCtrlDatabaseShow.GetItemText(
                self.treeCtrlDatabaseShow.GetItemParent(self.selectedItem))
            tableName = self.treeCtrlDatabaseShow.GetItemText(self.selectedItem)

            HttpRequestThread(action=config.TASK_GET_COLUMNS, shellEntity=self.shellEntity, connectInfo=connectInfo,
                              databaseName=databaseName,tableName=tableName, callBack=self.Callback_getColumns,
                              statusCallback=self.parent.SetHttpStatus).start()

            self.comboBoxSqlQueryString.SetValue('SELECT *FROM {0} ORDER BY 1 DESC'.format(tableName))

        event.Skip()

    def Callback_getTables(self,resultCode, resultContent):
        if resultCode:
            tableList = resultContent.split('\t')
            for table in tableList:
                if table:
                    self.treeCtrlDatabaseShow.AppendItem(self.selectedItem, table, self.tableImg, data='table')
                    self.treeCtrlDatabaseShow.Expand(self.selectedItem)

    def Callback_getColumns(self,resultCode, resultContent):
        if resultCode:
            tableList = resultContent.split('\t')
            for table in tableList:
                if table:
                    self.treeCtrlDatabaseShow.AppendItem(self.selectedItem, table, self.columnImg)
                    self.treeCtrlDatabaseShow.Expand(self.selectedItem)

    def OnTreeItemClick(self,event):
        pt = event.GetPosition()
        item, flags = self.treeCtrlDatabaseShow.HitTest(pt)
        if item:
            self.selectedItem = item
            self.treeCtrlDatabaseShow.SelectItem(item)
        event.Skip()

    def OnButtonQueryClick(self,event):

        self.listCtrlTableShow.DeleteAllItems()
        self.listCtrlTableShow.DeleteAllColumns()

        connectInfo = None
        xmlStr = '<root>{0}</root>'.format(self.shellEntity.database_info.replace('&','&amp;'))
        if self.shellEntity.shell_script_type == 'JSP':
            connectInfo = commonsUtil.get_dbInfo(xmlStr, 'X')
        elif self.shellEntity.shell_script_type == 'PHP':
            dbAddress = commonsUtil.get_dbInfo(xmlStr, 'H')
            dbUser = commonsUtil.get_dbInfo(xmlStr, 'U')
            dbPassword = commonsUtil.get_dbInfo(xmlStr, 'P')
            connectInfo = entity.DBConnectEntity(dbAddress, dbUser, dbPassword)

        databaseName = self.treeCtrlDatabaseShow.GetItemText(self.treeCtrlDatabaseShow.GetItemParent(self.selectedItem))

        queryString=self.comboBoxSqlQueryString.GetValue()

        HttpRequestThread(action=config.TASK_EXCUTE_SQLQUERY,shellEntity=self.shellEntity,connectInfo=connectInfo,databaseName=databaseName,queryString=queryString,callBack=self.Callback_excuteSqlQuery,statusCallback=self.parent.SetHttpStatus).start()

    def Callback_excuteSqlQuery(self,resultCode, resultContent):
        if resultCode:
            result_list=resultContent.split('\r\n')
            columnsNameList=result_list[0].split('\t|\t')
            for index in range(0,len(columnsNameList)):
                if columnsNameList[index]:
                    self.listCtrlTableShow.InsertColumn(index, columnsNameList[index])

            for index in range(1,len(result_list)):
                if result_list[index]:
                    itemList = result_list[index].split('\t|\t')
                    insertItem=self.listCtrlTableShow.InsertItem(0, itemList[0])
                    for itemIndex in range(1, len(itemList)):
                        if itemList[itemIndex]:
                            self.listCtrlTableShow.SetItem(insertItem,itemIndex, itemList[itemIndex])


    def __del__(self):
        pass
