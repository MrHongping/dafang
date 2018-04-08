# coding=utf-8

"""
@version: 1.0
@author: chaowei
@file: Dialog.py
@time: 2018/4/2 22:10
"""
import wx,sys,datetime

sys.path.append("..")

from utils.dbHelper import DatabaseHelper
from utils.entity import shell_entity

class ShellManageDialog(wx.Dialog):
    def __init__(
            self, parent, id, title, size=wx.DefaultSize, pos=wx.DefaultPosition,
            style=wx.DEFAULT_DIALOG_STYLE, name='dialog'
            ):
        wx.Dialog.__init__(self, parent, id=wx.ID_ANY, title=wx.EmptyString, pos=wx.DefaultPosition,
                           size=wx.DefaultSize, style=wx.DEFAULT_DIALOG_STYLE)

        self.SetSizeHints(wx.DefaultSize, wx.DefaultSize)

        DialogMainSizer = wx.BoxSizer(wx.VERTICAL)

        shellInforSizer = wx.StaticBoxSizer(wx.StaticBox(self, wx.ID_ANY, u"Shell信息"), wx.VERTICAL)

        shellAddressBoxSizer = wx.BoxSizer(wx.HORIZONTAL)

        self.m_staticText1 = wx.StaticText(shellInforSizer.GetStaticBox(), wx.ID_ANY, u"地   址：", wx.DefaultPosition,
                                           wx.DefaultSize, 0)
        self.m_staticText1.Wrap(-1)
        shellAddressBoxSizer.Add(self.m_staticText1, 0, wx.ALIGN_CENTER_VERTICAL | wx.ALL, 5)

        self.textCtrlShellAddress = wx.TextCtrl(shellInforSizer.GetStaticBox(), wx.ID_ANY, wx.EmptyString,
                                                wx.DefaultPosition, wx.Size(300, -1), 0)
        shellAddressBoxSizer.Add(self.textCtrlShellAddress, 0, wx.ALL, 5)

        self.textCtrlShellPassword = wx.TextCtrl(shellInforSizer.GetStaticBox(), wx.ID_ANY, wx.EmptyString,
                                                 wx.DefaultPosition, wx.Size(90, -1), 0)
        shellAddressBoxSizer.Add(self.textCtrlShellPassword, 0, wx.ALL, 5)

        shellInforSizer.Add(shellAddressBoxSizer, 1, 0, 5)

        shellDatabaseBoxSizer = wx.BoxSizer(wx.HORIZONTAL)

        self.m_staticText2 = wx.StaticText(shellInforSizer.GetStaticBox(), wx.ID_ANY, u"数据库：", wx.DefaultPosition,
                                           wx.DefaultSize, 0)
        self.m_staticText2.Wrap(80)
        shellDatabaseBoxSizer.Add(self.m_staticText2, 0, wx.ALL, 5)

        self.textCtrlShellDatabase = wx.TextCtrl(shellInforSizer.GetStaticBox(), wx.ID_ANY, wx.EmptyString,
                                                 wx.DefaultPosition, wx.Size(400, 80), 0)
        shellDatabaseBoxSizer.Add(self.textCtrlShellDatabase, 0, wx.BOTTOM | wx.RIGHT | wx.LEFT, 5)

        shellInforSizer.Add(shellDatabaseBoxSizer, 0, wx.TOP, 5)

        shellRemarkBoxSzier = wx.BoxSizer(wx.HORIZONTAL)

        self.m_staticText3 = wx.StaticText(shellInforSizer.GetStaticBox(), wx.ID_ANY, u"备   注：", wx.DefaultPosition,
                                           wx.DefaultSize, 0)
        self.m_staticText3.Wrap(-1)
        shellRemarkBoxSzier.Add(self.m_staticText3, 0, wx.ALIGN_CENTER_VERTICAL | wx.ALL, 5)

        self.textCtrlRemark = wx.TextCtrl(shellInforSizer.GetStaticBox(), wx.ID_ANY, wx.EmptyString, wx.DefaultPosition,
                                          wx.Size(400, -1), 0)
        shellRemarkBoxSzier.Add(self.textCtrlRemark, 0, wx.ALL, 5)

        shellInforSizer.Add(shellRemarkBoxSzier, 0, 0, 5)

        shellTypeBoxSizer = wx.BoxSizer(wx.HORIZONTAL)

        self.m_staticText8 = wx.StaticText(shellInforSizer.GetStaticBox(), wx.ID_ANY, u"类   型：", wx.DefaultPosition,
                                           wx.DefaultSize, 0)
        self.m_staticText8.Wrap(-1)
        shellTypeBoxSizer.Add(self.m_staticText8, 0, wx.ALIGN_CENTER_VERTICAL | wx.ALL, 5)

        comboBoxShellScriptTypeChoices = [u"PHP", u"JSP"]
        self.comboBoxShellScriptType = wx.ComboBox(shellInforSizer.GetStaticBox(), wx.ID_ANY, u"脚本类型",
                                                   wx.DefaultPosition, wx.Size(100, -1), comboBoxShellScriptTypeChoices,
                                                   0)
        shellTypeBoxSizer.Add(self.comboBoxShellScriptType, 0, wx.ALL, 5)

        comboBoxShellEncodeTypeChoices = [u"UTF-8", u"GB2312"]
        self.comboBoxShellEncodeType = wx.ComboBox(shellInforSizer.GetStaticBox(), wx.ID_ANY, u"编码类型",
                                                   wx.DefaultPosition, wx.Size(100, -1), comboBoxShellEncodeTypeChoices,
                                                   0)
        shellTypeBoxSizer.Add(self.comboBoxShellEncodeType, 0, wx.ALL, 5)

        shellInforSizer.Add(shellTypeBoxSizer, 1, wx.EXPAND, 5)

        DialogMainSizer.Add(shellInforSizer, 0, wx.ALL, 5)

        httpInforSizer = wx.StaticBoxSizer(wx.StaticBox(self, wx.ID_ANY, u"Http请求设置"), wx.VERTICAL)

        self.httpDefaultcheckBox2 = wx.CheckBox(httpInforSizer.GetStaticBox(), wx.ID_ANY, u"使用默认设置", wx.DefaultPosition,
                                                wx.DefaultSize, 0)
        self.httpDefaultcheckBox2.SetValue(True)
        httpInforSizer.Add(self.httpDefaultcheckBox2, 0, wx.ALL, 5)

        httpUABoxSizer = wx.BoxSizer(wx.HORIZONTAL)

        self.m_staticText4 = wx.StaticText(httpInforSizer.GetStaticBox(), wx.ID_ANY, u"User-Agent:", wx.DefaultPosition,
                                           wx.Size(-1, -1), 0)
        self.m_staticText4.Wrap(-1)
        httpUABoxSizer.Add(self.m_staticText4, 0, wx.ALL, 5)

        self.textCtrlUserAgent = wx.TextCtrl(httpInforSizer.GetStaticBox(), wx.ID_ANY, wx.EmptyString,
                                             wx.DefaultPosition, wx.Size(380, -1), 0)
        self.textCtrlUserAgent.Enable(False)

        httpUABoxSizer.Add(self.textCtrlUserAgent, 0, wx.ALL, 5)

        httpInforSizer.Add(httpUABoxSizer, 1, wx.EXPAND, 5)

        httpCookieBoxSizer = wx.BoxSizer(wx.HORIZONTAL)

        self.m_staticText5 = wx.StaticText(httpInforSizer.GetStaticBox(), wx.ID_ANY, u"      Cookie:",
                                           wx.DefaultPosition, wx.DefaultSize, 0)
        self.m_staticText5.Wrap(-1)
        httpCookieBoxSizer.Add(self.m_staticText5, 0, wx.ALL, 5)

        self.textCtrlCookie = wx.TextCtrl(httpInforSizer.GetStaticBox(), wx.ID_ANY, wx.EmptyString, wx.DefaultPosition,
                                          wx.Size(380, 50), 0 | wx.VSCROLL)
        self.textCtrlCookie.Enable(False)

        httpCookieBoxSizer.Add(self.textCtrlCookie, 0, wx.ALL, 5)

        httpInforSizer.Add(httpCookieBoxSizer, 0, 0, 5)

        DialogMainSizer.Add(httpInforSizer, 0, wx.EXPAND | wx.ALL, 5)

        socksTunnelStaticBoxSizer = wx.StaticBoxSizer(wx.StaticBox(self, wx.ID_ANY, u"Socks内网通道"), wx.VERTICAL)

        self.sockDefaultcheckBox3 = wx.CheckBox(socksTunnelStaticBoxSizer.GetStaticBox(), wx.ID_ANY, u"不启用内网通道",
                                                wx.DefaultPosition, wx.DefaultSize, 0)
        self.sockDefaultcheckBox3.SetValue(True)
        socksTunnelStaticBoxSizer.Add(self.sockDefaultcheckBox3, 0, wx.ALL, 5)

        socksTunnelPortBoxSizer = wx.BoxSizer(wx.HORIZONTAL)

        self.m_staticText7 = wx.StaticText(socksTunnelStaticBoxSizer.GetStaticBox(), wx.ID_ANY, u"侦听端口：",
                                           wx.DefaultPosition, wx.DefaultSize, 0)
        self.m_staticText7.Wrap(-1)
        socksTunnelPortBoxSizer.Add(self.m_staticText7, 0, wx.ALIGN_CENTER_VERTICAL | wx.ALL, 5)

        self.textCtrlTunnelPort = wx.TextCtrl(socksTunnelStaticBoxSizer.GetStaticBox(), wx.ID_ANY, wx.EmptyString,
                                              wx.DefaultPosition, wx.DefaultSize, 0)
        self.textCtrlTunnelPort.Enable(False)

        socksTunnelPortBoxSizer.Add(self.textCtrlTunnelPort, 0, wx.ALL, 5)

        socksTunnelStaticBoxSizer.Add(socksTunnelPortBoxSizer, 1, wx.EXPAND, 5)

        socksTunnelAddressBoxSizer = wx.BoxSizer(wx.HORIZONTAL)

        self.m_staticText6 = wx.StaticText(socksTunnelStaticBoxSizer.GetStaticBox(), wx.ID_ANY, u"侦听地址：",
                                           wx.DefaultPosition, wx.DefaultSize, 0)
        self.m_staticText6.Wrap(-1)
        socksTunnelAddressBoxSizer.Add(self.m_staticText6, 0, wx.ALIGN_CENTER_VERTICAL | wx.ALL, 5)

        comboBoxTunnelAddressChoices = []
        self.comboBoxTunnelAddress = wx.ComboBox(socksTunnelStaticBoxSizer.GetStaticBox(), wx.ID_ANY, u"选择地址",
                                                 wx.DefaultPosition, wx.Size(150, -1), comboBoxTunnelAddressChoices, 0)
        self.comboBoxTunnelAddress.Enable(False)

        socksTunnelAddressBoxSizer.Add(self.comboBoxTunnelAddress, 0, wx.ALL, 5)

        socksTunnelStaticBoxSizer.Add(socksTunnelAddressBoxSizer, 1, wx.EXPAND, 5)

        DialogMainSizer.Add(socksTunnelStaticBoxSizer, 0, wx.EXPAND | wx.ALL, 5)

        saveDataBaseBtn = wx.BoxSizer(wx.HORIZONTAL)
        self.saveDataBaseBtnOK = wx.Button(self, -1,label='保存')
        saveDataBaseBtn.Add(self.saveDataBaseBtnOK, 0, wx.ALIGN_CENTER_VERTICAL | wx.ALL, 5)
        self.saveDataBaseBtnCancel = wx.Button(self, -1,label='退出')
        saveDataBaseBtn.Add(self.saveDataBaseBtnCancel, 0, wx.ALIGN_CENTER_VERTICAL | wx.ALL, 5)

        DialogMainSizer.Add(saveDataBaseBtn, 1, wx.ALIGN_CENTER_HORIZONTAL | wx.ALL, 5)

        self.SetSizer(DialogMainSizer)
        self.Layout()
        DialogMainSizer.Fit(self)

        self.Centre(wx.BOTH)

        # Connect Events
        self.httpDefaultcheckBox2.Bind(wx.EVT_CHECKBOX, self.OnHttpDefaultCheck)
        self.sockDefaultcheckBox3.Bind(wx.EVT_CHECKBOX, self.OnTunnelCheck)
        self.saveDataBaseBtnOK.Bind(wx.EVT_BUTTON, self.OnSaveBtnClick)
        self.saveDataBaseBtnCancel.Bind(wx.EVT_BUTTON, self.OnCancelBtnClick)

        self.httpSettingDefault=True
        self.tunnelSettingDefault=True

    def OnHttpDefaultCheck(self, event):
        if event.IsChecked():
            self.textCtrlCookie.Enable(False)
            self.textCtrlUserAgent.Enable(False)
            self.httpSettingDefault=True
        else:
            self.textCtrlCookie.Enable(True)
            self.textCtrlUserAgent.Enable(True)
            self.httpSettingDefault = False
        event.Skip()

    def OnTunnelCheck(self, event):
        if event.IsChecked():
            self.textCtrlTunnelPort.Enable(False)
            self.comboBoxTunnelAddress.Enable(False)
            self.tunnelSettingDefault=True
        else:
            self.textCtrlTunnelPort.Enable(True)
            self.comboBoxTunnelAddress.Enable(True)
            self.tunnelSettingDefault=False
        event.Skip()

    def OnSaveBtnClick(self, event):

        shell_address=self.textCtrlShellAddress.GetValue()

        if not shell_address:
            wx.MessageBox('Shell地址不能为空')
            return

        shell_password=self.textCtrlShellPassword.GetValue()

        if not shell_password:
            wx.MessageBox('Shell密码不能为空')
            return

        shell_script_type=self.comboBoxShellScriptType.GetValue()
        print shell_script_type
        if not shell_script_type:
            wx.MessageBox('请选择Shell脚本类型')

        shell_encode_type=self.comboBoxShellEncodeType.GetValue()
        print shell_encode_type
        if not shell_encode_type:
            wx.MessageBox('请选择Shell编码类型')

        database_info =self.textCtrlShellDatabase.GetValue()
        shell_remark =self.textCtrlRemark.GetValue()

        nowTime = datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S')

        shellEntity=shell_entity(shell_address,shell_password,shell_script_type,shell_encode_type,database_info,shell_remark,self.httpSettingDefault,self.tunnelSettingDefault,nowTime)
        DatabaseHelper.saveShellEntity(shellEntity)
        self.SetReturnCode(1)
        self.Destroy()
        event.Skip()

    def OnCancelBtnClick(self, event):
        self.Destroy()
        event.Skip()