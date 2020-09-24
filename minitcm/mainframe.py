from os import name
import wx
import sys
import wx.html
from minitcm import CONFIG_FP, __version__
from minitcm.mainpanel import MainPanel

class AboutDialog(wx.Dialog):
    help_text = \
f'''
<html>
    <h1>Mini TCM ({__version__})</h1>
    <p>
    Running on:<br>
    wxPython {wx.VERSION_STRING}<br>
    Python {sys.version.split(' ')[0]}<br>
<p>
    A very mini/simple script(PDF) writer for traditional chinese medicine.
<p>
</html>
'''
    def __init__(self, parent) -> None:
        super(AboutDialog, self).__init__(parent=parent)
        self.SetTitle('About')
        self.html = wx.html.HtmlWindow(self)
        self.html.SetPage(self.help_text)


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

        about_menu = wx.Menu()
        about_item = about_menu.Append(wx.ID_ANY, 'About', 'About')

        menu_bar.Append(file_menu, '&File')
        menu_bar.Append(tools_menu, '&Tools')
        menu_bar.Append(about_menu, 'About')
        self.SetMenuBar(menu_bar)

        self.Bind(wx.EVT_MENU, self.on_quit, file_item)
        self.Bind(wx.EVT_MENU, self.settings, settings_item)
        self.Bind(wx.EVT_MENU, self.json2pdf, json2pdf_item)
        self.Bind(wx.EVT_MENU, self.checksum, checksum_item)
        self.Bind(wx.EVT_MENU, self.about, about_item)

    def on_quit(self, e:wx.Event):
        self.Close()

    def json2pdf(self, e:wx.Event):
        from minitcm.dframe import DFrame
        frame2 = DFrame(self, 'Debug')
        frame2.Center()
        frame2.Show()

    def checksum(self, e:wx.Event):
        from minitcm.checksum_frame import ChecksumFrame
        frame = ChecksumFrame(self, 'Checksum')
        frame.Show()

    def settings(self, e:wx.Event):
        wx.MessageBox(f'Configure program at:\n{CONFIG_FP}', 'Settings')
        print(f'Configure program at:\n{CONFIG_FP}')
        pass

    def about(self, e:wx.Event):
        dlg = AboutDialog(self)
        dlg.ShowModal()
        dlg.Destroy()
