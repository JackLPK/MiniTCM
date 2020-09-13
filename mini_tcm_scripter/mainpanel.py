import wx
import wx.grid
from mini_tcm_scripter.infopanel import InfoPanel
from mini_tcm_scripter.ingrid import InGrid
from mini_tcm_scripter.outgrid import OutGrid


class MainPanel(wx.Panel):
    def __init__(self, parent, *args, **kwargs) -> None:
        super(MainPanel, self).__init__(parent, *args, **kwargs)
        self.statusbar = parent.statusbar
        self.search_bar = wx.TextCtrl(self, style=wx.TE_PROCESS_ENTER)

        self.in_grid = InGrid(self)
        self.out_grid = OutGrid(self)

        self.info_panel = InfoPanel(self)
        # self.bpanel = BPanel(self)
        
        self.set_layout()
        self.set_binding()
        
    def set_layout(self):

        # top bar area
        sizer_1 = wx.BoxSizer()
        sizer_1.Add((50, -1), 1)
        sizer_1.Add(self.search_bar, 3, flag=wx.ALL, border=5)
        sizer_1.Add((50, -1), 2)
        sizer_1.Add((50, -1), 1)
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
        self.info_panel.btn_preview.Bind(wx.EVT_BUTTON, lambda: print('hi'))

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
    