import json
import toml
import zlib
from pathlib import Path
from pprint import pprint
from datetime import datetime

DEBUG = True

# Directories
PROJ_DIR = Path(__file__).parent.parent.resolve()
FONTS_DIR = Path(PROJ_DIR, 'fonts').resolve()

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

print('- '*20)

for d in [U_DIR, DATA_DIR, PDFS_DIR, PROFILES_DIR, RECORDS_DIR, TEMPLATES_DIR]:
    if not d.exists():
        d.mkdir()


# - - - - - #
def add_to_db(data):
    try:
        checksum = zlib.crc32(
            json.dumps(data, ensure_ascii=False).encode('utf-8')
            )
        Path(PROFILES_DIR / 'test.txt').write_text(json.dumps(data, ensure_ascii=False))
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
