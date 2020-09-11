import wx
import re
from pprint import pprint
import wx.grid
from mini_tcm_scripter.sample_data import sample_med_store, sample_med_store_labels
from mini_tcm_scripter import NO_EDITOR


class InGrid(wx.grid.Grid):
    def __init__(self, parent, *args, **kwargs) -> None:
        super(InGrid, self).__init__(parent, *args, **kwargs)
        self.data = sample_med_store
        self.labels = sample_med_store_labels
        self.CreateGrid(10, len(self.labels))  # test purpose, can remove
        self.HideRowLabels()
        self.EnableDragColSize()
        self.set_cell_attributes()
        self.SetSelectionMode(self.GridSelectRows)
        #
        self.set_col_labels()
        
        self.fill_grid(self.data)
        #
        self.Layout()
        
        self.Bind(wx.EVT_SIZE, self.on_size)
        
    def on_size(self, event:wx.Event):
        width = event.GetSize()[0]
        for col, _v in enumerate(self.labels):
            self.SetColSize(col, width/len(self.labels))
        event.Skip()
        
        
    def set_cell_attributes(self):
        for i, v in enumerate(self.labels):
            self.SetColAttr(i, NO_EDITOR.Clone())     

    def set_col_labels(self):
        for i, label in enumerate(self.labels):
            self.SetColLabelValue(i, label)

    def fill_grid(self, data):
        if self.NumberRows > 0:
            self.DeleteRows(0, self.NumberRows)
        
        self.AppendRows(len(data))
        for r, row_val in enumerate(data):
            for k, value in row_val.items():
                col = self.labels.index(k)
                self.SetCellValue(r, col, str(value))
                
        # set new selection
        self.SelectRow(0)
        self.ShowScrollbars(wx.SHOW_SB_ALWAYS, wx.SHOW_SB_ALWAYS)
        
    def select_new_row(self, action:str):
        if self.NumberRows == 0:
            return
        
        selected_row = self.GetSelectedRows()[0]
        # print(action, selected_row)

        if action in ('U', 'u') and selected_row != 0:
            # print('select up')
            self.SelectRow(selected_row-1)
        elif action in ('D', 'd') and selected_row != self.NumberRows-1:
            # print('select down')
            self.SelectRow(selected_row+1)
        else:
            return
    
    @property
    def current_id(self)->int:
        """ Get id as integer """
        row = self.GetSelectedRows()[0]
        col = 0    # this should not change
        val = int(self.GetCellValue(row, col))

        return val
        

    def filter(self, search_phrase=''):
        search_phrase = search_phrase.partition(':')[0]
        if search_phrase == '':
            self.fill_grid(self.data)
        else:
            def make_pattern(orig_s):
                retval = ''
                for c in orig_s:
                    retval += c + '+.*'
                return retval
            
            # print('in grid to filter by:', search_phrase)
            pattern = make_pattern(search_phrase)
            
            new_data = []
            for odic in self.data:
                for k, v in odic.items():
                    if re.match(pattern.lower(), v.lower()):
                        new_data.append(odic)
                        break
            
            self.fill_grid(new_data)
        
