from pprint import pprint
import wx
from wx.core import Size
import wx.grid
from wx.lib.scrolledpanel import ScrolledPanel
from mini_tcm_scripter.ingrid import InGrid
from mini_tcm_scripter.outgrid import OutGrid



class InfoPanel(ScrolledPanel):
    def __init__(self, parent) -> None:
        super(InfoPanel, self).__init__(parent)

        # Section: Patient
        self.lbl_patient_name = wx.StaticText(self, label='Patient Name')
        self.edit_patient_name = wx.TextCtrl(self, size=(1, -1))

        self.lbl_patient_age = wx.StaticText(self, label='Patient Age')
        self.edit_patient_age = wx.TextCtrl(self)

        self.lbl_patient_gender = wx.StaticText(self, label='Patient Gender')
        self.edit_patient_gender = wx.TextCtrl(self)

        self.lbl_patient_contact = wx.StaticText(self, label='Patient Contact')
        self.edit_patient_contact = wx.TextCtrl(self)

        # Section: Notes
        self.lbl_note_1 = wx.StaticText(self, label='Note 1')
        self.edit_note_1 = wx.TextCtrl(self, style=wx.TE_MULTILINE, size=(-1, 60))

        self.lbl_note_2 = wx.StaticText(self, label='Note 2')
        self.edit_note_2 = wx.TextCtrl(self, style=wx.TE_MULTILINE, size=(-1, 60))

        self.lbl_note_3 = wx.StaticText(self, label='Note 3')
        self.edit_note_3 = wx.TextCtrl(self, style=wx.TE_MULTILINE, size=(-1, 60))

        # Section: Doctor
        self.lbl_organiaztion_name = wx.StaticText(self, label='Organization')
        self.edit_organiaztion_name = wx.TextCtrl(self)

        self.lbl_doctor_name = wx.StaticText(self, label='Doctor Name')
        self.edit_doctor_name = wx.TextCtrl(self)

        # Section: Misc
        self.lbl_mass_unit = wx.StaticText(self, label='Mass Unit')
        self.edit_mass_unit = wx.TextCtrl(self)

        self.lbl_dangerous = wx.StaticText(self, label='Dangerous')
        self.edit_dangerous = wx.TextCtrl(self)

        self.lbl_amount_1 = wx.StaticText(self, label='Sticker A')
        self.edit_amount_1 = wx.TextCtrl(self)

        self.lbl_footer = wx.StaticText(self, label='Footer')
        self.edit_footer = wx.TextCtrl(self, style=wx.TE_MULTILINE)

        # Section: Buttons
        self.btn_clear_1 = wx.Button(self, label='Clear 1')
        self.btn_clear_2 = wx.Button(self, label='Clear 2')


        self.set_layout()
        self.SetupScrolling()
        # self.SetBackgroundColour('red')

    def set_layout(self):
        MY_FLAG = wx.EXPAND | wx.LEFT | wx.RIGHT | wx.ALIGN_LEFT
        MY_BORDER = 2

        fgs = wx.FlexGridSizer(cols=2, vgap=5, hgap=5)

        def add_spacer(fg, w=50, h=20):
            fg.Add(w, h)
            fg.Add(w, h)

        add_spacer(fgs)

        # patient
        fgs.Add(self.lbl_patient_name, flag=MY_FLAG, border=MY_BORDER)
        fgs.Add(self.edit_patient_name, flag=MY_FLAG, border=MY_BORDER)

        fgs.Add(self.lbl_patient_age, flag=MY_FLAG, border=MY_BORDER)
        fgs.Add(self.edit_patient_age, flag=MY_FLAG, border=MY_BORDER)

        fgs.Add(self.lbl_patient_gender, flag=MY_FLAG, border=MY_BORDER)
        fgs.Add(self.edit_patient_gender, flag=MY_FLAG, border=MY_BORDER)

        fgs.Add(self.lbl_patient_contact, flag=MY_FLAG, border=MY_BORDER)
        fgs.Add(self.edit_patient_contact, flag=MY_FLAG, border=MY_BORDER)
        add_spacer(fgs)

        # notes
        fgs.Add(self.lbl_note_1, flag=MY_FLAG, border=MY_BORDER)
        fgs.Add(self.edit_note_1, 1, flag=MY_FLAG, border=MY_BORDER)

        fgs.Add(self.lbl_note_2, flag=MY_FLAG, border=MY_BORDER)
        fgs.Add(self.edit_note_2, 1, flag=MY_FLAG, border=MY_BORDER)

        fgs.Add(self.lbl_note_3, flag=MY_FLAG, border=MY_BORDER)
        fgs.Add(self.edit_note_3, 1, flag=MY_FLAG, border=MY_BORDER)
        add_spacer(fgs)

        # doctor
        fgs.Add(self.lbl_organiaztion_name, flag=MY_FLAG, border=MY_BORDER)
        fgs.Add(self.edit_organiaztion_name, flag=MY_FLAG, border=MY_BORDER)

        fgs.Add(self.lbl_doctor_name, flag=MY_FLAG, border=MY_BORDER)
        fgs.Add(self.edit_doctor_name, flag=MY_FLAG, border=MY_BORDER)
        add_spacer(fgs)

        # misc
        fgs.Add(self.lbl_mass_unit, flag=MY_FLAG, border=MY_BORDER)
        fgs.Add(self.edit_mass_unit, flag=MY_FLAG, border=MY_BORDER)

        fgs.Add(self.lbl_dangerous, flag=MY_FLAG, border=MY_BORDER)
        fgs.Add(self.edit_dangerous, flag=MY_FLAG, border=MY_BORDER)

        fgs.Add(self.lbl_amount_1, flag=MY_FLAG, border=MY_BORDER)
        fgs.Add(self.edit_amount_1, flag=MY_FLAG, border=MY_BORDER)

        fgs.Add(self.lbl_footer, flag=MY_FLAG, border=MY_BORDER)
        fgs.Add(self.edit_footer, 1, flag=MY_FLAG, border=MY_BORDER)
        add_spacer(fgs)

        # buttons
        fgs.Add(self.btn_clear_1, flag=MY_FLAG, border=MY_BORDER)
        fgs.Add(self.btn_clear_2, flag=MY_FLAG, border=MY_BORDER)

        # growables; later: rewrite into function
        # fgs.AddGrowableRow(4, 1)
        # fgs.AddGrowableRow(5, 1)
        # fgs.AddGrowableRow(6, 1)

        self.SetSizerAndFit(fgs)


