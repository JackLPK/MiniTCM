from minitcm import CONFIG_FP
import wx
from minitcm.mainpanel import MainPanel

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
        settings_item = file_menu.Append(wx.ID_ANY, '&Settings', 'Configure program')
        file_item = file_menu.Append(wx.ID_EXIT, '&Quit', 'Quit application')

        tools_menu = wx.Menu()
        json2pdf_item = tools_menu.Append(wx.ID_ANY, 'JSON to PDF', 'Convert JSON string to PDF')
        checksum_item = tools_menu.Append(wx.ID_ANY, 'Checksum', 'Calculate checksum')
        
        menu_bar.Append(file_menu, '&File')
        menu_bar.Append(tools_menu, '&Tools')
        self.SetMenuBar(menu_bar)

        self.Bind(wx.EVT_MENU, self.on_quit, file_item)
        self.Bind(wx.EVT_MENU, self.show_settings, settings_item)
        self.Bind(wx.EVT_MENU, self.show_d_frame, json2pdf_item)
        self.Bind(wx.EVT_MENU, self.show_cs_frame, checksum_item)

    def on_quit(self, e:wx.Event):
        self.Close()

    def show_d_frame(self, e:wx.Event):
        from minitcm.dframe import DFrame
        frame2 = DFrame(self, 'Debug')
        frame2.Center()
        frame2.Show()

    def show_cs_frame(self, e:wx.Event):
        from minitcm.checksum_frame import ChecksumFrame
        frame = ChecksumFrame(self, 'Checksum')
        frame.Show()

    def show_settings(self, e:wx.Event):
        wx.MessageBox(f'Configure program at:\n{CONFIG_FP}', 'Settings')
        print(f'Configure program at:\n{CONFIG_FP}')
        pass