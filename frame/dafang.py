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
        wx.Log.SetActiveTarget(wx.LogStderr())

        self.log=Log()

        self.SetAssertMode(wx.APP_ASSERT_DIALOG)

        frame = wx.Frame(None, -1, u"大方——网站管理工具",style=wx.DEFAULT_FRAME_STYLE, name="")
        self.statusbar = frame.CreateStatusBar()

        self.statusbar.SetFieldsCount(2)
        self.statusbar.SetStatusWidths([-1,-1])
        self.SetTunnelStatusText('0')
        self.statusbar.SetStatusText("白帽磊落，神器大方", 0)

        frame.Maximize(True)
        frame.Show(True)

        win = MainWindow(frame,self,self.log)

        if win:
            win.SetFocus()
            self.window = win
        else:
            frame.Destroy()
            return True

        self.SetTopWindow(frame)
        self.frame = frame


        return True

    def OnExitApp(self, evt):
        self.frame.Close(True)

    def SetRequestStatusText(self,text):
        self.statusbar.SetStatusText("状态：{0}".format(text), 0)

    def SetTunnelStatusText(self,text):
        self.statusbar.SetStatusText("内网通道数：{0}".format(text), 1)

if __name__ == '__main__':
    app = MainApp()
    app.MainLoop()