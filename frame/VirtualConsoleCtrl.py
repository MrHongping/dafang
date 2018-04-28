# coding=utf-8

"""
@version: 1.0
@author: chaowei
@file: VirtualConsoleCtrl.py
@time: 2018/4/8 23:14
"""
import  wx,sys
sys.path.append("..")

from utils import config
from utils.shell import ShellTools

class VirtualConsole(wx.Panel):

    def __init__(self, parent,shellEntity, log):
        self.log = log
        self.shellEntity = shellEntity
        self.shellTools = ShellTools.getShellTools(self.shellEntity)
        wx.Panel.__init__(self, parent, -1)

        self.ed = wx.TextCtrl( self, wx.ID_ANY, wx.EmptyString, wx.DefaultPosition, wx.DefaultSize, wx.TE_MULTILINE)
        box = wx.BoxSizer(wx.VERTICAL)
        box.Add(self.ed, 1, wx.ALL | wx.GROW, 1)
        self.SetSizer(box)
        self.ed.SetBackgroundColour(wx.BLACK )
        self.ed.SetForegroundColour(wx.GREEN)
        self.ed.Bind(wx.EVT_KEY_DOWN,self.OnKeyDown)
        self.ed.SetInsertionPointEnd()

        self.history=[]
        self.charCount=0
        self.currentPath=''
        self.OnInit()

    def OnInit(self):
        code,currentPath=self.shellTools.getStart()
        if code:
            self.currentPath=currentPath
            terminalPath=config.TERMINAL_PATH_TEMPLATE.format(str(currentPath.strip()))
            self.ed.AppendText(terminalPath)
            self.charCount+=len(terminalPath.decode('utf-8'))

    def OnKeyDown(self,event):
        key = event.GetKeyCode()
        if key==wx.WXK_UP:
            print 'UP'
        elif key==wx.WXK_DOWN:
            pass
        elif key==wx.WXK_BACK:
            index=self.ed.GetInsertionPoint()
            if index>self.charCount:
                self.ed.Remove(index-1,index)
        elif key==wx.WXK_RETURN:#回车
            self.ed.GetLineText(self.ed.GetNumberOfLines())
            self.ed.AppendText('\n')
            self.charCount += len('\n'.decode('utf-8'))
            code,result=self.shellTools.excuteCommand(self.currentPath,'ifconfig')
            if code:
                commandResult,tmp=result.split('[S]')
                self.ed.AppendText(commandResult)
                self.charCount+=len(commandResult.decode('utf-8'))
                self.currentPath,error=tmp.split('[E]')
                if error:
                    self.ed.AppendText(error)
                    self.charCount += len(error.decode('utf-8'))
                terminalPath = config.TERMINAL_PATH_TEMPLATE.format(str(self.currentPath.strip()))
                self.ed.AppendText(terminalPath)
                self.charCount += len(terminalPath.decode('utf-8'))
        else:
            event.Skip()