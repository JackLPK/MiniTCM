import wx
import json
import zlib

class ChecksumFrame(wx.Frame):
    """ Checksum """
    def __init__(self, parent, title='') -> None:
        super(ChecksumFrame, self).__init__(parent, title=title)
        self.panel = wx.Panel(self)
        self.edit1 = wx.TextCtrl(self.panel, style=wx.TE_MULTILINE)
        self.lbl = wx.StaticText(self.panel, label='Checksum (CRC32)')
        self.edit2 = wx.TextCtrl(self.panel)

        self.set_layout()

        self.edit1.Bind(wx.EVT_TEXT, self.calculate)

    def set_layout(self):
        inner_sizer = wx.BoxSizer(wx.VERTICAL)
        inner_sizer.Add(self.edit1, 1, wx.EXPAND|wx.ALL, 2)
        inner_sizer.Add(self.lbl, 0, wx.ALL, 2)
        inner_sizer.Add(self.edit2, 0, wx.ALL, 2)

        self.panel.SetSizer(inner_sizer)

        sizer = wx.BoxSizer(wx.VERTICAL)
        sizer.Add(self.panel, 1, wx.EXPAND)
        self.SetSizer(sizer)
        self.Layout()

    def calculate(self, e:wx.Event):
        text = self.edit1.Value
        if text == '':
            self.lbl.SetLabelText('Checksum (CRC32):')
            self.edit2.SetValue('')
            return

        try:
            obj = json.loads(text)
            num = zlib.crc32(json.dumps(obj, ensure_ascii=False).encode('utf-8'))
            self.lbl.SetLabelText('Checksum (CRC32): Valid JSON')

        except json.JSONDecodeError:
            num = zlib.crc32(text.encode('utf-8'))
            self.lbl.SetLabelText('Checksum (CRC32): Invalid JSON')

        self.edit2.SetValue(str(num))
