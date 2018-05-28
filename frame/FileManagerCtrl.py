# coding=utf-8

"""
@version: 1.0
@author: chaowei
@file: FileManagerCtrlNew.py
@time: 2018/5/2 22:30
"""

import wx, sys, os
import wx.lib.mixins.listctrl as listmix

sys.path.append("..")

from WorkThread import HttpRequestThread
from utils import commonsUtil,config

class SortableListCtrl(wx.ListCtrl,listmix.ColumnSorterMixin,listmix.ListCtrlAutoWidthMixin):
    def __init__(self, parent, ID, pos=wx.DefaultPosition,
                 size=wx.DefaultSize, style=0):
        wx.ListCtrl.__init__(self, parent, ID, pos, size, style)
        listmix.ListCtrlAutoWidthMixin.__init__(self)
        listmix.ColumnSorterMixin.__init__(self,4)

    def GetListCtrl(self):
        return self

class FileManager(wx.Panel):
    def __init__(self, parent, log, shellEntity):
        wx.Panel.__init__(self, parent, -1, wx.DefaultPosition, wx.DefaultSize)

        self.shellEntity = shellEntity
        self.parent = parent
        self.log = log
        self.selectedDirectoryItemIndex=-1
        
        self.separator='\\'

        bSizerMain = wx.BoxSizer(wx.VERTICAL)

        bSizerTop = wx.BoxSizer(wx.HORIZONTAL)

        comboBoxPathChoices = []
        self.comboBoxPath = wx.ComboBox(self, wx.ID_ANY, wx.EmptyString, wx.DefaultPosition, wx.DefaultSize,
                                        comboBoxPathChoices, 0)
        bSizerTop.Add(self.comboBoxPath, 1, wx.ALIGN_CENTER_VERTICAL)

        self.buttonRead = wx.Button(self, wx.ID_ANY, u"读取", wx.DefaultPosition, (50,-1), 0)
        bSizerTop.Add(self.buttonRead, 0, wx.ALL, 2)

        bSizerMain.Add(bSizerTop, 0, wx.EXPAND, 5)

        bSizerBottom = wx.BoxSizer(wx.HORIZONTAL)

        bSizerFileTree = wx.BoxSizer(wx.VERTICAL)

        bSizerStatus = wx.BoxSizer(wx.HORIZONTAL)

        self.staticTextHost = wx.StaticText(self, wx.ID_ANY, u" ", wx.DefaultPosition, wx.DefaultSize,
                                              0)
        bSizerStatus.Add(self.staticTextHost, 1, wx.LEFT|wx.EXPAND,5)

        self.staticTextCount = wx.StaticText(self, wx.ID_ANY, u" ", wx.DefaultPosition, wx.DefaultSize, 0)
        bSizerStatus.Add(self.staticTextCount, 1, wx.EXPAND)

        bSizerFileTree.Add(bSizerStatus, 0, wx.EXPAND, 5)

        self.treeCtrlFile = wx.TreeCtrl(self, wx.ID_ANY, wx.DefaultPosition, wx.DefaultSize, wx.TR_HAS_BUTTONS|wx.TR_HIDE_ROOT|wx.TR_NO_LINES)
        bSizerFileTree.Add(self.treeCtrlFile, 1, wx.ALL | wx.EXPAND, 5)

        bSizerBottom.Add(bSizerFileTree, 1, wx.EXPAND, 5)

        bSizerDirectoryList = wx.BoxSizer(wx.VERTICAL)

        self.listCtrlDirectory = SortableListCtrl(self, wx.ID_ANY, wx.DefaultPosition, wx.DefaultSize, wx.LC_REPORT)
        bSizerDirectoryList.Add(self.listCtrlDirectory, 1, wx.ALL | wx.EXPAND, 5)

        bSizerBottom.Add(bSizerDirectoryList, 2, wx.EXPAND, 5)

        bSizerMain.Add(bSizerBottom, 1, wx.EXPAND, 5)

        self.il = wx.ImageList(16, 16)
        self.fileImage = self.il.Add(wx.ArtProvider.GetBitmap(wx.ART_NORMAL_FILE, wx.ART_OTHER, (16, 16)))
        self.folderImage = self.il.Add(wx.ArtProvider.GetBitmap(wx.ART_FOLDER, wx.ART_OTHER, (16,16)))
        self.harddiskImage = self.il.Add(wx.ArtProvider.GetBitmap(wx.ART_HARDDISK, wx.ART_OTHER, (16,16)))

        self.listCtrlDirectory.SetImageList(self.il, wx.IMAGE_LIST_SMALL)
        self.treeCtrlFile.SetImageList(self.il)

        self.listCtrlDirectory.InsertColumn(0, u'名称',width=80)
        self.listCtrlDirectory.InsertColumn(1, u"时间",width=80)
        self.listCtrlDirectory.InsertColumn(2, u"大小",width=80)
        self.listCtrlDirectory.InsertColumn(3, u"属性",width=80)

        self.SetSizer(bSizerMain)

        #windows下第一次点击，会莫名其妙触发两次，暂未定位到问题
        self.treeCtrlFile.Bind(wx.EVT_TREE_SEL_CHANGED, self.OnFileTreeItemClick)

        self.listCtrlDirectory.Bind(wx.EVT_LEFT_DCLICK, self.OnDirectoryItemDoubleClick)
        self.listCtrlDirectory.Bind(wx.EVT_LIST_ITEM_SELECTED, self.OnDirectoryItemSelected)
        self.listCtrlDirectory.Bind(wx.EVT_LIST_ITEM_DESELECTED, self.OnDirectoryItemDeSelected)

        #windows右键
        self.listCtrlDirectory.Bind(wx.EVT_COMMAND_RIGHT_CLICK, self.OnDirectoryItemRightClick)
        #linux右键
        self.listCtrlDirectory.Bind(wx.EVT_RIGHT_UP, self.OnDirectoryItemRightClick)

        self.buttonRead.Bind(wx.EVT_BUTTON,self.OnButtonReadClick)

    #外部调用
    def OnInit(self):
        self.OnInitMenu()

        self.root = self.treeCtrlFile.AddRoot(config.FILE_TREE_ROOT_TEXT)

        self.staticTextHost.SetLabelText(self.shellEntity.shell_host)

        # 返回当前路径
        HttpRequestThread(config.TASK_GET_START,shellEntity=self.shellEntity,callBack=self.CallBack_getStart,statusCallback=self.parent.SetStatus).start()

    def hasChild(self,treeCtrl,parentItem,childItemText):

        item, cookie = treeCtrl.GetFirstChild(parentItem)

        if item:

            if treeCtrl.GetItemText(item)  == childItemText:
                return item

            while item.IsOk():

                item, cookie = treeCtrl.GetNextChild(parentItem, cookie)

                if item:

                    if treeCtrl.GetItemText(item) == childItemText:
                        return item

        return None

    def InsertChildItem(self,treeCtrl,parentItem,childTextList):
        for itemText in childTextList:
            parentItem = treeCtrl.AppendItem(parentItem, itemText, image=self.folderImage)
        return parentItem

    def OnButtonReadClick(self,event):
        path=self.comboBoxPath.GetValue()
        if path:
            directoryList=path.split(self.separator)
            directoryList=[item for item in filter(lambda x: x != '', directoryList)]
            index=0
            if path.startswith('/'):
                parentItem=self.realRootItem
            else:
                parentItem=self.treeCtrlFile.GetRootItem()
            newItem=None
            while True:
                childItem=self.hasChild(self.treeCtrlFile,parentItem,directoryList[index])
                if childItem == None:
                    newItem=self.InsertChildItem(self.treeCtrlFile,parentItem,directoryList[index:])
                    self.selectedFileTreeItem=newItem
                else:
                    parentItem=childItem
                    index+=1
                if index==len(directoryList):
                    break
            if newItem:
                self.treeCtrlFile.SelectItem(newItem)
            else:
                self.treeCtrlFile.SelectItem(childItem)
        else:
            wx.MessageBox('路径不能为空')

    def CallBack_getStart(self,resultCode,resultContent):

        newInsertItem=None

        if resultCode:

            if resultContent.startswith('/'):

                self.separator = '/'

                currentDirectoryPath = resultContent.split('\t')[0]

                shellFolder = currentDirectoryPath.split(self.separator)

                self.realRootItem =newInsertItem = self.treeCtrlFile.AppendItem(self.root, '/', image=self.harddiskImage)
                # 初始化根
                for item in shellFolder:
                    if item:
                        newInsertItem = self.treeCtrlFile.AppendItem(newInsertItem, item, image=self.folderImage)

            else:
                self.separator = '\\'
                inforList=resultContent.split('\t')
                currentDirectoryPath, disks = inforList[0],inforList[1]
                diskList = disks.split(':')
                shellFolder = currentDirectoryPath.split(self.separator)

                for disk in diskList:

                    if disk + ':' == shellFolder[0]:
                        self.realRootItem=newInsertItem = self.treeCtrlFile.AppendItem(self.root, disk + ':', image=self.harddiskImage)

                        # 初始化根
                        for item in shellFolder:
                            if item and item != disk + ':':
                                newInsertItem = self.treeCtrlFile.AppendItem(newInsertItem, item,
                                                                             image=self.folderImage)
                    elif disk:

                        self.treeCtrlFile.AppendItem(self.root, disk + ':', image=self.harddiskImage)

            self.treeCtrlFile.ExpandAll()

            if newInsertItem:
                self.treeCtrlFile.SelectItem(newInsertItem)

    def OnInitMenu(self):
        self.fileManageMenu = wx.Menu()
        for text in config.FILE_MANAGE_MENU.split():
            item = self.fileManageMenu.Append(-1, text)
            self.listCtrlDirectory.Bind(wx.EVT_MENU, self.OnFileManageMenuItemSelected, item)

        self.directoryManageMenu = wx.Menu()
        for text in config.DIRECTORY_MANAGE_MENU.split():
            item = self.directoryManageMenu.Append(-1, text)
            self.listCtrlDirectory.Bind(wx.EVT_MENU, self.OnDirectoryManageMenuItemSelected, item)

        self.emptyDirectoryManageMenu = wx.Menu()
        for text in config.EMPTY_DIRECTORY_MANAGE_MENU.split():
            item = self.emptyDirectoryManageMenu.Append(-1, text)
            self.listCtrlDirectory.Bind(wx.EVT_MENU, self.OnEmptyDirectoryManageMenuItemSelected, item)

    def OnFileTreeItemClick(self, event):
        item = event.GetItem()
        if item:
            self.DoFileTreeItemClick(item)
        event.Skip()

    def OnDirectoryItemDoubleClick(self, event):
        itemName=self.selectedDirectoryItemList[self.selectedDirectoryItemIndex]
        if commonsUtil.isDirectory(itemName):
            self.ClickFileTreeItemByName(itemName)
        else:
            self.OpenNewFileEditor(itemName)
        event.Skip()

    def OnDirectoryItemSelected(self, event):
        self.selectedDirectoryItemIndex = event.Index
        event.Skip()

    def OnDirectoryItemDeSelected(self, event):
        self.selectedDirectoryItemIndex = -1
        event.Skip()

    def OnDirectoryItemRightClick(self, event):
        if self.selectedDirectoryItemIndex==-1:
            self.listCtrlDirectory.PopupMenu(self.emptyDirectoryManageMenu)
        else:
            if commonsUtil.isDirectory(self.selectedDirectoryItemList[self.selectedDirectoryItemIndex]):
                self.listCtrlDirectory.PopupMenu(self.directoryManageMenu)
            else:
                self.listCtrlDirectory.PopupMenu(self.fileManageMenu)
        event.Skip()

    def OnDirectoryManageMenuItemSelected(self,event):
        item = self.directoryManageMenu.FindItemById(event.GetId())

        text = item.GetText()

        path = self.getItemPath(self.selectedFileTreeItem)

        itemName=self.selectedDirectoryItemList[self.selectedDirectoryItemIndex]

        if text == u'下载文件到服务器':
            pass

        if text == u'上传':
            self.UploadFile(path)

        if text == u'删除':
            HttpRequestThread(action=config.TASK_DELETE_FILE_OR_DIRECTORY, shellEntity=self.shellEntity,
                              path=path + self.separator + itemName, callBack=None,
                              statusCallback=self.parent.SetStatus).start()
        self.UpdateFileTree(self.selectedFileTreeItem)
        event.Skip()

    def OnEmptyDirectoryManageMenuItemSelected(self,event):
        item = self.emptyDirectoryManageMenu.FindItemById(event.GetId())

        text = item.GetText()

        path = self.getItemPath(self.selectedFileTreeItem)

        if text == u'下载文件到服务器':
            pass

        if text == u'上传':
            self.UploadFile(path)

        self.UpdateFileTree(self.selectedFileTreeItem)

    def OnFileManageMenuItemSelected(self, event):

        item = self.fileManageMenu.FindItemById(event.GetId())

        text = item.GetText()

        remotePath=self.getItemPath(self.selectedFileTreeItem)

        itemName = self.selectedDirectoryItemList[self.selectedDirectoryItemIndex]

        fileLength=int(self.listCtrlDirectory.GetItemText(self.selectedDirectoryItemIndex,2))

        if text==u'下载文件到服务器':
            pass

        if text==u'上传':
            self.UploadFile(remotePath)
            self.UpdateFileTree(self.selectedFileTreeItem)

        if text==u'下载':
            dlg = wx.FileDialog(
                self, message="下载为", defaultDir=os.getcwd(),
                defaultFile=itemName, wildcard="All files (*.*)|*.*", style=wx.FD_SAVE | wx.FD_OVERWRITE_PROMPT
            )

            if dlg.ShowModal() == wx.ID_OK:
                localPath = dlg.GetPath()
                HttpRequestThread(action=config.TASK_DOWNLOAD_FILE,shellEntity=self.shellEntity,path=remotePath+self.separator+itemName,localPath=localPath,fileLength=fileLength,callBack=None,statusCallback=self.parent.SetStatus).start()

        if text ==u'删除':
            HttpRequestThread(action=config.TASK_DELETE_FILE_OR_DIRECTORY,shellEntity=self.shellEntity,path=remotePath+self.separator+itemName,callBack=None,statusCallback=self.parent.SetStatus).start()
            self.UpdateFileTree(self.selectedFileTreeItem)

        if text==u'编辑':
            self.OpenNewFileEditor(text)

    def UploadFile(self,remotePath):
        dlg = wx.FileDialog(
            self, message="选择文件", defaultDir=os.getcwd(),
            defaultFile='', wildcard="All files (*.*)|*.*", style=wx.FD_OPEN
        )

        if dlg.ShowModal() == wx.ID_OK:
            localFilename=dlg.GetFilename()
            localPath=dlg.GetPath()
            with open(localPath,'rb') as file:
                content=file.read()
            if content:
                HttpRequestThread(action=config.TASK_UPLOAD_FILE,shellEntity=self.shellEntity,path=remotePath+self.separator+localFilename,content=content.encode('hex'),callBack=None,statusCallback=self.parent.SetStatus).start()

    def ClickFileTreeItemByName(self,itemName):

        item,cookie=self.treeCtrlFile.GetFirstChild(self.selectedFileTreeItem)

        if self.treeCtrlFile.GetItemText(item)+'/' ==itemName:

            self.treeCtrlFile.SelectItem(item)

            return

        while item.IsOk():

            item,cookie=self.treeCtrlFile.GetNextChild(self.selectedFileTreeItem,cookie)

            if item:

                if self.treeCtrlFile.GetItemText(item) + '/' == itemName:

                    self.treeCtrlFile.SelectItem(item)

                    return

    def DoFileTreeItemClick(self,item):
        if item:
            self.selectedFileTreeItem = item
                #更新子节点
            self.UpdateFileTree(item)

    def UpdateFileTree(self, selectedItem):
        #获取当前单击item的对应路径
        path = self.getItemPath(selectedItem)

        self.comboBoxPath.SetValue(path)

        HttpRequestThread(config.TASK_GET_DIRECTORY_CONTENT,shellEntity=self.shellEntity,path=path,callBack=self.Callback_getDirectoryContent,statusCallback=self.parent.SetStatus).start()

    def Callback_getDirectoryContent(self,resultCode,resultContent):

        # 更新文件列表
        if resultCode:

            directoryList=self.UpdateDirectoryContent(resultContent)

            self.UpdateFileTreeChildItem(directoryList)

    def UpdateFileTreeChildItem(self,directoryList):

        selectedItem = self.selectedFileTreeItem

        hasNewChild = False
        for directoryName in directoryList:
            if self.hasChild(self.treeCtrlFile,selectedItem,directoryName.replace('/',''))==None:
                hasNewChild = True
                newItem = self.treeCtrlFile.AppendItem(selectedItem, directoryName)
                self.treeCtrlFile.SetItemImage(newItem, self.folderImage, wx.TreeItemIcon_Normal)
        if hasNewChild:
            self.treeCtrlFile.Expand(selectedItem)

    #更新目录的文件列表
    def UpdateDirectoryContent(self, directoryContent):
        self.listCtrlDirectory.DeleteAllItems()

        self.selectedDirectoryItemList = []

        subDirectoryList=[]

        directoryCount=0
        fileCount=0

        contentList = directoryContent.split('\n')

        directoryContentData={}

        for content in contentList:
            itemName, createTime, fileSize, accessPermission='','','',''

            try:
                contentElements = content.split('\t')
                itemName = contentElements[0]
                createTime = contentElements[1]
                fileSize = contentElements[2]
                accessPermission = contentElements[3]
            except Exception:
                pass

            if itemName == './' or itemName == '../':
                continue

            self.selectedDirectoryItemList.append(itemName)

            directoryFlag = commonsUtil.isDirectory(itemName)

            if directoryFlag:
                directoryCount+=1
                directoryName = itemName[:len(itemName) - 1]
                subDirectoryList.append(directoryName.replace('/',self.separator))
                index = self.listCtrlDirectory.InsertItem(self.listCtrlDirectory.GetItemCount(), directoryName, self.folderImage)
            else:
                fileCount+=1
                index = self.listCtrlDirectory.InsertItem(self.listCtrlDirectory.GetItemCount(), itemName, self.fileImage)

            self.listCtrlDirectory.SetItem(index, 1, createTime)
            self.listCtrlDirectory.SetItem(index, 2, fileSize)
            self.listCtrlDirectory.SetItem(index, 3, accessPermission)
            self.listCtrlDirectory.SetItemData(index,index+1)

            directoryContentData[index+1]=(itemName, createTime, fileSize, accessPermission)

        self.listCtrlDirectory.itemDataMap=directoryContentData

        # 设置文件列表属性的宽度
        if directoryCount+fileCount>0:
            self.listCtrlDirectory.SetColumnWidth(0, wx.LIST_AUTOSIZE)
            self.listCtrlDirectory.SetColumnWidth(1, wx.LIST_AUTOSIZE)
            self.listCtrlDirectory.SetColumnWidth(2, wx.LIST_AUTOSIZE)
            self.listCtrlDirectory.SetColumnWidth(3, wx.LIST_AUTOSIZE)

        self.staticTextCount.SetLabelText('目录（{0}），文件（{1}）'.format(directoryCount,fileCount))

        return subDirectoryList

    def getItemPath(self,item):

        path=self.treeCtrlFile.GetItemText(item)

        if path == '/':
            return path

        if ':' in path:
            return path+self.separator

        parentItem= self.treeCtrlFile.GetItemParent(item)
        while parentItem.IsOk():

            itemText=self.treeCtrlFile.GetItemText(parentItem)

            if itemText == '/':
                path = self.treeCtrlFile.GetItemText(parentItem) + path
                break

            path=self.treeCtrlFile.GetItemText(parentItem)+self.separator+path

            if ':' in itemText:
                break

            parentItem= self.treeCtrlFile.GetItemParent(parentItem)
        return path

    def OpenNewFileEditor(self, fileName):
        path = self.getItemPath(self.selectedFileTreeItem)
        filePath=path + self.separator + fileName
        self.parent.OpenFileEditor(fileName, filePath, self.shellEntity)