class MainPanel(wx.Panel):
    def __init__(self, parent) -> None:
        super(MainPanel, self).__init__(parent)
        self.statusbar = parent.statusbar
        self.info_panel = InfoPanel(self)
        self.search_bar = MySearchBar(self, style=wx.TE_PROCESS_ENTER)
        self.in_grid = InGrid(self)
        self.out_grid = OutGrid(self)

        self.set_layout()
        self.set_binding()
        self.search_bar.SetFocus()

    def set_layout(self):
        self.info_panel.SetMinSize((300, 300))
        self.in_grid.SetMinSize((300, 600))
        self.out_grid.SetMinSize((300, 600))

        inner_sizer = wx.BoxSizer()
        inner_sizer.Add(self.in_grid, proportion=1, flag=wx.EXPAND|wx.ALL, border=5)
        inner_sizer.Add(self.out_grid, proportion=1, flag=wx.EXPAND|wx.ALL, border=5)

        #
        sizer = wx.BoxSizer(wx.VERTICAL)
        sizer.Add(self.search_bar, flag=wx.EXPAND|wx.ALL, border=5)
        sizer.Add(inner_sizer, flag=wx.EXPAND|wx.ALL, border=5)


        outer_sizer = wx.BoxSizer(orient=wx.HORIZONTAL)
        outer_sizer.Add(sizer, proportion=1, flag=wx.EXPAND|wx.ALL, border=5)
        outer_sizer.Add(self.info_panel, proportion=1, flag=wx.EXPAND|wx.ALL, border=5)

        self.SetSizer(outer_sizer)
        self.Layout()
        # outer_sizer.Fit(self)

    def set_binding(self):
        self.search_bar.Bind(wx.EVT_TEXT, self.on_text)
        self.search_bar.Bind(wx.EVT_TEXT_ENTER, self.on_text_enter)
        self.search_bar.Bind(wx.EVT_KEY_DOWN, self.on_key_down)
        self.in_grid.Bind(wx.grid.EVT_GRID_CELL_LEFT_DCLICK, self.on_grid_left_dclick)

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
    

    
class MySearchBar(wx.TextCtrl):
    def __init__(self, parent, *args, **kwargs) -> None:
        super(MySearchBar, self).__init__(parent, *args, **kwargs)


class MyFrame(wx.Frame):
    def __init__(self, parent, title='') -> None:
        super(MyFrame, self).__init__(parent, title=title)
        self.statusbar = self.CreateStatusBar()
        #
        self.panel = MainPanel(self)
        
        self.set_layout()

        #
        self.CenterOnScreen()
        self.SetSizeHints(800, 600)
        self.SetSize(1000, 650)
        self.Show()
        self.Center()

    def set_layout(self):
        sizer = wx.BoxSizer()
        sizer.Add(self.panel, 1, flag=wx.EXPAND)
        self.SetSizer(sizer)

def main():
    app = wx.App()
    fr = MyFrame(None, title='Mini TCM Scripter')
    app.MainLoop()



