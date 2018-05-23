# coding=utf-8

"""
@version: 1.0
@author: chaowei
@file: dafang.py
@time: 2018/4/14 11:56
"""
import wx
import sys

reload(sys)

sys.setdefaultencoding( "utf-8" )

from MainWindowCtrl import MainWindow

class Log:
    def WriteText(self, text):
        if text[-1:] == '\n':
            text = text[:-1]
        wx.LogMessage(text)
    write = WriteText

class MainApp(wx.App):
    def __init__(self):
        wx.App.__init__(self, redirect=False)

    def OnInit(self):

        self.log=Log()

        self.SetAssertMode(wx.APP_ASSERT_DIALOG)

        self.frame = MainWindow(self,self.log,'大方——网站管理工具')

        self.statusbar = self.frame.CreateStatusBar()

        self.statusbar.SetFieldsCount(2)

        self.statusbar.SetStatusWidths([-1,-1])

        self.statusbar.SetStatusText("白帽磊落，神器大方", 0)

        self.statusbar.SetStatusText("仅供学习研究，请勿用于他途，否则。。。", 1)

        self.frame.Show(True)

        return True

if __name__ == '__main__':
    app = MainApp()
    app.MainLoop()