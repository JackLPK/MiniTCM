from mini_tcm_scripter.mainframe import MainFrame
import wx


class MyApp(wx.App):
    def OnInit(self):
        self.frame1 = MainFrame(None, 'Hello TCM')
        self.frame1.SetSizeHints(900, 800)
        self.frame1.Show()
        self.frame1.Center()
        
        return True


def main():
    app = MyApp()
    app.MainLoop()
