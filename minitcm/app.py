import sys

import toml
import wx

from minitcm import CONFIG_FP
from minitcm.mainframe import MainFrame


class MyApp(wx.App):
    def OnInit(self):
        #
        try:
            toml.load(CONFIG_FP)
        except Exception as e:
            print(f'Error: Cannot load config file\n{CONFIG_FP}')
            wx.MessageBox(
                f'Error: Cannot load config file\n{CONFIG_FP}', 'Error',
                style=wx.ICON_WARNING)
            sys.exit()

        #
        self.frame1 = MainFrame(None, 'Mini TCM')
        self.frame1.SetMinSize((900, 750))
        self.frame1.SetSize(-1, -1, 900, 750)
        self.frame1.CenterOnScreen()
        self.frame1.Show()

        return True


def main():
    app = MyApp()
    app.MainLoop()
