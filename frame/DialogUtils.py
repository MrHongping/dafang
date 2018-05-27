# coding=utf-8

"""
@version: 1.0
@author: chaowei
@file: Dialog.py
@time: 2018/4/2 22:10
"""
import wx,sys,datetime

import xml.dom.minidom as xmldom

sys.path.append("..")

from utils import config
from utils.dbHelper import DatabaseHelper
from utils.entity import *

class ShellManageDialog(wx.Dialog):
    def __init__(
            self, parent, id, title, size=wx.DefaultSize, pos=wx.DefaultPosition,
            style=wx.DEFAULT_DIALOG_STYLE, name='dialog',shellEntity=None
            ):
        wx.Dialog.__init__(self, parent, id=wx.ID_ANY, title=title, pos=wx.DefaultPosition,
                           size=wx.DefaultSize, style=wx.DEFAULT_DIALOG_STYLE)

        self.SetSizeHints(wx.DefaultSize, wx.DefaultSize)

        shellInforSizer = wx.BoxSizer(wx.VERTICAL)

        shellAddressBoxSizer = wx.BoxSizer(wx.HORIZONTAL)

        self.m_staticText1 = wx.StaticText(self, wx.ID_ANY, u"地   址：", wx.DefaultPosition,
                                           wx.DefaultSize, 0)
        self.m_staticText1.Wrap(-1)
        shellAddressBoxSizer.Add(self.m_staticText1, 0, wx.ALIGN_CENTER_VERTICAL | wx.ALL, 5)

        self.textCtrlShellAddress = wx.TextCtrl(self, wx.ID_ANY, wx.EmptyString,
                                                wx.DefaultPosition, wx.Size(400, -1), 0)
        shellAddressBoxSizer.Add(self.textCtrlShellAddress, 0, wx.ALL, 5)

        self.textCtrlShellPassword = wx.TextCtrl(self, wx.ID_ANY, wx.EmptyString,
                                                 wx.DefaultPosition, wx.Size(90, -1), 0)
        shellAddressBoxSizer.Add(self.textCtrlShellPassword, 0, wx.ALL, 5)

        shellInforSizer.Add(shellAddressBoxSizer, 1, wx.TOP, 5)

        shellDatabaseBoxSizer = wx.BoxSizer(wx.HORIZONTAL)

        self.m_staticText2 = wx.StaticText(self, wx.ID_ANY, u"数据库：", wx.DefaultPosition,
                                           wx.DefaultSize, 0)
        self.m_staticText2.Wrap(80)
        shellDatabaseBoxSizer.Add(self.m_staticText2, 0, wx.ALL, 5)

        self.textCtrlShellDatabase = wx.TextCtrl(self, wx.ID_ANY, wx.EmptyString,
                                                 wx.DefaultPosition, wx.Size(500, 100), wx.TE_MULTILINE)
        shellDatabaseBoxSizer.Add(self.textCtrlShellDatabase, 0, wx.BOTTOM | wx.RIGHT | wx.LEFT, 5)

        shellInforSizer.Add(shellDatabaseBoxSizer, 0, wx.TOP, 5)

        shellRemarkBoxSzier = wx.BoxSizer(wx.HORIZONTAL)

        self.m_staticText3 = wx.StaticText(self, wx.ID_ANY, u"备   注：", wx.DefaultPosition,
                                           wx.DefaultSize, 0)
        self.m_staticText3.Wrap(-1)
        shellRemarkBoxSzier.Add(self.m_staticText3, 0, wx.ALIGN_CENTER_VERTICAL | wx.ALL, 5)

        self.textCtrlRemark = wx.TextCtrl(self, wx.ID_ANY, wx.EmptyString, wx.DefaultPosition,
                                          wx.Size(400, -1), 0)
        shellRemarkBoxSzier.Add(self.textCtrlRemark, 0, wx.ALL, 5)

        shellInforSizer.Add(shellRemarkBoxSzier, 0, 0, 5)

        shellTypeBoxSizer = wx.BoxSizer(wx.HORIZONTAL)

        self.m_staticText8 = wx.StaticText(self, wx.ID_ANY, u"类   型：", wx.DefaultPosition,
                                           wx.DefaultSize, 0)
        self.m_staticText8.Wrap(-1)
        shellTypeBoxSizer.Add(self.m_staticText8, 0, wx.ALIGN_CENTER_VERTICAL | wx.ALL, 5)

        self.comboBoxShellScriptType = wx.ComboBox(self, wx.ID_ANY, u"脚本类型",
                                                   wx.DefaultPosition, wx.Size(100, -1), config.SHELL_SCRIPT_LIST,
                                                   0)
        shellTypeBoxSizer.Add(self.comboBoxShellScriptType, 0, wx.ALL, 5)

        self.comboBoxShellEncodeType = wx.ComboBox(self, wx.ID_ANY, u"编码类型",
                                                   wx.DefaultPosition, wx.Size(100, -1), config.SHELL_ENCODE_LIST,
                                                   0)
        shellTypeBoxSizer.Add(self.comboBoxShellEncodeType, 0, wx.ALL, 5)

        shellInforSizer.Add(shellTypeBoxSizer, 1, wx.EXPAND, 5)

        saveDataBaseBtn = wx.BoxSizer(wx.HORIZONTAL)

        if shellEntity:
            self.textCtrlShellAddress.SetValue(shellEntity.shell_address)
            self.textCtrlShellPassword.SetValue(shellEntity.shell_password)
            self.textCtrlShellDatabase.SetValue(shellEntity.database_info)
            self.textCtrlRemark.SetValue(shellEntity.shell_remark)
            self.comboBoxShellScriptType.SetValue(shellEntity.shell_script_type)
            self.comboBoxShellEncodeType.SetValue(shellEntity.shell_encode_type)

            self.saveDataBaseBtnOK = wx.Button(self, -1, label='修改')
            self.saveDataBaseBtnOK.Bind(wx.EVT_BUTTON, self.OnUpdateBtnClick)
            self.shellID=shellEntity.shell_id
        else:
            self.saveDataBaseBtnOK = wx.Button(self, -1, label='保存')
            self.saveDataBaseBtnOK.Bind(wx.EVT_BUTTON, self.OnSaveBtnClick)
            self.httpSettingDefault = True
            self.tunnelSettingDefault = True

        saveDataBaseBtn.Add(self.saveDataBaseBtnOK, 0, wx.ALIGN_CENTER_VERTICAL | wx.ALL, 5)
        self.saveDataBaseBtnCancel = wx.Button(self, -1, label='退出')
        saveDataBaseBtn.Add(self.saveDataBaseBtnCancel, 0, wx.ALIGN_CENTER_VERTICAL | wx.ALL, 5)

        self.m_staticline1 = wx.StaticLine(self, wx.ID_ANY, wx.DefaultPosition, wx.DefaultSize, wx.LI_HORIZONTAL)
        shellInforSizer.Add(self.m_staticline1, 0, wx.EXPAND | wx.ALL, 5)

        shellInforSizer.Add(saveDataBaseBtn,1, wx.ALIGN_RIGHT, 5)

        self.SetSizer(shellInforSizer)
        self.Layout()
        shellInforSizer.Fit(self)

        self.Centre(wx.BOTH)

        # Connect Events
        self.saveDataBaseBtnCancel.Bind(wx.EVT_BUTTON, self.OnCancelBtnClick)
        self.textCtrlShellAddress.Bind(wx.EVT_TEXT,self.OnShellAddressChange)

        self.saveDataBaseBtnOK.SetFocus()

    def GetSettingResult(self):
        shell_address = self.textCtrlShellAddress.GetValue()

        if not shell_address:
            wx.MessageBox('Shell地址不能为空')
            return

        shell_password = self.textCtrlShellPassword.GetValue()

        if not shell_password:
            wx.MessageBox('Shell密码不能为空')
            return

        shell_script_type = self.comboBoxShellScriptType.GetValue()
        if shell_script_type not in config.SHELL_SCRIPT_LIST:
            shell_script_type='JSP'

        shell_encode_type = self.comboBoxShellEncodeType.GetValue()
        if shell_encode_type not in config.SHELL_ENCODE_LIST:
            shell_encode_type='UTF-8'

        database_info = self.textCtrlShellDatabase.GetValue()
        shell_remark = self.textCtrlRemark.GetValue()

        nowTime = datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S')

        return shell_entity(shell_address, shell_password, shell_script_type, shell_encode_type, database_info,
                                   shell_remark, nowTime)

    def OnSaveBtnClick(self, event):

        shellEntity=self.GetSettingResult()
        if not shellEntity:
            return

        DatabaseHelper.saveShellEntity(shellEntity)

        self.SetReturnCode(1)
        self.Destroy()
        event.Skip()

    def OnUpdateBtnClick(self, event):

        shellEntity = self.GetSettingResult()
        if not shellEntity:
            return
        DatabaseHelper.updateShellEntityByID(shellEntity,self.shellID)
        self.SetReturnCode(1)
        self.Destroy()
        event.Skip()

    def OnCancelBtnClick(self, event):
        self.Destroy()
        event.Skip()

    def OnShellAddressChange(self,event):
        shellAddress=event.GetString()
        if '.' in shellAddress:
            ss=shellAddress.split('.')
            suffix=ss[len(ss)-1]
            if 'jsp' in suffix.lower():
                self.comboBoxShellScriptType.SetValue('JSP')
            if 'php' in suffix.lower():
                self.comboBoxShellScriptType.SetValue('PHP')

