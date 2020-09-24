import csv
import webbrowser
from pathlib import Path

import toml
import wx
import wx.grid

from minitcm import CONFIG_FP, PDFS_DIR, PROFILES_DIR, U_DIR, add_to_db
from minitcm.infopanel import InfoPanel
from minitcm.ingrid import InGrid
from minitcm.outgrid import OutGrid
from minitcm.report import create_pdf


class MainPanel(wx.Panel):
    def __init__(self, parent, *args, **kwargs) -> None:
        super(MainPanel, self).__init__(parent, *args, **kwargs)
        self.lbl_profile = wx.StaticText(self, label='No Profile')
        self.profile = self.ini_profile()
        self.store = self.get_store()
        self.statusbar = parent.statusbar
        self.search_bar = wx.TextCtrl(self, style=wx.TE_PROCESS_ENTER)
        self.btn_reload = wx.Button(self, label='Choose Profile')

        self.in_grid = InGrid(self, self.store)
        self.out_grid = OutGrid(self, self.profile, self.store)

        self.info_panel = InfoPanel(self, self.profile)

        self.set_layout()
        self.set_binding()

    def set_layout(self):

        # top bar area
        sizer_1 = wx.BoxSizer()
        sizer_1.Add((50, -1), 1)
        sizer_1.Add(self.search_bar, 3, flag=wx.ALL, border=5)
        sizer_1.Add((50, -1), 2)
        sizer_1.Add(self.btn_reload, -1, flag=wx.ALL, border=5)
        sizer_1.Add(self.lbl_profile, -1, wx.ALL|wx.ALIGN_CENTER_VERTICAL, 5)
        sizer_1.Add((50, -1), 1)

        sizer_2 = wx.BoxSizer()
        sizer_2.Add(self.in_grid, 1, wx.EXPAND|wx.ALIGN_TOP|wx.ALL, 5)
        sizer_2.Add(self.out_grid, 1, wx.EXPAND|wx.ALIGN_TOP|wx.ALL, 5)
        sizer_2.Add(self.info_panel, 1, wx.EXPAND|wx.ALIGN_TOP|wx.ALL, 5)

        #
        sizer = wx.BoxSizer(wx.VERTICAL)
        sizer.Add(sizer_1, 1, wx.EXPAND)
        sizer.Add(wx.StaticLine(self, ))
        sizer.Add(sizer_2, 1, wx.EXPAND)

        #
        self.SetSizer(sizer)
        self.Layout()

    def set_binding(self):
        self.search_bar.Bind(wx.EVT_TEXT, self.on_text)
        self.search_bar.Bind(wx.EVT_TEXT_ENTER, self.on_text_enter)
        self.search_bar.Bind(wx.EVT_KEY_DOWN, self.on_key_down)
        self.in_grid.Bind(wx.grid.EVT_GRID_CELL_LEFT_DCLICK, self.on_grid_left_dclick)
        self.btn_reload.Bind(wx.EVT_BUTTON, self.on_button)
        self.info_panel.Bind(wx.EVT_BUTTON, self.on_button)

    def ini_profile(self):
        """ Initialise profile and set label """
        p_fp = None
        try:
            config = toml.load(CONFIG_FP)
            p_fp = Path(U_DIR / config['profile']).absolute()
            if not p_fp.exists():
                raise KeyError

            self.lbl_profile.SetLabelText(p_fp.stem)
            return toml.load(p_fp)

        except FileNotFoundError:
            wx.MessageBox('Cannot find config.toml')
        except KeyError:
            wx.MessageBox(f'Cannot identify default profile for {p_fp}')

    def get_store(self):
        config = toml.load(CONFIG_FP)
        fp = Path(U_DIR / config['store']).resolve()
        if not fp.exists():
            wx.MessageBox(f'Cannot locate store: {fp}')
        #
        ms = []
        with open(fp, newline='', encoding='utf-8') as csv_file:
            reader = csv.DictReader(csv_file, delimiter='\t')
            for line in reader:
                ms.append(line)
        return ms

    def reload_ui(self):
        """ Reload profile, affects info panel and outgrid. """
        fdlg = wx.FileDialog(
            self, 'Choose profile', PROFILES_DIR.as_posix(),
            style=wx.FD_OPEN|wx.FD_FILE_MUST_EXIST
        )

        # remember starting directory
        if fdlg.ShowModal() == wx.ID_OK:

            fp = Path(fdlg.GetPath()).resolve()
            self.profile = toml.load(fp)
            self.lbl_profile.SetLabelText(fp.stem)
            self.info_panel.reload_ui(self.profile)
            self.out_grid.reload_ui(self.profile)

    def on_button(self, event:wx.Event):
        event_obj = event.GetEventObject()

        if event_obj == self.btn_reload:
            self.reload_ui()
        elif event_obj == self.info_panel.btn_clear_2:
            self.out_grid.clear()
        elif event_obj == self.info_panel.btn_preview:
            self.preview()
        elif event_obj == self.info_panel.btn_save:
            self.save()
        else:
            print(event_obj)
            event.Skip()

    def _export(self):
        """ Call export on both outgrid and infopanel """
        data = self.info_panel.export()
        data['meds'] = self.out_grid.export(self.info_panel.profile)  # rewrite, put profile to mainpanel
        return data

    def preview(self):
        data = self._export()
        fp = create_pdf(None, {'data': data}, True)
        webbrowser.open(fp.as_uri(), True, True)

    def save(self):
        print('save from mainpanel')
        fp = None
        data = self._export()
        default_fn = '{}_{}.pdf'.format(data['patient']['name'], data['script']['date'].replace('T', '_'))
        default_fn = default_fn.replace(':', '_')
        # print('default filename', default_fn)
        fdlg = wx.FileDialog(
            self, 'Save as PDF', PDFS_DIR.as_posix(),
            default_fn, 'PDF files (*.pdf)|*.pdf', wx.FD_SAVE)
        if fdlg.ShowModal() == wx.ID_OK:
            if add_to_db(data):    # save to database
                self.statusbar.PushStatusText('Added to database.')
            fp = Path(fdlg.GetPath()).resolve()
            create_pdf(fp, {'data': data}, False)
            try:
                if toml.load(CONFIG_FP).get('open_after_save', False):
                    webbrowser.open(fp.as_uri(), True, True)
            except:
                wx.MessageBox('Error: config.toml error', 'Error', style=wx.ICON_ERROR)

        else:
            return

    def on_text(self, event: wx.Event):
        event_obj = event.EventObject
        if event_obj == self.search_bar:
            value = event_obj.GetValue()
            self.in_grid.filter(value) if ':' not in value else None
        else:
            print('other text events')
        event.Skip()

    def on_key_down(self, event:wx.KeyEvent):
        event_obj = event.GetEventObject()
        keycode = event.KeyCode

        if event_obj == self.search_bar and keycode in (315, 317):
            if keycode == 315: # UP
                self.in_grid.select_new_row('U')
            elif keycode == 317: # DOWN
                self.in_grid.select_new_row('D')
        else:
            event.Skip()

    def on_text_enter(self, event: wx.Event):
        event_obj = event.GetEventObject()
        if event_obj == self.search_bar:
            med_id = self.in_grid.current_id
            self.out_grid.add(med_id)
        # no skip

    def on_grid_left_dclick(self, event:wx.grid.GridEvent):
        event_obj = event.GetEventObject()
        if event_obj == self.in_grid:
            med_id = self.in_grid.current_id
            self.out_grid.add(med_id)
        event.Skip()

    def get_mass(self)->int:
        """ Get mass as int """
        mass = self.search_bar.Value.partition(':')[2]  # None or num
        self.search_bar.Clear()    # clear search bar
        return mass if mass.isdigit() else 1
