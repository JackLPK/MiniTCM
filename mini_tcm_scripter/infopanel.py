import wx
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


        self.set_layout()
        self.SetupScrolling()
        # self.SetBackgroundColour('red')

    def set_layout(self):
        MY_FLAG = wx.EXPAND | wx.LEFT | wx.RIGHT | wx.ALIGN_LEFT
        MY_BORDER = 2

        fgs = wx.FlexGridSizer(cols=2, vgap=5, hgap=5)

        def add_spacer(fg, w=50, h=10):
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
        # self.SetSizer(fgs)
        # return
        
        sizer = wx.BoxSizer(wx.VERTICAL)
        sizer.Add(fgs)
        
        sizer.Add(self.btn_clear_1, 0, MY_FLAG, MY_BORDER)
        sizer.Add(self.btn_clear_2, 0, MY_FLAG, MY_BORDER)
        

        # growables; later: rewrite into function
        # fgs.AddGrowableRow(4, 1)
        # fgs.AddGrowableRow(5, 1)
        # fgs.AddGrowableRow(6, 1)

        self.SetSizer(sizer)
