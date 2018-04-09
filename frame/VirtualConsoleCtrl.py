# coding=utf-8

"""
@version: 1.0
@author: chaowei
@file: VirtualConsoleCtrl.py
@time: 2018/4/8 23:14
"""
import  wx,sys
import wx.lib.editor as editor

sys.path.append("..")

class VirtualConsole(wx.Panel):

    def __init__(self, parent, log):
        self.log = log
        wx.Panel.__init__(self, parent, -1)

        self.ed = editor.Editor(self, -1, style=wx.SUNKEN_BORDER)
        box = wx.BoxSizer(wx.VERTICAL)
        box.Add(self.ed, 1, wx.ALL | wx.GROW, 1)
        self.SetSizer(box)
        self.SetAutoLayout(True)
        self.ed.SetBackgroundColour(wx.SystemSettings.GetColour( wx.SYS_COLOUR_BACKGROUND ) )

        self.ed.SetText(["",
                    "This is a simple text editor, the class name is",
                    "Editor.  Type a few lines and try it out.",
                    "",
                    "It uses Windows-style key commands that can be overridden by subclassing.",
                    "Mouse select works. Here are the key commands:",
                    "",
                    "Cursor movement:     Arrow keys or mouse",
                    "Beginning of line:   Home",
                    "End of line:         End",
                    "Beginning of buffer: Control-Home",
                    "End of the buffer:   Control-End",
                    "Select text:         Hold down Shift while moving the cursor",
                    "Copy:                Control-Insert, Control-C",
                    "Cut:                 Shift-Delete,   Control-X",
                    "Paste:               Shift-Insert,   Control-V",
                    ""])