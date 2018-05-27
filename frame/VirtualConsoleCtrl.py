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
from WorkThread import HttpRequestThread

class VirtualConsole(wx.Panel):

    def __init__(self, parent,shellEntity, log):

        self.parent=parent
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
        self.histortCommandPointer=-1
        self.charCount=0
        self.currentPath=''
        self.commandZ1=''
        self.commandZ2=''

    def OnInit(self):
        HttpRequestThread(config.TASK_GET_START, shellEntity=self.shellEntity, callBack=self.CallBack_getStart,
                          statusCallback=self.parent.SetStatus).start()

    def CallBack_getStart(self, resultCode, resultContent):

        if resultCode:

            if resultContent.startswith('/'):

                self.currentPath = resultContent.split('\t')[0]
                if self.shellEntity.shell_script_type == 'JSP':
                    self.commandZ1='-c/bin/sh'
                else:
                    self.commandZ1 = '/bin/sh'
                self.commandZ2='{0};{1};echo [S];pwd;echo [E]'

            else:
                inforList=resultContent.split('\t')
                self.currentPath,disks=inforList[0],inforList[1]
                if self.shellEntity.shell_script_type=='JSP':
                    self.commandZ1 = '/ccmd'
                else:
                    self.commandZ1='cmd'
                self.commandZ2 = 'cd /d {0}&{1}&echo [S]&cd&echo [E]'

            terminalPath=config.TERMINAL_PATH_TEMPLATE.format(self.currentPath.strip())
            self.ed.AppendText(terminalPath)
            self.charCount+=len(terminalPath.decode('utf-8'))

    def OnKeyDown(self,event):
        key = event.GetKeyCode()
        if key==wx.WXK_UP:

            if self.histortCommandPointer < len(self.history)-1:
                self.histortCommandPointer += 1

                self.ed.Remove(self.charCount, len(self.ed.GetValue().decode('utf-8'))+self.ed.GetNumberOfLines())

                self.ed.AppendText(self.history[self.histortCommandPointer])


        elif key==wx.WXK_DOWN:

            if self.histortCommandPointer>0:

                self.histortCommandPointer -= 1

                self.ed.Remove(self.charCount, len(self.ed.GetValue().decode('utf-8'))+self.ed.GetNumberOfLines())

                self.ed.AppendText(self.history[self.histortCommandPointer])


        elif key==wx.WXK_BACK:
            index=self.ed.GetInsertionPoint()
            if index>self.charCount:
                self.ed.Remove(index-1,index)
        elif key==wx.WXK_RETURN:#回车

            lineText=self.ed.GetLineText(self.ed.GetNumberOfLines()-1)

            self.ed.AppendText('\r\n')
            self.charCount += len('\r\n'.decode('utf-8'))

            self.inputCommand=lineText.replace(config.TERMINAL_PATH_TEMPLATE.format(self.currentPath.strip()),'')

            if self.inputCommand:

                self.charCount += len(self.inputCommand.decode('utf-8'))

                HttpRequestThread(config.TASK_EXCUTE_COMMAND,path=self.currentPath,shellEntity=self.shellEntity,commandZ1=self.commandZ1,commandZ2=self.commandZ2.format(self.currentPath,self.inputCommand),command=self.inputCommand,callBack=self.Callback_excuteCommand,statusCallback=self.parent.SetStatus).start()

        elif key==ord('X'):
            if event.ControlDown():
                pass
            else:
                event.Skip()
        else:
            event.Skip()

    def Callback_excuteCommand(self,resultCode, resultContent):
        if resultCode:

            self.history.insert(0, self.inputCommand)

            self.histortCommandPointer = -1

            commandResult, tmp = resultContent.split('[S]')

            self.ed.AppendText(commandResult)

            self.charCount += len(commandResult.decode('utf-8'))

            currentPath, error = tmp.split('[E]')

            self.currentPath = currentPath.strip()

            if error:
                error+='\r\n'
                self.ed.AppendText(error)
                self.charCount += len(error.decode('utf-8'))

        terminalPath = config.TERMINAL_PATH_TEMPLATE.format(self.currentPath.strip())
        self.ed.AppendText(terminalPath)
        self.charCount += len(terminalPath.decode('utf-8'))