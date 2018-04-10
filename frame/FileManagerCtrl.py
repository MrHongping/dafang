import wx,sys

sys.path.append("..")
import DafangFileTreeCtrl
import DafangFileListCtrl
from utils.entity import shell_entity
from utils.shell import ShellTools

class FileManager(wx.Panel):

    def __init__(self,parent,log,shellEntity):
        wx.Panel.__init__(self, parent, -1, wx.DefaultPosition, wx.DefaultSize)  
        
        vsizer1 = wx.BoxSizer(orient=wx.HORIZONTAL)  

        self.shellEntity=shellEntity
        self.parent=parent
        self.log=log  
        
        self.DafangFileListCtrl=DafangFileListCtrl.DafangFileList(self,log)

        self.DafangFileTreeCtrl=DafangFileTreeCtrl.DafangFileTree(self, log, shellEntity)

        vsizer1.Add(self.DafangFileTreeCtrl, 1, wx.EXPAND | wx.LEFT,5)
        vsizer1.Add(self.DafangFileListCtrl, 3, wx.EXPAND | wx.RIGHT,20)
        
        # wx.ALIGN_LEFT, wx.ALIGN_RIGHT  
        self.SetSizer(vsizer1)

    def OpenNewFileEditor(self,fileName):
        path=self.DafangFileTreeCtrl.getSelectedItemPath()
        fileContent=ShellTools.getShellTools(self.shellEntity).getFileContent(path+'/'+fileName)
        self.parent.OpenFileEditor(fileName,fileContent)