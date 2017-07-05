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

    hj.config.dt = hj.device.Type.local_file.name
    hj.config.formatters = {'html':'hj.util.format.html',
                            'json':'hj.util.format.json',
                            'markdown':'hj.util.format.markdown'}
    hj.config.export = ['html', 'markdown']
    hj.config.garmin_etrex_10__mp = '${HOME}'
    hj.config.local_file__dir = '${HOME}'
    hj.config.templates = {'hdr':os.path.join (os.path.dirname (__file__),
                                               'util/templates/header.md'),
                           'nav':os.path.join (os.path.dirname (__file__),
                                               'util/templates/navigate.md'),
                           'seg':os.path.join (os.path.dirname (__file__),
                                               'util/templates/segment.md')}
    hj.config.viewer = '/usr/bin/eog'
    hj.config.wdir = '${HOME}/Hiking/Journal'
    return

def load (fn):
    fn = os.path.expanduser (os.path.expandvars (fn))
    initialize()
    if os.path.exists (fn):
        with open (fn, 'rt') as f:
            archive = json.load (f)
            for k in archive.keys(): setattr (hj.config, k, archive[k])
            pass
        pass

    hj.config.wdir = os.path.expanduser (os.path.expandvars (hj.config.wdir))
    if not os.path.exists (hj.config.wdir): os.makedirs (hj.config.wdir)
    return

def save (fn):
    archive = {}
    for n in _dir(): archive[n] = getattr (hj.config, n)
    fn = os.path.expanduser (os.path.expandvars (fn))
    with open (fn, 'wt') as f: json.dump (archive, f, indent=2)
    return
