# coding=utf-8

"""
@version: 1.0
@author: chaowei
@file: FileManagerCtrl.py
@time: 2018/4/2 16:55
"""
import wx,sys

sys.path.append("..")
import DafangFileTreeCtrl
import DafangFileListCtrl
from utils.entity import shell_entity
from utils.shell import ShellTools

class FileManager(wx.Panel):

    def __init__(self,parent,log,shellEntity):
        wx.Panel.__init__(self, parent, -1, wx.DefaultPosition, wx.DefaultSize)

        self.shellEntity=shellEntity
        self.parent=parent
        self.log=log

        bSizer1 = wx.BoxSizer(wx.VERTICAL)

        bSizer2 = wx.BoxSizer(wx.HORIZONTAL)

        comboBoxDirectoryPathChoices = []
        self.comboBoxDirectoryPath = wx.ComboBox(self, wx.ID_ANY, u"Combo!", wx.DefaultPosition, wx.DefaultSize,
                                                 comboBoxDirectoryPathChoices, 0)

        bSizer2.Add(self.comboBoxDirectoryPath, 1, wx.ALL, 5)

        self.buttonRequest = wx.Button(self, wx.ID_ANY, u"读取", wx.DefaultPosition, wx.DefaultSize, 0)
        bSizer2.Add(self.buttonRequest, 0, wx.ALL, 5)

        bSizer1.Add(bSizer2, 0, wx.EXPAND, 5)

        bSizer3 = wx.BoxSizer(wx.HORIZONTAL)

        self.DafangFileTreeCtrl = DafangFileTreeCtrl.DafangFileTree(self, log, shellEntity)
        bSizer3.Add(self.DafangFileTreeCtrl, 1, wx.ALL | wx.EXPAND, 3)

        self.DafangFileListCtrl = DafangFileListCtrl.DafangFileList(self, log)
        bSizer3.Add(self.DafangFileListCtrl, 2, wx.ALL | wx.EXPAND, 3)

        bSizer1.Add(bSizer3, 1, wx.EXPAND, 5)

        self.SetSizer(bSizer1)
        
        # vsizer1 = wx.BoxSizer(orient=wx.HORIZONTAL)
        #

        #
        # self.DafangFileListCtrl=DafangFileListCtrl.DafangFileList(self,log)
        #
        # self.DafangFileTreeCtrl=DafangFileTreeCtrl.DafangFileTree(self, log, shellEntity)
        #
        # vsizer1.Add(self.DafangFileTreeCtrl, 1, wx.EXPAND,-1)
        # vsizer1.Add(self.DafangFileListCtrl, 3, wx.EXPAND,-1)
        #
        # # wx.ALIGN_LEFT, wx.ALIGN_RIGHT
        # self.SetSizer(vsizer1)

    def OpenNewFileEditor(self,fileName):
        path=self.DafangFileTreeCtrl.getSelectedItemPath()
        fileContent=ShellTools.getShellTools(self.shellEntity).getFileContent(path+'/'+fileName)
        self.parent.OpenFileEditor(fileName,fileContent)

    def SetRequestStatusText(self,text):
        self.parent.SetRequestStatusText(text)

    def SetHostSelectedStatusText(self,text):
        self.parent.SetRequestStatusText(text)

    def SetTunnelStatusText(self,text):
        self.parent.SetRequestStatusText(text)