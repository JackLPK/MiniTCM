""" Debug Frame. """
import wx
import json
from pprint import pprint

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
            from sample_data import sample_export_data
            text = json.dumps(sample_export_data, ensure_ascii=False)
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


