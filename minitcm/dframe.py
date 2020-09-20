""" Debug Frame. """
import json, toml
import webbrowser
from pprint import pprint
from pathlib import Path

import wx
from minitcm.report import create_pdf
from minitcm import RECORDS_DIR, PDFS_DIR, CONFIG_FP, DEBUG

# DEBUG = False

class DFrame(wx.Frame):
    """ The frame """
    def __init__(self, parent, title='') -> None:
        super(DFrame, self).__init__(parent, title=title)
        # self.statusbar = self.CreateStatusBar()
        self.panel = wx.Panel(self)
        self.edit = wx.TextCtrl(self.panel, style=wx.TE_MULTILINE)
        self.btn1 = wx.Button(self.panel, label='Make PDF')

        self.btn1.Bind(wx.EVT_BUTTON, self.on_button)

        self.set_layout()

        # json
        if DEBUG:
            with open(RECORDS_DIR / '2020-09.json', encoding='utf-8') as jfile:
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

    def on_button(self, e:wx.Event):
        e_obj = e.GetEventObject()
        if e_obj == self.btn1:
            fdlg = wx.FileDialog(
                self, 'Export to PDF', PDFS_DIR.as_posix(),
                style=wx.FD_SAVE, wildcard='PDF files (*.pdf)|*.pdf')
            if fdlg.ShowModal() == wx.ID_OK:
                fp = Path(fdlg.GetPath()).resolve()
                self.report(fp)
            else:
                return

        else:
            e.Skip()

    def report(self, fp:Path):
        obj = json.loads(self.edit.Value)
        create_pdf(fp, obj)

        try:
            if toml.load(CONFIG_FP)['open_after_save'] == True:
                webbrowser.open(fp.as_uri(), new=True, autoraise=True)
        except Exception as e:
            print(e)
