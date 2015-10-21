'''Interface to database so that others can open/close all of it
'''

import enum
import hashlib
import hj.config
import os
import shelve
import subprocess

class EntryType(enum.Enum):
    entry = 3
    leg   = 5 # track, waypoint, pictures, etc
    map   = 4 # hj.Map instance
    raw   = 6 # raw files that other elements reference
    route = 0
    track = 1
    waypt = 2
    pass

def _id (data:bytes, id:str=None)->str:
    if id is None:
        m = hashlib.md5()
        m.update (data)
        s = hashlib.sha1()
        s.update (data)
        id = '%s_%s' % (m.hexdigest(), s.hexdigest())
        pass
    return id

def _open(): return shelve.open (os.path.join (hj.config.wdir, 'db'))

def _rid (fn:str)->str:
    m = subprocess.check_output ('md5sum', fn).decode().split()[0]
    s = subprocess.check_output ('sha1sum', fn).decode().split()[0]
    return '%s_%s' % (m, s)

def archive (typ:EntryType, item, id:str=None):
    '''Archive data into the database for later reference

    typ  : the type of data expected
    item : the actual data
    id   : optional ID of the data and when not given will be the md5_sha1
           checksums of 
    '''
    if typ is EntryType.raw: shutil.copy (item, os.path.join (hj.config.wdir,
                                                              _rid (item)))
    else:
        data = pickle.dumps (item, pickle.HIGHEST_PROTOCOL)
        with open (os.path.join (hj.config.wdir,
                                 _id (data, id)), 'wb') as f: f.write (data)
        pass

    insert (typ, id)
    return id

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
