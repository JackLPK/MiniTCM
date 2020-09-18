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
        self.set_menu()
        self.Layout()

    def set_menu(self):
        menu_bar = wx.MenuBar()
        file_menu = wx.Menu()
        file_item = file_menu.Append(wx.ID_EXIT, '&Quit', 'Quit application')

        edit_menu = wx.Menu()
        json2pdf_item = edit_menu.Append(wx.ID_ANY, 'JSON to PDF', 'Convert JSON string to PDF')


        menu_bar.Append(file_menu, '&File')
        menu_bar.Append(edit_menu, '&Edit')
        self.SetMenuBar(menu_bar)

        self.Bind(wx.EVT_MENU, self.on_quit, file_item)
        self.Bind(wx.EVT_MENU, self.show_d_frame, json2pdf_item)

    def on_quit(self, e:wx.Event):
        self.Close()

    def show_d_frame(self, e:wx.Event):
        from mini_tcm_scripter.dframe import DFrame
        frame2 = DFrame(None, 'Debug')
        frame2.Center()
        frame2.Show()

