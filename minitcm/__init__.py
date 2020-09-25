import json
import shutil
import zlib
from datetime import datetime
from pathlib import Path


DEBUG = False
__version__ = '0.1.0'

# Directories
APP_DIR = Path(__file__).parent.resolve()
PROJ_DIR = APP_DIR.parent.resolve()
FONTS_DIR = Path(APP_DIR, 'resources', 'fonts').resolve()
SAMPLE_DIR = Path(APP_DIR , 'resources' , 'sample' , 'MiniTCM').resolve()
assert SAMPLE_DIR.exists()

if DEBUG:
    U_DIR = Path(PROJ_DIR , 'sample_hdir' , 'MiniTCM')    # $HOME/MiniTCM/, for testing
else:
    U_DIR = Path().home() / 'MiniTCM'    # usage directory, deploy

TEMPLATES_DIR = Path(U_DIR, 'templates').resolve()
CONFIG_FP = Path(U_DIR , 'config.toml').resolve()
DATA_DIR = Path(U_DIR, 'data').resolve()
PDFS_DIR = Path(U_DIR, 'pdfs').resolve()
PROFILES_DIR = Path(U_DIR, 'profiles').resolve()
RECORDS_DIR = Path(U_DIR, 'records').resolve()

if not U_DIR.exists():
    print('Creating directory for user:')
    print(U_DIR)
    shutil.copytree(SAMPLE_DIR, U_DIR.resolve())
    print(f'configure program at:\n{CONFIG_FP}')
print(f'configure program at:\n{CONFIG_FP}')

for d in [DATA_DIR, PDFS_DIR, PROFILES_DIR, RECORDS_DIR, TEMPLATES_DIR]:
    if not d.exists():
        d.mkdir()

# - - - - - #
def add_to_db(data):
    try:
        checksum = zlib.crc32(
            json.dumps(data, ensure_ascii=False).encode('utf-8')
            )
        Path(PROFILES_DIR / 'test.txt').write_text(json.dumps(data, ensure_ascii=False), encoding='utf-8')
        date_str = data['script']['date']
        file_name = '{}-{:02}.json'.format(
            datetime.fromisoformat(date_str).year,
            datetime.fromisoformat(date_str).month )

        fp =  RECORDS_DIR / file_name

        if not fp.exists():
            fp.write_text('[]', encoding='utf-8')

        obj_list = json.loads(fp.read_text('utf-8'))

        obj_list.append({'data': data, 'checksum': checksum})

        with open(fp, 'w', encoding='utf-8') as jsonfile:
            json.dump(obj_list, jsonfile, ensure_ascii=False, indent=4)
        return True
    except Exception as e:
        print('Error', e)
        return False

# constants for wx
import wx.grid


NO_EDITOR = wx.grid.GridCellAttr()
NO_EDITOR.SetReadOnly()
