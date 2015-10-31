'''GUI routines for attaching metadata to GPS elements
'''

from hj.fe import fapp

import hj.db
import json

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
