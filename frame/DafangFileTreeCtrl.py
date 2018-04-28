# -*- coding: UTF-8 -*-

import  wx,sys

sys.path.append("..")
from utils.shell import ShellTools
import  wx.lib.mixins.treemixin as tm
#---------------------------------------------------------------------------

class FileTree(wx.TreeCtrl,tm.VirtualTree):
    def __init__(self, parent, id, pos, size, style, log):
        wx.TreeCtrl.__init__(self, parent, id, pos, size, style)
        self.log = log

    def OnCompareItems(self, item1, item2):
        t1 = self.GetItemText(item1)
        t2 = self.GetItemText(item2)
        self.log.WriteText('compare: ' + t1 + ' <> ' + t2 + '\n')
        if t1 < t2: return -1
        if t1 == t2: return 0
        return 1

#---------------------------------------------------------------------------

class DafangFileTree(wx.Panel):

    def __init__(self, parent, log,shellEntity):
        self.parent=parent

        self.shellEntity=shellEntity
        wx.Panel.__init__(self, parent, -1, style=wx.WANTS_CHARS)
        self.Bind(wx.EVT_SIZE, self.OnSize)

        self.log = log
        
        tID = wx.NewId()
        sizer = wx.BoxSizer(wx.VERTICAL)

        self.tree = FileTree(self, tID, wx.DefaultPosition, wx.DefaultSize,
                               wx.TR_HAS_BUTTONS
                               , self.log)
        
        isz = (16,16)
        il = wx.ImageList(isz[0], isz[1])
        self.folderImage = il.Add(wx.ArtProvider.GetBitmap(wx.ART_FOLDER,wx.ART_OTHER, isz))
        self.harddiskImage=il.Add(wx.ArtProvider.GetBitmap(wx.ART_HARDDISK,wx.ART_OTHER, isz))

        self.tree.SetImageList(il)
        self.il = il

        self.Bind(wx.EVT_TREE_SEL_CHANGED, self.OnSelChanged, self.tree)

        self.tree.Bind(wx.EVT_LEFT_DOWN, self.OnLeftClick)
        
        self.FileTreeInit()
        sizer.Add(self.tree, 1, wx.EXPAND)
        self.SetSizer(sizer)
        self.selectedItem=None

    def UpdateStatusUI(self,resultCode,resultContent,otherInfo=''):
        print resultContent
        if not resultCode:
            self.parent.SetRequestStatusText(resultContent)
            self.parent.SetComboBoxText('请求错误')
            return
        else:
            self.parent.SetRequestStatusText('请求成功')
            self.parent.SetComboBoxText(otherInfo)

    def FileTreeInit(self):
        # 发送Shell初始化请求
        self.shellTools = ShellTools.getShellTools(self.shellEntity)

        #返回当前路径
        resultCode,startResultContent = self.shellTools.getStart()

        self.UpdateStatusUI(resultCode,startResultContent,startResultContent)

        #初始化根
        self.root = self.tree.AddRoot("/",self.harddiskImage)
        self.tree.SetItemData(self.root, None)

        shellFolder=startResultContent.split('/')
        
        child={}
        
        #初始化文件树
        for x in range(1,len(shellFolder)):
            if x==1:
                child[x]=self.tree.AppendItem(self.root, shellFolder[x])
            else:
                child[x]=self.tree.AppendItem(child[x-1], shellFolder[x])
                
            self.tree.SetItemData(child[x], None)
            self.tree.SetItemImage(child[x], self.folderImage, wx.TreeItemIcon_Normal)
            
        self.tree.ExpandAll()

        self.parent.SetComboBoxText('请求中...')

        #返回目录列表或错误信息
        resultCode, directoryResultContent = self.shellTools.getDirectoryContent(startResultContent)

        self.UpdateStatusUI(resultCode, directoryResultContent)


        #初始化文件列表    
        self.parent.DafangFileListCtrl.UpdateDirectory(directoryResultContent)


    # def GetDirectoryContent(self,path):
    #     resultCode,resultContent=self.shellTools.getDirectoryContent(path)
    #     return None

    def OnSize(self, event):
        w,h = self.GetClientSize()
        self.tree.SetSize(0, 0, w, h)

    def OnLeftClick(self, event):
        pt = event.GetPosition()
        item, flags = self.tree.HitTest(pt)
        if item:
            self.OnItemClick(item)

        event.Skip()

    def ClickItemByName(self,itemName):
        item,cookie=self.tree.GetFirstChild(self.selectedItem)
        if self.tree.GetItemText(item)+'/' ==itemName:
            self.OnItemClick(item)
            return
        while item.IsOk():
            item,cookie=self.tree.GetNextChild(self.selectedItem,cookie)
            if item:
                if self.tree.GetItemText(item) + '/' == itemName:
                    self.OnItemClick(item)
                    return

    def OnItemClick(self,item):
        if item:
            self.selectedItem = item
            self.tree.SelectItem(item)
            self.log.WriteText("OnLeftClick: %s\n" % self.tree.GetItemText(item))
            #更新子节点
            subDirectoryList=self.UpdateFileList(item)
            self.UpdateItemChild(item,subDirectoryList)

    def getSelectedItemPath(self):
        path=self.tree.GetItemText(self.selectedItem)
        item= self.tree.GetItemParent(self.selectedItem)
        while item.IsOk():
            itemText=self.tree.GetItemText(item)
            if itemText !='/':
                path=self.tree.GetItemText(item)+'/'+path
            item= self.tree.GetItemParent(item)
        return '/'+path

    def OnSelChanged(self, event):
        item = event.GetItem()
        if item:
            self.log.WriteText("OnSelChanged: %s\n" % self.tree.GetItemText(item))
            if wx.Platform == '__WXMSW__':
                self.log.WriteText("BoundingRect: %s\n" %
                                   self.tree.GetBoundingRect(item, True))
            self.tree.Expand(item)
            
        event.Skip()

    def UpdateItemChild(self,selected_item,directory_list):
        itemChildrenTextList=[]
        child,cookie=self.tree.GetFirstChild(selected_item)
        if child:
            itemChildrenTextList.append(self.tree.GetItemText(child))
            while (child.IsOk()):
                child,cookie=self.tree.GetNextChild(selected_item,cookie)
                if child:
                    itemChildrenTextList.append(self.tree.GetItemText(child))

        for directory_name in directory_list:
            if directory_name not in itemChildrenTextList:
                newItem=self.tree.AppendItem(selected_item,directory_name)
                self.tree.SetItemData(newItem, None)
                self.tree.SetItemImage(newItem, self.folderImage, wx.TreeItemIcon_Normal)

        self.tree.Expand(selected_item)

    def UpdateFileList(self, item):
        path = self.tree.GetItemText(item)
        if path != '/':
            path += '/'
        preItem = self.tree.GetItemParent(item)

        while (preItem.IsOk()):
            itemText = self.tree.GetItemText(preItem)
            if itemText != '/':
                itemText += '/'
            path = itemText + path
            preItem = self.tree.GetItemParent(preItem)

        self.parent.SetComboBoxText('请求中...')
        resultCode, resultContent = self.shellTools.getDirectoryContent(path)

        self.UpdateStatusUI(resultCode,resultContent,path)

        # 更新文件列表
        return self.parent.DafangFileListCtrl.UpdateDirectory(resultContent)
        
        


