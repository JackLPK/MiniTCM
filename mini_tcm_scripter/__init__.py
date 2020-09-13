from pathlib import Path
# Directories
PROJECTDIR = Path(__file__).parent.parent.resolve()
print('project dir:', PROJECTDIR)
TEMPLATEDIR = Path(PROJECTDIR, 'templates').resolve()
assert TEMPLATEDIR.exists()
SAMPLEDATA_DIR = Path(PROJECTDIR, 'sample_data').resolve()
print('sample dir:', SAMPLEDATA_DIR)
assert SAMPLEDATA_DIR.exists()


# constants for wx
import wx.grid
NO_EDITOR = wx.grid.GridCellAttr()
NO_EDITOR.SetReadOnly()


