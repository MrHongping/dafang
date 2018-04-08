# -*- coding: UTF-8 -*-
import  wx,sys

sys.path.append("..")
from utils import commonsUtil
import  wx.lib.mixins.listctrl  as  listmix

#----------------------------------------------------------------------

class FileList(wx.ListCtrl, listmix.ListCtrlAutoWidthMixin):
    def __init__(self, parent, ID, pos=wx.DefaultPosition,
                 size=wx.DefaultSize, style=0):
        wx.ListCtrl.__init__(self, parent, ID, pos, size, style)
        listmix.ListCtrlAutoWidthMixin.__init__(self)

class DafangFileList(wx.Panel):
    
    def __init__(self, parent, log):
        wx.Panel.__init__(self, parent, -1, style=wx.WANTS_CHARS)
        self.parent=parent
        self.log = log
        tID = wx.NewId()
        
        sizer = wx.BoxSizer(wx.VERTICAL)

        self.list = FileList(self, tID,
                                 style=wx.LC_REPORT 
                                 | wx.BORDER_NONE
                                 | wx.LC_EDIT_LABELS
                                 )
        
        self.il = wx.ImageList(16, 16)
        self.fldridx  = self.il.Add(wx.ArtProvider.GetBitmap(wx.ART_FOLDER,      wx.ART_OTHER, (16,16)))
        self.fileidx  = self.il.Add(wx.ArtProvider.GetBitmap(wx.ART_NORMAL_FILE,      wx.ART_OTHER, (16,16)))
        
        self.list.SetImageList(self.il, wx.IMAGE_LIST_SMALL)

        self.list.InsertColumn(0, u'名称')
        self.list.InsertColumn(1, u"时间")
        self.list.InsertColumn(2, u"大小")
        self.list.InsertColumn(3, u"属性")

        self.list.Bind(wx.EVT_LEFT_DCLICK, self.OnDoubleClick)
        self.Bind(wx.EVT_LIST_ITEM_SELECTED, self.OnItemSelected, self.list)

        sizer.Add(self.list, 1, wx.EXPAND)

        self.SetSizer(sizer)

        self.itemList=[]

    def UpdateDirectory(self,dirContent):
        self.list.DeleteAllItems()

        subDirectoryList=[]
        self.itemList = []
        
        if dirContent=='':
            return subDirectoryList

        if 'Error:' in dirContent:
            return subDirectoryList
          
        contentList=dirContent.split('\n')
        
        for content in contentList:
            contentElements=content.split('\t')

            if len(contentElements)<3:
                continue

            itemName=contentElements[0]
            createTime=contentElements[1]
            fileSize=contentElements[2]
            accessPermission=contentElements[3]

            self.itemList.append(itemName)

            elementParams=''
            for i in range(4,len(contentElements)):
                elementParams+=' '+contentElements[i]
                
            directoryFlag=commonsUtil.isDirectory(itemName)

            if directoryFlag:
                directoryName=itemName[:len(itemName)-1]
                subDirectoryList.append(directoryName)
                index=self.list.InsertItem(self.list.GetItemCount(),directoryName,self.fldridx)
            else:
                index=self.list.InsertItem(self.list.GetItemCount(),itemName,self.fileidx)

            self.list.SetItem(index, 1, createTime)
            self.list.SetItem(index, 2, fileSize)
            self.list.SetItem(index, 3, accessPermission)

        #设置文件列表属性的宽度
        self.list.SetColumnWidth(0, wx.LIST_AUTOSIZE)
        self.list.SetColumnWidth(1, wx.LIST_AUTOSIZE)
        self.list.SetColumnWidth(2, wx.LIST_AUTOSIZE)
        self.list.SetColumnWidth(3, wx.LIST_AUTOSIZE)

        return subDirectoryList


    def OnDoubleClick(self, event):
        itemName=self.itemList[self.currentItem]
        if commonsUtil.isDirectory(itemName):
            self.parent.DafangFileTreeCtrl.ClickItemByName(itemName)
        else:
            self.parent.OpenNewFileEditor(itemName)
        event.Skip()

    def OnItemSelected(self, event):
        self.currentItem = event.Index

    def OnSize(self, evt):
        self.tree.SetSize(self.GetSize())


