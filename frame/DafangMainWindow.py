# coding=utf-8

"""
@version: 1.0
@author: chaowei
@file: DafangMainWindow.py
@time: 2018/4/2 16:55
"""
import wx, wx.aui, sys

sys.path.append("..")
import ShellListCtrl
import FileManagerCtrl
import FileEditorCtrl


class MainWindow(wx.Panel):
    def __init__(self, parent, log):
        self.log = log
        wx.Panel.__init__(self, parent, -1)

        self.nb = wx.aui.AuiNotebook(self)

        win = ShellListCtrl.ShellList(self, log)
        self.nb.AddPage(win, 'Shell')

        sizer = wx.BoxSizer()
        sizer.Add(self.nb, 1, wx.EXPAND)
        self.SetSizer(sizer)
        wx.CallAfter(self.nb.SendSizeEvent)

    def OpenFileTree(self, shellEntity):
        win = FileManagerCtrl.FileManager(self, self.log, shellEntity)
        index = self.nb.AddPage(win, shellEntity.shell_host)
        self.nb.ChangeSelection(self.nb.GetPageCount() - 1)

    def OpenFileEditor(self, fileName, fileContent):
        win = FileEditorCtrl.FileEditor(self, self.log, fileContent)
        index = self.nb.AddPage(win, fileName)
        print index
        self.nb.ChangeSelection(self.nb.GetPageCount() - 1)

def runTest(frame, nb, log):
    win = MainWindow(nb, log)
    return win


if __name__ == '__main__':
    import sys, os
    import run
    run.main(['', os.path.basename(sys.argv[0])] + sys.argv[1:])