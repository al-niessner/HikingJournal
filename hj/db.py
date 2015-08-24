'''Interface to database so that others can open/close all of it
'''

import enum
import hj.config
import os
import shelve

class EntryType(enum.Enum):
    entry = 3
    leg   = 5 # track, waypoint, pictures, etc
    quad  = 4
    route = 0
    track = 1
    waypt = 2
    pass

def _open(): return shelve.open (os.path.join (hj.config.wdir, 'db'))

def insert (et:EntryType, id:str):
    with _open() as db: db[id] = et
    return

def stats()->{}:
    result = {}
    with _open() as db: ets = [v for v in db.values()]
    result['total'] = len (ets)
    for et in EntryType: result[et.name] = ets.count (et)
    print (result)
    return result
