from pathlib import Path
PROJECTDIR = Path(__file__).parent.parent
print('project dir:', PROJECTDIR)
TEMPLATEDIR = Path(PROJECTDIR, 'templates')

import wx.grid
NO_EDITOR = wx.grid.GridCellAttr()
NO_EDITOR.SetReadOnly()


