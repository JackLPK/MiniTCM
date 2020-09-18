import wx
from mini_tcm_scripter.mainpanel import MainPanel

class MainFrame(wx.Frame):
    """ The frame """
    def __init__(self, parent, title='') -> None:
        super(MainFrame, self).__init__(parent, title=title)
        self.statusbar = self.CreateStatusBar()

        self.panel = MainPanel(self)

        sizer = wx.BoxSizer()
        sizer.Add(self.panel, 1, wx.EXPAND)
        self.SetSizer(sizer)
        self.Layout()
