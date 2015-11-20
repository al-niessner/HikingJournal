'''GUI routines for attaching metadata to GPS elements
'''

from hj.fe import fapp

import flask
import hj.db
import hj.util.geo
import json
import matplotlib.image

@fapp.route ('/metadata/collate', methods=['GET'])
def collate ()->bytes:
    content = {'map':{}, 'wids':[]}
    tid = flask.request.args.get ('tid')
    t = hj.db.fetch ([tid])[tid]
    ml = [m for m in filter (lambda m:m.any (t.get_points()),
                             hj.db.filter (hj.db.EntryType.map))]
    ws = hj.db.filter (hj.db.EntryType.waypt)
    for i in  hj.util.geo.indices (t, ws): # REF: 2, indices still is not right!
        content['wids'].append (ws[i].get_fingerprint())
        pass
    m = None if len (ml) == 0 else  hj.util.geo.Joined (ml=ml)
    
    if m is None or not m.all (t.get_points()):
        print ('Need to get some bloody maps from USGS!!!!!')
        print ('  track: ' + t.get_label())
    else: # else should not be here when can autoload the maps
        m.overlay (t.get_points())
        coords = [] if len (ws) == 0 else \
                 m.overlay ([w.get_points()[0] for w in ws], True)
        content['map']['fingerprint'] = m.get_fingerprint()
        content['map']['waypts'] = coords
        matplotlib.image.imsave ('/tmp/overlay.png', m.get_image())
        pass
    return json.dumps (content).encode()

@fapp.route ('/metadata/photos', methods=['GET'])
def photos()->bytes:
    content = [w.as_dict() for w in hj.db.filter (hj.db.EntryType.photo)]
    return json.dumps (content).encode()

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
