
import json
import os

def entry (outdir:str, name:str, prologue:str, segments:[str]):
    dfn = os.path.join (outdir, 'entry.json')
    try:
        with open (dfn, 'rt') as f: data = json.load (f)
    except: data = {}
    try: jp = json.loads (prologue)
    except:
        print ('Error decoding:')
        print (prologue)
        raise
    js = []
    for s in segments:
        try: js.append (json.loads (s))
        except:
            print ('Error decoding:')
            print (s)
            raise
        pass
    data[name] = {'prologue':jp, 'segments':js}
    with open (dfn, 'tw') as f: json.dump (data, f)
    return

def navigate (outdir:str, nav):
    dfn = os.path.join (outdir, 'navigation.json')
    try:
        with open (dfn, 'rt') as f: data = json.load (f)
    except: data = []
    try: data.append (json.loads (nav))
    except:
        print ('Error decoding:')
        print (nav)
        raise
    with open (dfn, 'tw') as f: json.dump (data, f)
    return
