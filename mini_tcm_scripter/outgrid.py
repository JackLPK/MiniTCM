import wx
import wx.grid
from sample_data import sample_med_prep, sample_out_labels, sample_med_store
from mini_tcm_scripter import NO_EDITOR


class OutGrid(wx.grid.Grid):
    def __init__(self, parent, *args, **kwargs) -> None:
        super(OutGrid, self).__init__(parent, *args, **kwargs)
        self.labels = sample_out_labels
        self.statusbar = parent.statusbar
        self.CreateGrid(0, len(self.labels))  # test purpose, can remove
        self.set_col_labels()
        self.HideRowLabels()
        self.EnableDragRowSize(False)

        self.set_cell_attributes()
        self.get_mass = parent.get_mass
        self.set_binding()
        self.ShowScrollbars(wx.SHOW_SB_ALWAYS, wx.SHOW_SB_ALWAYS)

    def set_binding(self):
        self.Bind(wx.grid.EVT_GRID_CMD_CELL_RIGHT_DCLICK, self.on_cell_rdclick)
    
    def on_cell_rdclick(self, event:wx.grid.GridEvent):
        row, col = event.Row, event.Col
        if col in (0, 1):    # softcode this!!
            self.remove(row)
        pass

    def set_col_labels(self):
        for i, label in enumerate(self.labels):
            self.SetColLabelValue(i, label)

    def set_cell_attributes(self):
        # Cell attr
        self.SetColAttr(0, NO_EDITOR.Clone())
        self.SetColAttr(1, NO_EDITOR.Clone())

        #
        self.med_prep_choice_editor = wx.grid.GridCellChoiceEditor(sample_med_prep)
        self.ca_med_prep = wx.grid.GridCellAttr()   # cell attr cook method
        self.ca_med_prep.SetEditor(self.med_prep_choice_editor)
        self.SetColAttr(2, self.ca_med_prep)

        #
        self.mass_editor = wx.grid.GridCellNumberEditor(1, 10000)
        self.ca_mass = wx.grid.GridCellAttr()    # cell attr mass
        self.ca_mass.SetEditor(self.mass_editor)
        self.SetColAttr(3, self.ca_mass)


    def add(self, id):
        name_key = 'chinese_t'  # softcode this!!
        name = [obj[name_key] for obj in sample_med_store if int(obj['id']) == id]
        if len(name) > 1:
            raise Exception(f'Error: Arbitary id for data source, {med}')
        name = name[0]
        mass = self.get_mass()
        prep = sample_med_prep[0]
        print('fn:add', name, mass)

        #
        self.AppendRows()
        row = self.NumberRows-1

        # softcode this!!
        self.SetCellValue(row, self.labels.index('id'), str(id))
        self.SetCellValue(row, self.labels.index('name'), name)
        self.SetCellValue(row, self.labels.index('method'), prep)
        self.SetCellValue(row, self.labels.index('mass'), str(mass))
        
        self.statusbar.PushStatusText(f'++ {name}')
        
    def remove(self, row):
        value = self.GetCellValue(row, 1)
        self.statusbar.PushStatusText(f'-- {value}')
        self.DeleteRows(row)