class TunnelSettingDialog(wx.Dialog):
    def __init__(self, parent,title,shellEntity):
        wx.Dialog.__init__(self, parent, id=wx.ID_ANY, title=title, pos=wx.DefaultPosition,
                           size=wx.DefaultSize, style=wx.DEFAULT_DIALOG_STYLE)

        self.shellEntity=shellEntity

        self.SetSizeHints(wx.DefaultSize, wx.DefaultSize)

        bSizer1 = wx.BoxSizer(wx.VERTICAL)

        bSizer2 = wx.BoxSizer(wx.HORIZONTAL)

        self.m_staticText1 = wx.StaticText(self, wx.ID_ANY, u"侦听端口：", wx.DefaultPosition, wx.DefaultSize, 0)
        self.m_staticText1.Wrap(-1)
        bSizer2.Add(self.m_staticText1, 0, wx.ALL, 5)

        self.textCtrlListenPort = wx.TextCtrl(self, wx.ID_ANY, wx.EmptyString, wx.DefaultPosition, wx.DefaultSize, 0)
        bSizer2.Add(self.textCtrlListenPort, 0, wx.ALL, 5)

        bSizer1.Add(bSizer2, 1, wx.EXPAND, 5)

        bSizer3 = wx.BoxSizer(wx.HORIZONTAL)

        self.m_staticText2 = wx.StaticText(self, wx.ID_ANY, u"侦听地址：", wx.DefaultPosition, wx.DefaultSize, 0)
        self.m_staticText2.Wrap(-1)
        bSizer3.Add(self.m_staticText2, 0, wx.ALL, 5)

        self.comboBoxListenIP = wx.ComboBox(self, wx.ID_ANY, u"选择地址", wx.DefaultPosition, wx.DefaultSize,
                                            config.TUNNEL_LISTEN_IP_LIST, 0)
        bSizer3.Add(self.comboBoxListenIP, 0, wx.ALL, 5)

        bSizer1.Add(bSizer3, 1, wx.EXPAND, 5)

        bSizer4 = wx.BoxSizer(wx.HORIZONTAL)

        self.buttonStartSocks = wx.Button(self, wx.ID_ANY, u"开启", wx.DefaultPosition, wx.DefaultSize, 0)
        bSizer4.Add(self.buttonStartSocks, 0, wx.ALL, 5)

        self.buttonCancel = wx.Button(self, wx.ID_ANY, u"退出", wx.DefaultPosition, wx.DefaultSize, 0)
        bSizer4.Add(self.buttonCancel, 0, wx.ALL, 5)

        self.m_staticline1 = wx.StaticLine(self, wx.ID_ANY, wx.DefaultPosition, wx.DefaultSize, wx.LI_HORIZONTAL)
        bSizer1.Add(self.m_staticline1, 0, wx.EXPAND | wx.ALL, 5)

        bSizer1.Add(bSizer4, 1, wx.EXPAND, 5)

        self.SetSizer(bSizer1)
        self.Layout()
        bSizer1.Fit(self)

        self.Centre(wx.BOTH)

        # Connect Events
        self.buttonStartSocks.Bind(wx.EVT_BUTTON, self.OnStartBtnClick)
        self.buttonCancel.Bind(wx.EVT_BUTTON, self.OnCancelBtnClick)

    def __del__(self):
        pass

    def getSettingResult(self):
        tunnelPort = self.textCtrlListenPort.GetValue()
        if not tunnelPort:
            wx.MessageBox('内网代理侦听端口未设置')
            return

        tunnelIP = self.comboBoxListenIP.GetValue()
        if tunnelIP not in config.TUNNEL_LISTEN_IP_LIST:
            wx.MessageBox('内网代理侦听IP未设置')
            return

        return TunnelSettingEntity(tunnelPort, tunnelIP)

    # Virtual event handlers, overide them in your derived class
    def OnStartBtnClick(self, event):

        tunnelSettingEntity = self.getSettingResult()

        isSetted = DatabaseHelper.getTunnelSettingEntityByShellID(self.shellEntity.shellID)
        if isSetted:
            DatabaseHelper.updateTunnelSettingEntity(tunnelSettingEntity)
        else:
            DatabaseHelper.saveTunnelSettingEntity(tunnelSettingEntity)

        self.SetReturnCode(1)
        self.Destroy()
        event.Skip()

        event.Skip()

    def OnCancelBtnClick(self, event):
        event.Skip()


