'''Configuration of the hiking journal software'''

import hj.config
import json
import os

def initialize():
    import hj.config

    hj.config.wdir = '${HOME}/Hiking/Journal'
    return

def load (fn):
    if os.path.exists (fn):
        fn = os.path.expanduser (os.path.expandvars (fn))
        with open (fn, 'wt') as f:
            archive = json.load (f)
            hj.config.wdir = archive['wdir']
            pass
        pass
    else: initialize()

    hj.config.wdir = os.path.expanduser (os.path.expandvars (hj.config.wdir))
    if not os.path.exists (hj.config.wdir): os.makedirs (hj.config.wdir)
    return

def save (fn):
    archive = {'wdir':wdir}
    fn = os.path.expanduser (os.path.expandvars (fn))
    with open (fn, 'wt') as f: json.dump (archive, f, indent=2)
    return
