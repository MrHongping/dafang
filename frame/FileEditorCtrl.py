# coding=utf-8

"""
@version: 1.0
@author: chaowei
@file: FileEditorCtrl.py
@time: 2018/4/1 20:16
"""
import  wx,sys
import wx.richtext as rt

sys.path.append("..")

class FileEditor(wx.Panel):

    def __init__(self, parent, log,fileContent):
        self.log = log
        wx.Panel.__init__(self, parent, -1)

        self.ed = rt.RichTextCtrl(self, style=wx.VSCROLL|wx.HSCROLL|wx.NO_BORDER)
        box = wx.BoxSizer(wx.VERTICAL)
        box.Add(self.ed, 1, wx.ALL | wx.GROW, 1)
        self.SetSizer(box)
        self.ed.WriteText(fileContent)
