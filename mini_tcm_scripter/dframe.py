""" Debug Frame. """
import json
from pprint import pprint
from pathlib import Path

import wx
from mini_tcm_scripter.report import create_pdf
from mini_tcm_scripter import RECORDS_DIR

DEBUG = True

class DFrame(wx.Frame):
    """ The frame """
    def __init__(self, parent, title='') -> None:
        super(DFrame, self).__init__(parent, title=title)
        # self.statusbar = self.CreateStatusBar()
        self.panel = wx.Panel(self)
        self.edit = wx.TextCtrl(self.panel, style=wx.TE_MULTILINE)
        self.btn1 = wx.Button(self.panel, label='Make PDF')

        self.btn1.Bind(wx.EVT_BUTTON, self.report)

        self.set_layout()

        # json
        if DEBUG:
            with open(RECORDS_DIR / '2020-09.json') as jfile:
                text = json.dumps((json.load(jfile)[0]), ensure_ascii=False, indent=4)
                self.edit.SetValue(text)

    def set_layout(self):
        inner_sizer = wx.BoxSizer(wx.VERTICAL)
        inner_sizer.Add(self.edit, 2, flag=wx.EXPAND|wx.ALL, border=5)
        inner_sizer.Add(self.btn1, -1, flag=wx.ALIGN_RIGHT|wx.ALL, border=5)
        self.panel.SetSizer(inner_sizer)

        sizer = wx.BoxSizer()
        sizer.Add(self.panel, 1, wx.EXPAND)
        self.SetSizer(sizer)
        self.Layout()

    def report(self, event:wx.Event):
        obj = json.loads(self.edit.Value)
        pprint(obj)

        create_pdf(obj)
