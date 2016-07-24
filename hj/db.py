'''Interface to database so that others can open/close all of it
'''

import builtins
import enum
import hashlib
import hj.config
import hj.db
import os
import pickle
import shelve
import shutil
import subprocess

class EntryType(enum.Enum):
    annot = 5 # annotated track with other gps elements, maps, photos etc
    entry = 3
    map   = 4 # hj.Map instance
    photo = 7
    raw   = 6 # raw files that are referenced by either map or photo
    route = 0 # instance of hj.GPSElement
    track = 1 # instance of hj.GPSElement
    waypt = 2 # instance of hj.GPSElement
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

def _rid (fn:str, id:str=None)->str:
    if id is None:
        m = subprocess.check_output (['md5sum', fn]).decode().split()[0]
        s = subprocess.check_output (['sha1sum', fn]).decode().split()[0]
        id = '%s_%s' % (m, s)
        pass
    return id

def archive (typ:EntryType, item, id:str=None):
    '''Archive data into the database for later reference

    typ  : the type of data expected
    item : the actual data
    id   : optional ID of the data and when not given will be the md5_sha1
           checksums of 
    '''
    if typ is EntryType.raw:
        id =  _rid (item, id)
        shutil.copy (item, os.path.join (hj.config.wdir, id))
    else:
        data = pickle.dumps (item, pickle.HIGHEST_PROTOCOL)
        id = _id (data, id)
        with open (os.path.join (hj.config.wdir, id), 'wb') as f: f.write (data)
        pass

    insert (typ, id)
    return id

def contains (id:str)->bool:
    with _open() as db: result = id in db
    return result

def fetch (ids:[str])->{str:object}:
    '''Fetch particular items from the db and return it in a dictionary using same fps as the keys'''
    result = {}
    with _open() as db:
        for fn in ids:
            with open (os.path.join (hj.config.wdir, fn), 'rb') as f:
                result[fn] = pickle.load (f)
                pass
            pass
        pass
    return result

def filter (et:EntryType)->[]:
    '''Extract a specific data type out of the database
    '''
    result = []
    with _open() as db:
        for fn,et in builtins.filter(lambda i:i[1] == et, db.items()):
            with open (os.path.join (hj.config.wdir, fn), 'rb') as f:
                result.append (pickle.load (f))
                pass
            pass
        pass
    return result

def insert (et:EntryType, id:str):
    '''Insert an entry into the database'''
    with _open() as db: db[id] = et
    return

def seek (labels:[str], et:EntryType):
    '''Genertor to iterate over all types with a given set of labels'''
    for e in hj.db.filter (et):
        if e.get_label() in labels: yield e
        pass
    return

def stats()->{}:
    result = {}
    with _open() as db: ets = [v for v in db.values()]
    result['total'] = len (ets)
    for et in EntryType: result[et.name] = ets.count (et)
    return result

def update (id:str, item)->None:
    with open (os.path.join (hj.config.wdir, id), 'wb') as f:
        pickle.dump (item, f, pickle.HIGHEST_PROTOCOL)
        pass
    return