class HttpSettingDialog(wx.Dialog):
    def __init__(self, parent,title,shellEntity):
        wx.Dialog.__init__(self, parent, id=wx.ID_ANY, title=title, pos=wx.DefaultPosition,
                           size=wx.DefaultSize, style=wx.DEFAULT_DIALOG_STYLE)

        self.shellEntity = shellEntity

        self.SetSizeHints(wx.DefaultSize, wx.DefaultSize)

        bSizer5 = wx.BoxSizer(wx.VERTICAL)

        bSizer6 = wx.BoxSizer(wx.HORIZONTAL)

        self.m_staticText3 = wx.StaticText(self, wx.ID_ANY, u"UA示例：", wx.DefaultPosition, wx.DefaultSize, 0)
        self.m_staticText3.Wrap(-1)
        bSizer6.Add(self.m_staticText3, 0, wx.ALL, 5)

        self.comboBoxUserAgentExamples = wx.ComboBox(self, wx.ID_ANY, u"选择浏览器User-Agent", wx.DefaultPosition,
                                                     wx.Size(300, -1), config.USER_AGENT_LIST, 0)
        bSizer6.Add(self.comboBoxUserAgentExamples, 0, wx.ALL, 5)

        bSizer5.Add(bSizer6, 1, wx.EXPAND, 5)

        bSizer8 = wx.BoxSizer(wx.HORIZONTAL)

        self.m_staticText31 = wx.StaticText(self, wx.ID_ANY, u"UA配置：", wx.DefaultPosition, wx.DefaultSize, 0)
        self.m_staticText31.Wrap(-1)
        bSizer8.Add(self.m_staticText31, 0, wx.ALL, 5)

        self.textCtrlUserAgent = wx.TextCtrl(self, wx.ID_ANY, wx.EmptyString, wx.DefaultPosition, wx.Size(300, 50), wx.TE_MULTILINE)
        bSizer8.Add(self.textCtrlUserAgent, 0, wx.ALL, 5)

        bSizer5.Add(bSizer8, 0, wx.EXPAND, 5)

        bSizer7 = wx.BoxSizer(wx.HORIZONTAL)

        self.m_staticText4 = wx.StaticText(self, wx.ID_ANY, u"Cookie：", wx.DefaultPosition, wx.DefaultSize, 0)
        self.m_staticText4.Wrap(-1)
        bSizer7.Add(self.m_staticText4, 0, wx.ALL, 5)

        self.textCtrlCookie = wx.TextCtrl(self, wx.ID_ANY, wx.EmptyString, wx.DefaultPosition, wx.Size(300, 100),
                                          wx.TE_MULTILINE | wx.VSCROLL)
        bSizer7.Add(self.textCtrlCookie, 0, wx.ALL, 5)

        bSizer5.Add(bSizer7, 0, wx.EXPAND, 5)

        self.m_staticline1 = wx.StaticLine(self, wx.ID_ANY, wx.DefaultPosition, wx.DefaultSize, wx.LI_HORIZONTAL)
        bSizer5.Add(self.m_staticline1, 0, wx.EXPAND | wx.ALL, 5)

        bSizer9 = wx.BoxSizer(wx.HORIZONTAL)

        self.buttonSave = wx.Button(self, wx.ID_ANY, u"保存", wx.DefaultPosition, wx.DefaultSize, 0)
        bSizer9.Add(self.buttonSave, 0, wx.ALL | wx.ALIGN_CENTER_VERTICAL, 5)

        self.buttonCancel = wx.Button(self, wx.ID_ANY, u"退出", wx.DefaultPosition, wx.DefaultSize, 0)
        bSizer9.Add(self.buttonCancel, 0, wx.ALIGN_CENTER_VERTICAL | wx.RIGHT, 5)

        bSizer5.Add(bSizer9, 0, wx.ALIGN_CENTER_HORIZONTAL | wx.ALIGN_RIGHT, 5)

        self.SetSizer(bSizer5)
        self.Layout()
        bSizer5.Fit(self)

        self.Centre(wx.BOTH)

        # Connect Events
        self.buttonSave.Bind(wx.EVT_BUTTON, self.btnSaveClick)
        self.buttonCancel.Bind(wx.EVT_BUTTON, self.cancelBtnClick)

        self.Bind(wx.EVT_COMBOBOX, self.EvtComboBox, self.comboBoxUserAgentExamples)

        httpSettingEntity=DatabaseHelper.getHttpSettingEntityByShellID(self.shellEntity.shell_id)
        if httpSettingEntity:
            self.textCtrlUserAgent.SetValue(httpSettingEntity.user_agent)
            self.textCtrlCookie.SetValue(httpSettingEntity.cookie)

    def __del__(self):
        pass

    def EvtComboBox(self,evt):
        if evt.GetString() in config.USER_AGENT_LIST:
            self.textCtrlUserAgent.SetValue(evt.GetString())
        evt.Skip()

    def getSettingResult(self):
        userAgent = self.textCtrlUserAgent.GetValue()
        if not userAgent:
            wx.MessageBox('Http User-Agent未设置')
            return

        cookies = self.textCtrlCookie.GetValue()
        if not cookies:
            wx.MessageBox('Http Cookie未设置')
            return

        return HttpSettingEntity(cookies,userAgent, self.shellEntity.shell_id)

    def btnSaveClick(self, event):

        httpSettingEntity=self.getSettingResult()

        isSetted = DatabaseHelper.getHttpSettingEntityByShellID(self.shellEntity.shell_id)
        if isSetted:
            DatabaseHelper.updateHttpSettingEntity(httpSettingEntity)
        else:
            DatabaseHelper.saveHttpSettingEntity(httpSettingEntity)

        self.SetReturnCode(1)
        self.Destroy()
        event.Skip()

    def cancelBtnClick(self, event):
        self.Destroy()
        event.Skip()

