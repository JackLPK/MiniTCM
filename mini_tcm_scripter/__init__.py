from pathlib import Path
from pprint import pprint

DEBUG = True

# Directories
PROJECTDIR = Path(__file__).parent.parent.resolve()
print('project dir:', PROJECTDIR)

FONTS_DIR = Path(PROJECTDIR, 'fonts').resolve()
print('fonts dir:', FONTS_DIR)
assert FONTS_DIR.exists()

if DEBUG:
    U_DIR = Path(PROJECTDIR, 'sample_hdir') / 'MiniTCM'    # $HOME/MiniTCM/, for testing
else:
    U_DIR = Path().home() / 'MiniTCM'    # usage directory, deploy

if not U_DIR.exists():
    U_DIR.mkdir()
print('u dir:', U_DIR)
assert U_DIR.exists()

TEMPLATES_DIR = Path(U_DIR, 'templates').resolve()
assert TEMPLATES_DIR.exists()

CONFIG_FP = U_DIR / 'config.toml'
assert CONFIG_FP.exists()

DATA_DIR = Path(U_DIR, 'data').resolve()
print('data dir:', DATA_DIR)
assert DATA_DIR.exists()

PDFS_DIR = Path(U_DIR, 'pdfs').resolve()
print('pdfs dir:', PDFS_DIR)
assert PDFS_DIR.exists()

PROFILES_DIR = Path(U_DIR, 'profiles').resolve()
print('profiles dir:', PROFILES_DIR)
assert PROFILES_DIR.exists()

RECORDS_DIR = Path(U_DIR, 'records').resolve()
print('records dir:', RECORDS_DIR)
assert RECORDS_DIR.exists()

# constants for wx
import wx.grid
NO_EDITOR = wx.grid.GridCellAttr()
NO_EDITOR.SetReadOnly()


