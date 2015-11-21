'''GUI routines for attaching metadata to GPS elements
'''

from hj.fe import fapp

import flask
import hj.config
import hj.db
import hj.util.geo
import json
import matplotlib.image
import os
import subprocess
import tempfile

@fapp.route ('/metadata/collate', methods=['GET'])
def collate ()->bytes:
    content = {'map':{}, 'wids':[]}
    tid = flask.request.args.get ('tid')
    t = hj.db.fetch ([tid])[tid]
    ml = [m for m in filter (lambda m:m.any (t.get_points()),
                             hj.db.filter (hj.db.EntryType.map))]
    ws = hj.db.filter (hj.db.EntryType.waypt)
    for i in  hj.util.geo.indices (t, ws):
        content['wids'].append (ws[i].get_fingerprint())
        pass
    m = None if len (ml) == 0 else  hj.util.geo.Joined (ml=ml)

    if m is None or not m.all (t.get_points()):
        print ('Need to get some bloody maps from USGS!!!!!')
        print ('  track: ' + t.get_label())
    else: # else should not be here when can autoload the maps
        m.overlay (t.get_points())
        coords = [] if len (ws) == 0 else m.overlay ([w.get_points()[0] for w in
              filter (lambda w:0 < content['wids'].count (w.get_fingerprint()),
                      ws)], True)
        content['map']['fingerprint'] = m.get_fingerprint()
        content['map']['waypts'] = coords
        fid,fn = tempfile.mkstemp (prefix='mdmap', suffix='.png')
        os.close (fid)
        matplotlib.image.imsave (fn, m.get_image())
        content['map']['name'] = fn
        pass
    return json.dumps (content).encode()

@fapp.route ('/metadata/load/<path:fn>', methods=['GET'])
def load (fn:str)->bytes:
    img = b''

    if not fn.startswith ('/'): fn = os.path.join ('/', fn)
    if os.path.isfile (fn):
        with open (fn, 'rb') as f: img = f.read()
        pass
    return img

@fapp.route ('/metadata/photos', methods=['GET'])
def photos()->bytes:
    content = [w.as_dict() for w in hj.db.filter (hj.db.EntryType.photo)]
    return json.dumps (content).encode()

@fapp.route ('/metadata/spawn/<path:fn>', methods=['PUT'])
def spawn (fn:str)->bytes:
    if not fn.startswith ('/'): fn = os.path.join ('/', fn)
    if os.path.isfile (fn): subprocess.Popen([hj.config.viewer, fn])
    return b''

@fapp.route ('/metadata/tracks', methods=['GET'])
def tracks()->bytes:
    a = [a.get_track_fingerprint() for a in hj.db.filter(hj.db.EntryType.annot)]
    content = {'barren':[], 'annotated':[]}
    for t in hj.db.filter (hj.db.EntryType.track):
        if 0 < a.count (t.get_fingerprint()):
            content['annotated'].append (t.as_dict())
        else: content['barren'].append (t.as_dict())
        pass
    content['annotated'].sort (key=lambda t:t['label'])
    content['barren'].sort (key=lambda t:t['label'])
    return json.dumps (content).encode()

@fapp.route ('/metadata/waypts', methods=['GET'])
def waypts()->bytes:
    content = [w.as_dict() for w in hj.db.filter (hj.db.EntryType.waypt)]
    content.sort (key=lambda w:w['label'])
    return json.dumps (content).encode()
