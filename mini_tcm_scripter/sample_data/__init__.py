import csv
from os import read
from pathlib import Path
from mini_tcm_scripter import PROJECTDIR

THISDIR = Path(__file__).parent

sample_med_prep = ['mp1', 'mp2', 'mp3']

sample_export_data = {
    "data": {
        "script": {
            "id": 1,
            "date": "2020-02-02T12:04:05",
            "unit": "g",
            "dangerous": "Normal",
            "footer": "generic footer generic footer generic footer generic footer generic footer ",
            "amount": 13,
            # "payment": "醫保"
        },
        "meds": [
            { "name": "med 101", "mass": 10 },
            { "name": "med 102", "mass": 10 },
            { "name": "med 103", "mass": 10 },
            { "name": "med 101", "mass": 10 },
            { "name": "med 102", "mass": 10 },
            { "name": "med 103", "mass": 10 },
            { "name": "med 101", "mass": 10 },
            { "name": "med 102", "mass": 10 },
            { "name": "med 103", "mass": 10 },
            { "name": "med 101", "mass": 10 },
            { "name": "med 102", "mass": 10 },
            { "name": "med 103", "mass": 10 },
            { "name": "med 104", "mass": 10 }
        ],
        "doctor": {
            "organisation": "第一GG銀行",
            "name": "严A医生"
        },
        "patient": {
            "name": "黃大明",
            "age": 10,
            "gender": "M",
            "contact": "07400111222"
        },
        "notes": [
            { "name": "west story", "content": "Stuff from western" },
            { "name": "east story", "content": "Stuff from eastern" },
            { "name": "instruction", "content": "Just eat this raw, ok?" }
        ]
    },
    "checksum": "12345"
}

sample_profile_1 = {
    'prep': ['mp1', 'mp2', 'mp3'],
    'prep.default': 'mp1',
    'unit': 'g',
}

sample_out_labels = ['id', 'name', 'method', 'mass']

# Data from csv
sample_med_store_labels = []
sample_med_store = []

with open(THISDIR / 'sample_meds_2020-05-26.csv', newline='') as csv_file:
    reader = csv.DictReader(csv_file, delimiter='\t')
    sample_med_store_labels = reader.fieldnames

    for line in reader:
        sample_med_store.append(line)
    
