import wx
from wx.core import Event
from wx.lib.scrolledpanel import ScrolledPanel


class InfoPanel(ScrolledPanel):
    def __init__(self, parent) -> None:
        super(InfoPanel, self).__init__(parent)

        # Section: Patient
        self.lbl_patient_name = wx.StaticText(self, label='Patient Name')
        self.edit_patient_name = wx.TextCtrl(self)

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

        # # Section: Buttons
        self.btn_clear_1 = wx.Button(self, label='Clear 1')
        self.btn_clear_2 = wx.Button(self, label='Clear 2')


        # self.set_layout_2()
        self.set_layout()
        self.SetupScrolling()
        # self.SetBackgroundColour('red')
        self.Bind(wx.EVT_SIZE, self.on_size)
        self.Layout()
        


    def set_layout(self):
        
        sizer = wx.GridBagSizer(5, 5)
        to_grow = []
        
        def add_row(sizer, row, items, grow=False, prop=0):
            # for c, item in enumerate(items):
            #     sizer.Add(item, (row, c))
            sizer.Add(items[0], (row, 0))
            sizer.Add(items[1], (row, 1), flag=wx.EXPAND)
            if grow:
                # sizer.AddGrowableRow(row, prop)
                to_grow.append((row, prop))
        
        add_row(sizer, 0, [self.lbl_patient_name, self.edit_patient_name])
        add_row(sizer, 1, [self.lbl_patient_age, self.edit_patient_age])
        add_row(sizer, 2, [self.lbl_patient_gender, self.edit_patient_gender])
        add_row(sizer, 3, [self.lbl_patient_contact, self.edit_patient_contact])
        
        add_row(sizer, 5, [self.lbl_note_1, self.edit_note_1], True, 1)
        add_row(sizer, 6, [self.lbl_note_2, self.edit_note_2], True, 1)
        add_row(sizer, 7, [self.lbl_note_3, self.edit_note_3], True, 1)
        
        add_row(sizer, 9, [self.lbl_organiaztion_name, self.edit_organiaztion_name])
        add_row(sizer, 10, [self.lbl_doctor_name, self.edit_doctor_name])
        
        add_row(sizer, 12, [self.lbl_mass_unit, self.edit_mass_unit])
        add_row(sizer, 13, [self.lbl_dangerous, self.edit_dangerous])
        add_row(sizer, 14, [self.lbl_amount_1, self.edit_amount_1])
        add_row(sizer, 15, [self.lbl_footer, self.edit_footer], True, 1)

        sizer.Add(self.btn_clear_1, pos=(16, 0), span=(1, 2), flag=wx.EXPAND)
        sizer.Add(self.btn_clear_2, (17, 0), span=(1, 2), flag=wx.EXPAND)
        

        sizer.AddGrowableCol(1)
        self.SetSizer(sizer)


    def on_size(self, event:wx.Event):
        event.Skip()