class DatabaseSettingDialog(wx.Dialog):
    def __init__(self, parent,shellEntity):
        wx.Dialog.__init__(self, parent, id=wx.ID_ANY, title=u"数据库配置信息", pos=wx.DefaultPosition, size=wx.Size(1000, 500),
                           style=wx.DEFAULT_DIALOG_STYLE)

        self.SetSizeHints(wx.DefaultSize, wx.DefaultSize)
        self.shellEntity=shellEntity

        bSizer4 = wx.BoxSizer(wx.VERTICAL)

        bSizer5 = wx.BoxSizer(wx.HORIZONTAL)

        self.m_staticText1 = wx.StaticText(self, wx.ID_ANY, u"示例：", wx.DefaultPosition, wx.DefaultSize, 0)
        self.m_staticText1.Wrap(-1)
        bSizer5.Add(self.m_staticText1, 0, wx.ALL | wx.ALIGN_CENTER_VERTICAL, 5)

        comboBoxChoice=''
        if shellEntity.shell_script_type=='JSP':
            comboBoxChoice=config.DATABASE_SETTING_TEMPLATE_JSP
        if shellEntity.shell_script_type=='PHP':
            comboBoxChoice=config.DATABASE_SETTING_TEMPLATE_PHP
        self.comboBoxExamples = wx.ComboBox(self, wx.ID_ANY, u"选择数据库类型", wx.DefaultPosition, wx.DefaultSize,comboBoxChoice, 0)
        bSizer5.Add(self.comboBoxExamples, 1, wx.ALL | wx.ALIGN_CENTER_VERTICAL, 5)

        bSizer4.Add(bSizer5, 0, wx.EXPAND, 5)

        bSizer6 = wx.BoxSizer(wx.HORIZONTAL)

        self.m_staticText2 = wx.StaticText(self, wx.ID_ANY, u"配置：", wx.DefaultPosition, wx.DefaultSize, 0)
        self.m_staticText2.Wrap(-1)
        bSizer6.Add(self.m_staticText2, 0, wx.ALL, 5)

        self.textCtrlDatabaseSetting = wx.TextCtrl(self, wx.ID_ANY, wx.EmptyString, wx.DefaultPosition, wx.DefaultSize,
                                                   wx.TE_MULTILINE)
        bSizer6.Add(self.textCtrlDatabaseSetting, 1, wx.ALL | wx.EXPAND, 5)

        bSizer4.Add(bSizer6, 1, wx.EXPAND, 5)

        bSizer7 = wx.BoxSizer(wx.VERTICAL)

        self.buttonUpdate = wx.Button(self, wx.ID_ANY, u"提交", wx.DefaultPosition, wx.Size(940, -1), 0)
        bSizer7.Add(self.buttonUpdate, 0, wx.ALL | wx.ALIGN_RIGHT, 5)

        bSizer4.Add(bSizer7, 0, wx.EXPAND, 5)

        self.SetSizer(bSizer4)
        self.Layout()

        self.Centre(wx.BOTH)

        self.Bind(wx.EVT_COMBOBOX, self.EvtComboBox, self.comboBoxExamples)

        self.buttonUpdate.Bind(wx.EVT_BUTTON, self.OnButtonUpdateClick)

    def EvtComboBox(self,event):
        if event.GetString():
            self.textCtrlDatabaseSetting.SetValue(event.GetString())
        event.Skip()

    def OnButtonUpdateClick(self,event):
        self.shellEntity.database_info=self.textCtrlDatabaseSetting.GetValue()
        DatabaseHelper.updateShellEntityByID(self.shellEntity,self.shellEntity.shell_id)

        self.SetReturnCode(1)
        self.Destroy()
        event.Skip()

    def __del__(self):
        pass


