'''Update the readable journal
'''

from hj.fe import fapp

import flask
import hj
import hj.config
import hj.db
import hj.tool.export
import os

@fapp.route ('/update', methods=['GET'])
def journal():
    bdir = os.path.join (hj.config.wdir, 'pages')
    idir = os.path.join (bdir, 'images')
    
    if not os.path.isdir (bdir): os.makedirs (bdir)
    if not os.path.isdir (idir): os.makedirs (idir)

    items = hj.db.filter (hj.db.EntryType.entry)
    with open (hj.config.templates['hdr'], 'rt') as f: th = f.read()
    with open (hj.config.templates['nav'], 'rt') as f: nv = f.read()
    with open (hj.config.templates['seg'], 'rt') as f: ts = f.read()
    hj.tool.export._navigate (items, hj.config.export, idir, bdir, nv)
    for item in items:\
        hj.tool.export._entry(item, hj.config.export, idir, bdir, th, ts)
    return b''
