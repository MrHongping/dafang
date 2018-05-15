# coding=utf-8

"""
@version: 1.0
@author: chaowei
@file: FileManagerCtrlNew.py
@time: 2018/5/2 22:30
"""

import wx, sys, os

sys.path.append("..")
from utils.shell import ShellTools
from utils import commonsUtil,config


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
        bSizerTop.Add(self.comboBoxPath, 1, wx.ALL | wx.ALIGN_CENTER_VERTICAL, 5)

        self.buttonRead = wx.Button(self, wx.ID_ANY, u"读取", wx.DefaultPosition, wx.DefaultSize, 0)
        bSizerTop.Add(self.buttonRead, 0, wx.ALL, 5)

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

        self.listCtrlDirectory = wx.ListCtrl(self, wx.ID_ANY, wx.DefaultPosition, wx.DefaultSize, wx.LC_REPORT)
        bSizerDirectoryList.Add(self.listCtrlDirectory, 1, wx.ALL | wx.EXPAND, 5)

        bSizerBottom.Add(bSizerDirectoryList, 2, wx.EXPAND, 5)

        bSizerMain.Add(bSizerBottom, 1, wx.EXPAND, 5)

        self.il = wx.ImageList(16, 16)
        self.fileImage = self.il.Add(wx.ArtProvider.GetBitmap(wx.ART_NORMAL_FILE, wx.ART_OTHER, (16, 16)))
        self.folderImage = self.il.Add(wx.ArtProvider.GetBitmap(wx.ART_FOLDER, wx.ART_OTHER, (16,16)))
        self.harddiskImage = self.il.Add(wx.ArtProvider.GetBitmap(wx.ART_HARDDISK, wx.ART_OTHER, (16,16)))

        self.listCtrlDirectory.SetImageList(self.il, wx.IMAGE_LIST_SMALL)
        self.treeCtrlFile.SetImageList(self.il)

        self.listCtrlDirectory.InsertColumn(0, u'名称')
        self.listCtrlDirectory.InsertColumn(1, u"时间")
        self.listCtrlDirectory.InsertColumn(2, u"大小")
        self.listCtrlDirectory.InsertColumn(3, u"属性")

        self.SetSizer(bSizerMain)

        self.treeCtrlFile.Bind(wx.EVT_LEFT_DOWN, self.OnFileTreeItemClick)


        self.listCtrlDirectory.Bind(wx.EVT_LEFT_DCLICK, self.OnDirectoryItemDoubleClick)
        self.listCtrlDirectory.Bind(wx.EVT_LIST_ITEM_SELECTED, self.OnDirectoryItemSelected)
        self.listCtrlDirectory.Bind(wx.EVT_LIST_ITEM_DESELECTED, self.OnDirectoryItemDeSelected)

        #windows右键
        self.listCtrlDirectory.Bind(wx.EVT_COMMAND_RIGHT_CLICK, self.OnDirectoryItemRightClick)
        #linux右键
        self.listCtrlDirectory.Bind(wx.EVT_RIGHT_UP, self.OnDirectoryItemRightClick)

    #外部调用
    def OnInit(self):
        self.OnInitMenu()

        self.root = self.treeCtrlFile.AddRoot(config.FILE_TREE_ROOT_TEXT)

        self.staticTextHost.SetLabelText(self.shellEntity.shell_host)
        # 发送Shell初始化请求
        self.shellTools = ShellTools.getShellTools(self.shellEntity)

        # 返回当前路径
        resultCode, resultContent = self.shellTools.getStart()

        self.UpdateStatusUI(resultCode, resultContent, resultContent)

        if resultCode==config.REQUESTS_SUCCESS:

            if resultContent.startswith('/'):

                self.separator='/'

                currentDirectoryPath = resultContent

                shellFolder = currentDirectoryPath.split(self.separator)

                child = {}

                # 初始化根
                for x in range(0, len(shellFolder)):
                    if x == 0:
                        child[x] = self.treeCtrlFile.AppendItem(self.root, '/',image=self.harddiskImage)
                    else:
                        child[x] = self.treeCtrlFile.AppendItem(child[x - 1], shellFolder[x],image=self.folderImage)

                    self.treeCtrlFile.SelectItem(child[x])

            else:
                self.separator = '\\'
                currentDirectoryPath,disks=resultContent.split('\t')
                diskList=disks.split(':')
                shellFolder=currentDirectoryPath.split(self.separator)
                child = {}

                for disk in diskList:
                    if disk:
                        newItem=self.treeCtrlFile.AppendItem(self.root, disk+':', image=self.harddiskImage)
                        if shellFolder[0]==disk+':':

                            # 初始化根
                            for x in range(1, len(shellFolder)):
                                if x == 1:
                                    child[x] = self.treeCtrlFile.AppendItem(newItem, shellFolder[x], image=self.folderImage)
                                else:
                                    child[x] = self.treeCtrlFile.AppendItem(child[x - 1], shellFolder[x], image=self.folderImage)

                                self.treeCtrlFile.SelectItem(child[x])

            self.treeCtrlFile.ExpandAll()

            self.comboBoxPath.SetValue('请求中...')

            # 返回目录列表或错误信息
            resultCode, resultContent = self.shellTools.getDirectoryContent(currentDirectoryPath)

            self.UpdateStatusUI(resultCode, resultContent,currentDirectoryPath)

            # 初始化文件列表
            if resultCode:
                self.UpdateDirectoryContent(resultContent)

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
        pt = event.GetPosition()
        item, flags = self.treeCtrlFile.HitTest(pt)
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
            self.shellTools.deleteFileOrDirectory(path + self.separator + itemName)
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

            dlg.SetFilterIndex(2)

            if dlg.ShowModal() == wx.ID_OK:
                localPath = dlg.GetPath()
                self.log.WriteText('You selected "%s"' % localPath)
                count=0
                with open(localPath,'ab') as file:
                    for data in self.shellTools.downloadFile(remotePath+self.separator+itemName):

                        #删掉菜刀响应标识符，文件前三个字节和后三个字节
                        if count==0:
                            data=data[len(config.SPLIT_SYMBOL_LEFT):]
                        elif count+len(data)>fileLength:
                            data = data[:fileLength-count]

                        file.write(data)

                        count+=len(data)

        if text ==u'删除':
            self.shellTools.deleteFileOrDirectory(remotePath+self.separator+itemName)
            self.UpdateFileTree(self.selectedFileTreeItem)

        if text==u'编辑':
            self.OpenNewFileEditor(text)

    def UploadFile(self,remotePath):
        dlg = wx.FileDialog(
            self, message="选择文件", defaultDir=os.getcwd(),
            defaultFile='', wildcard="All files (*.*)|*.*", style=wx.FD_OPEN
        )

        dlg.SetFilterIndex(2)

        if dlg.ShowModal() == wx.ID_OK:
            localFilename=dlg.GetFilename()
            localPath=dlg.GetPath()
            with open(localPath,'rb') as file:
                content=file.read()
            if content:
                self.shellTools.uploadFile(remotePath+self.separator+localFilename,content.encode('hex'))

    def ClickFileTreeItemByName(self,itemName):

        item,cookie=self.treeCtrlFile.GetFirstChild(self.selectedFileTreeItem)

        if self.treeCtrlFile.GetItemText(item)+'/' ==itemName:

            self.DoFileTreeItemClick(item)

            return

        while item.IsOk():

            item,cookie=self.treeCtrlFile.GetNextChild(self.selectedFileTreeItem,cookie)

            if item:

                if self.treeCtrlFile.GetItemText(item) + '/' == itemName:

                    self.DoFileTreeItemClick(item)

                    return

    def DoFileTreeItemClick(self,item):
        if item:
            self.selectedFileTreeItem = item
            self.treeCtrlFile.SelectItem(item)
            #更新子节点
            self.UpdateFileTree(item)

    def UpdateFileTree(self, selectedItem):
        #获取当前单击item的对应路径
        path = self.getItemPath(selectedItem)

        self.comboBoxPath.SetValue('请求中...')
        resultCode, resultContent = self.shellTools.getDirectoryContent(path)

        self.UpdateStatusUI(resultCode,resultContent,path)

        # 更新文件列表
        if resultCode:
            directoryList=self.UpdateDirectoryContent(resultContent)

            itemChildrenTextList = []
            child, cookie = self.treeCtrlFile.GetFirstChild(selectedItem)
            if child:
                itemChildrenTextList.append(self.treeCtrlFile.GetItemText(child))
                while (child.IsOk()):
                    child, cookie = self.treeCtrlFile.GetNextChild(selectedItem, cookie)
                    if child:
                        itemChildrenTextList.append(self.treeCtrlFile.GetItemText(child))

            for directoryName in directoryList:
                if directoryName not in itemChildrenTextList:
                    newItem = self.treeCtrlFile.AppendItem(selectedItem, directoryName)
                    self.treeCtrlFile.SetItemData(newItem, None)
                    self.treeCtrlFile.SetItemImage(newItem, self.folderImage, wx.TreeItemIcon_Normal)
            self.treeCtrlFile.Expand(selectedItem)

    def UpdateStatusUI(self, resultCode, resultContent, path):
        if not resultCode:
            self.SetRequestStatusText(resultContent)
            self.staticTextCount.SetLabelText('请求完成，但有错误发生')
        else:
            self.SetRequestStatusText('请求成功')
        self.SetComboBoxText(path)

    #更新目录的文件列表
    def UpdateDirectoryContent(self, directoryContent):
        self.listCtrlDirectory.DeleteAllItems()

        self.selectedDirectoryItemList = []

        subDirectoryList=[]

        directoryCount=0
        fileCount=0

        contentList = directoryContent.split('\n')

        for content in contentList:
            contentElements = content.split('\t')

            if len(contentElements) < 3:
                continue

            itemName = contentElements[0]
            createTime = contentElements[1]
            fileSize = contentElements[2]
            accessPermission = contentElements[3]

            self.selectedDirectoryItemList.append(itemName)

            elementParams = ''
            for i in range(4, len(contentElements)):
                elementParams += ' ' + contentElements[i]

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

        # 设置文件列表属性的宽度
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
        #resultCode, fileContent = ShellTools.getShellTools(self.shellEntity).getFileContent(path + self.separator + fileName)
        self.parent.OpenFileEditor(fileName, filePath, self.shellEntity)

    def SetRequestStatusText(self, text):
        self.parent.SetRequestStatusText(text)

    def SetComboBoxText(self, text):
        self.comboBoxPath.SetValue(text)