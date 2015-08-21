'''Interface to database so that others can open/close all of it
'''

import enum
import hj.config
import os
import shelve

class EntryType(enum.Enum):
    entry = 3
    route = 0
    track = 1
    waypt = 2
    pass

def _open(): return shelve.open (os.path.join (hj.config.wdir, 'db'))

def insert (et:EntryType, id:str):
    with _open() as db: db[id] = et
    return
