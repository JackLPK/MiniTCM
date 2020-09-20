import json
import toml
from pathlib import Path
from datetime import datetime
from pprint import pprint

import wx
from wx.lib.scrolledpanel import ScrolledPanel

from mini_tcm_scripter import PROFILES_DIR, RECORDS_DIR
# from sample_data import sample_profile_1, sample_export_data


class InfoPanel(ScrolledPanel):
    def __init__(self, parent, ini_profile_fp) -> None:
        super(InfoPanel, self).__init__(parent)
        self.profile = ini_profile_fp

        self.make_controls()
        self.make_sections()
        self.set_defaults()
        self.set_binding()
        self.set_layout()
        self.Layout()

        # self.SetBackgroundColour('red')
        # self.Bind(wx.EVT_SIZE, self.on_size)
        self.SetupScrolling()

    def set_binding(self):
        self.btn_debug.Bind(wx.EVT_BUTTON, self.on_button)
        self.btn_clear_1.Bind(wx.EVT_BUTTON, self.on_button)
        self.btn_clear_2.Bind(wx.EVT_BUTTON, self.on_button)
        self.btn_preview.Bind(wx.EVT_BUTTON, self.on_button)
        self.btn_save.Bind(wx.EVT_BUTTON, self.on_button)

    def on_button(self, event:wx.Event):
        event_obj = event.GetEventObject()

        if event_obj == self.btn_debug:
            print('debug button')
        elif event_obj == self.btn_clear_1:
            self.set_defaults()
        elif event_obj == self.btn_clear_2:
            event.Skip()
        elif event_obj == self.btn_preview:
            event.Skip()
        elif event_obj == self.btn_save:
            event.Skip()
        else:
            event.Skip()

    def reload_ui(self, profile=None):
        self.Freeze()
        self.sizer.Clear(True)

        # self.profile = self.get_profile(fp)
        self.profile = profile
        self.make_controls()
        self.make_sections()
        self.set_defaults()
        self.set_binding()
        self.set_layout()
        self.Layout()
        self.Thaw()

    def make_controls(self):
        # Section: Patient
        self.lbl_patient_name = wx.StaticText(self, label='Patient Name')
        self.edit_patient_name = wx.TextCtrl(self)

        self.lbl_patient_age = wx.StaticText(self, label='Patient Age')
        self.edit_patient_age = wx.SpinCtrl(self, min=0, max=1000, initial=0)

        self.lbl_patient_gender = wx.StaticText(self, label='Patient Gender')
        self.edit_patient_gender = wx.ComboBox(self, choices=self.profile['gender'], style=wx.CB_READONLY)

        self.lbl_patient_contact = wx.StaticText(self, label='Patient Contact')
        self.edit_patient_contact = wx.TextCtrl(self)

        # Section: Doctor
        self.lbl_organiaztion_name = wx.StaticText(self, label='Organization')
        self.edit_organiaztion_name = wx.TextCtrl(self)

        self.lbl_doctor_name = wx.StaticText(self, label='Doctor Name')
        self.edit_doctor_name = wx.TextCtrl(self)

        # Section: Misc
        self.lbl_mass_unit = wx.StaticText(self, label='Mass Unit')
        self.edit_mass_unit = wx.ComboBox(self, choices=self.profile['unit'])

        self.lbl_dangerous = wx.StaticText(self, label='Dangerous')
        self.edit_dangerous = wx.ComboBox(self, choices=self.profile['category'])

        self.lbl_dosage = wx.StaticText(self, label='Dosage')
        self.edit_dosage = wx.SpinCtrl(self, min=0, max=1000, initial=1)

        self.lbl_footer = wx.StaticText(self, label='Footer')
        self.edit_footer = wx.TextCtrl(self, style=wx.TE_MULTILINE)
        # might add payment method

        # Section: Buttons
        self.btn_clear_1 = wx.Button(self, label='Clear info')
        self.btn_clear_2 = wx.Button(self, label='Clear grid')
        self.btn_preview = wx.Button(self, label='Preview')
        self.btn_save = wx.Button(self, label='Save')
        self.btn_debug = wx.Button(self, label='debug')

    def set_defaults(self, event=None):
        # Patient
        self.edit_patient_name.SetValue('')
        self.edit_patient_age.SetValue(0)
        self.edit_patient_gender.SetSelection(0)
        self.edit_patient_contact.SetValue('')

        # Doctor
        self.edit_organiaztion_name.SetValue(self.profile['doctor']['organisation'])
        self.edit_doctor_name.SetValue(self.profile['doctor']['name'])

        # Notes
        for lbl, edit in self.section_notes:
            content = [note['content'] for note in self.profile['notes'] if note['name'] == lbl.LabelText][0]
            edit.SetValue(content)

        # Misc
        self.edit_mass_unit.SetSelection(0)
        self.edit_dangerous.SetSelection(0)
        self.edit_dosage.SetValue(1)
        self.edit_footer.SetValue(self.profile['footer'])

    def make_sections(self):
        self.section_patient = (
            (self.lbl_patient_name, self.edit_patient_name),
            (self.lbl_patient_age, self.edit_patient_age),
            (self.lbl_patient_gender, self.edit_patient_gender),
            (self.lbl_patient_contact, self.edit_patient_contact)
        )

        self.section_notes = self._make_notes()

        self.section_doctor = (
            (self.lbl_organiaztion_name, self.edit_organiaztion_name),
            (self.lbl_doctor_name, self.edit_doctor_name),
        )

        self.section_misc = (
            (self.lbl_mass_unit, self.edit_mass_unit),
            (self.lbl_dangerous, self.edit_dangerous),
            (self.lbl_dosage, self.edit_dosage),
            (self.lbl_footer, self.edit_footer)
        )

        self.section_btn = (
            self.btn_clear_1,
            self.btn_clear_2,
            self.btn_preview,
            self.btn_save,
            self.btn_debug
        )

    def set_layout(self):
        self.sizer = wx.GridBagSizer(5, 5)
        row = 0
        to_grow = []
        to_grow.extend(self.section_notes)
        to_grow.append((self.lbl_footer, self.edit_footer))

        for lbl, edit in self.section_patient:
            self.sizer.Add(lbl, (row, 0))
            self.sizer.Add(edit, (row, 1), flag=wx.EXPAND)
            row += 1

        row += 1

        for lbl, edit in self.section_notes:
            self.sizer.Add(lbl, (row, 0))
            self.sizer.Add(edit, (row, 1), flag=wx.EXPAND)
            # to_grow.append(row)
            row += 1

        row += 1

        for lbl, edit in self.section_doctor:
            self.sizer.Add(lbl, (row, 0))
            self.sizer.Add(edit, (row, 1), flag=wx.EXPAND)
            row += 1

        row += 1

        for lbl, edit in self.section_misc:
            self.sizer.Add(lbl, (row, 0))
            self.sizer.Add(edit, (row, 1), flag=wx.EXPAND)
            row += 1

        row += 1

        for btn in self.section_btn:
            self.sizer.Add(btn, (row, 0), span=(1, 2), flag=wx.EXPAND)
            row += 1


        self.sizer.AddGrowableCol(1)
        for lbl, edit in to_grow:
            row = self.sizer.GetItemPosition(edit)[0]
            self.sizer.AddGrowableRow(row)
        self.SetSizer(self.sizer)

    def preview123(self):
        self.export()
        pass

    def previous_id(self):
        try:
            # print(list(RECORDS_DIR.glob('*.json')))
            fp = sorted(list(RECORDS_DIR.glob('*.json')), reverse=True)[0]
            # print('fn previous_id fp', fp)
            with open(fp, encoding='utf-8') as json_file:
                obj_list = json.load(json_file)
                last_id = [obj['data']['script']['id'] for obj in obj_list][-1]
            # print('fn previous_id last_id', last_id)
            return int(last_id)
        except Exception as e:
            print(e)
            wx.MessageBox('Cannot Retrieve previous record id. Starts with 1 now', 'Warning', wx.ICON_WARNING, self)
            return 0


    def export(self):
        obj = {
            'script': {
                'id': self.previous_id() + 1,    # softcode this
                'subtitle': '處方紙',
                'date': datetime.now().isoformat(timespec='seconds'),
                'unit': self.edit_mass_unit.Value,
                'category': self.edit_dangerous.Value,
                'footer': self.edit_footer.Value,
                'dosage': self.edit_dosage.Value,
                'payment': False
            },
            'meds': [],
            'doctor': {
                'organisation': self.edit_organiaztion_name.Value,
                'name': self.edit_doctor_name.Value
            },
            'patient': {
            'name': self.edit_patient_name.Value,
            'age': self.edit_patient_age.Value,
            'gender': self.edit_patient_gender.Value,
            'contact': self.edit_patient_contact.Value
            },
            'notes': [{'name': lbl.LabelText, 'content': edit.Value} for lbl, edit in self.section_notes ]
        }

        return obj

    def _make_notes(self):
        notes = self.profile['notes']
        retval = []
        for note in notes:
            lbl = wx.StaticText(self, label=note['name'])
            edit = wx.TextCtrl(self, style=wx.TE_MULTILINE, size=(-1, 60))
            edit.ChangeValue(note['content'])
            retval.append((lbl, edit))

        return retval
