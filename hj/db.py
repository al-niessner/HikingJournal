'''Interface to database so that others can open/close all of it
'''

import enum
import hj.config
import os
import shelve

class EntryType(enum.Enum):
    entry = 3
    leg   = 5 # track, waypoint, pictures, etc
    map   = 4 # hj.Map instance
    raw   = 6 # raw files that other elements reference
    route = 0
    track = 1
    waypt = 2
    pass

def _open(): return shelve.open (os.path.join (hj.config.wdir, 'db'))

def archive (typ:EntryType, item, id:str=None):
    fd,fn = tempfile.mkstemp()
    os.close (fd)
    with open (fn, 'wb') as f: pickle.dump (item, f)
    shutil.move (fn, os.path.join (hj.config.wdir, item))
    # FIXME: need to compute the md5_sha1 id here if not already given
    assert (id is not None)
    insert (typ, id)
    return

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
