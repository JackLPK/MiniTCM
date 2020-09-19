import json
import toml
import zlib
from pathlib import Path
from pprint import pprint
from datetime import datetime

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

print('- '*20)

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


