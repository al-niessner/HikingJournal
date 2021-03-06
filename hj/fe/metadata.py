'''GUI routines for attaching metadata to GPS elements
'''

from hj.fe import fapp

import flask
import hj.config
import hj.db
import hj.util.geo
import json
import logging; log = logging.getLogger(__name__)
import matplotlib.image
import os
import subprocess
import tempfile

@fapp.route ('/metadata/assign', methods=['PUT'])
def assign()->bytes:
    kwds = dict([(k, flask.request.args.get (k))
                 for k in flask.request.args.keys()]) # flask thing
    for k in filter (lambda k:k.endswith ('ids'),
                     kwds.keys()): kwds[k] = kwds[k].split (':')
    a = hj.Annotated(**kwds)
    facets = json.loads (flask.request.data.decode())
    a.update (dict([(f['key'],f['value']) for f in facets]))
    hj.db.archive (hj.db.EntryType.annot, a, a.get_fingerprint())
    return b''

@fapp.route ('/metadata/collate', methods=['GET'])
def collate()->bytes:
    content = {'map':{}, 'wids':[]}
    tid = flask.request.args.get ('tid')
    t = hj.db.fetch ([tid])[tid]
    ml = [m for m in filter (lambda m:m.any (t.get_points()),
                             hj.db.filter (hj.db.EntryType.map))]
    content['map']['constituents'] = sorted ([m.get_name() for m in ml])
    ws = hj.db.filter (hj.db.EntryType.waypt)
    for i in  hj.util.geo.indices (t, ws):
        content['wids'].append (ws[i].get_fingerprint())
        pass
    m = None if len (ml) == 0 else  hj.util.geo.Joined (ml=ml)

    if m is None or not m.all (t.get_points()):
        log.error ('Need to get some bloody maps from USGS!!!!!')
        log.error ('  track: ' + t.get_label())
        log.error ('  first: ' + str(t.get_points()[0].lat) + ' ' + str(t.get_points()[0].lon))
    else: # else should not be here when can autoload the maps
        m.overlay (t.get_points())
        coords = [] if len (content['wids']) == 0 else m.overlay \
                 ([w.get_points()[0] for w in
                   filter (lambda w:0 < content['wids'].
                           count (w.get_fingerprint()), ws)], True)
        content['map']['fingerprint'] = m.get_fingerprint()
        content['map']['waypts'] = coords
        fid,fn = tempfile.mkstemp (prefix='mdmap', suffix='.png')
        os.close (fid)
        matplotlib.image.imsave (fn, m.get_image())
        content['map']['name'] = fn
        pass
    return json.dumps (content).encode()

@fapp.route ('/metadata/facets', methods=['GET'])
def facets()->bytes:
    ad = dict([(a.get_track_fingerprint(), a.get_fingerprint())
               for a in hj.db.filter(hj.db.EntryType.annot)])
    content = []
    tid = flask.request.args.get ('tid')

    if tid in ad:
        a = hj.db.fetch ([ad[tid]])[ad[tid]]
        for k,v in sorted (a.get_facets().items(), key=lambda t:t[0]):
            content.append ({'key':k, 'value':v})
            pass
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
