from mini_tcm_scripter.mainframe import MainFrame
from mini_tcm_scripter.dframe import DFrame
import wx


class MyApp(wx.App):
    def OnInit(self):
        self.frame1 = MainFrame(None, 'Hello TCM')
        self.frame1.SetMinSize((900, 750))
        self.frame1.SetSize(-1, -1, 900, 750)
        self.frame1.CenterOnScreen()
        self.frame1.Show()

        # self.frame2 = DFrame(None, 'Debug')
        # self.frame2.Center()
        # self.frame2.Show()

        return True


def main():
    app = MyApp()
    app.MainLoop()
