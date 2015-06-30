'''Configuration of the hiking journal software'''

import hj.config
import hj.device
import json
import os

def _dir():
    ignore = ['_dir',
              'hj',
              'initialize',
              'json',
              'load',
              'os',
              'save']
    return [n for n in filter (lambda n:ignore.count (n) == 0 and
                               not n.startswith ('__') and
                               not n.endswith ('__'), dir (hj.config))]

def initialize():
    import hj.config

    hj.config.wdir = '${HOME}/Hiking/Journal'
    hj.config.dt = hj.device.Type.local_file.name
    hj.config.local_file__dir = '${HOME}'
    return

def load (fn):
    initialize()
    if os.path.exists (fn):
        fn = os.path.expanduser (os.path.expandvars (fn))
        with open (fn, 'wt') as f:
            archive = json.load (f)
            for k in archive.keys(): eval ('hj.config.' + k + ' = archive["' +
                                           k + '"]', globals(), locals())
            pass
        pass

    hj.config.wdir = os.path.expanduser (os.path.expandvars (hj.config.wdir))
    if not os.path.exists (hj.config.wdir): os.makedirs (hj.config.wdir)
    return

def save (fn):
    archive = {}
    for n in _dir(): archive[n] = eval ('hj.config.' + n, globals(), locals())
    fn = os.path.expanduser (os.path.expandvars (fn))
    with open (fn, 'wt') as f: json.dump (archive, f, indent=2)
    return
