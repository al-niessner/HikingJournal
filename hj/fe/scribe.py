'''GUI routines for attaching metadata to GPS elements
'''

from hj.fe import fapp

import flask
import hj
import hj.config
import hj.db
import hj.util.geo
import json
import logging; log = logging.getLogger(__name__)
import os

@fapp.route ('/scribe/a_and_e', methods=['GET'])
def a_and_e()->bytes:
    content = {'annots':sorted ([{'fingerprint':a.get_fingerprint(),
                                  'label':a.get_track().get_label()}
                                 for a in hj.db.filter (hj.db.EntryType.annot)],
                                key=lambda a:a['label']),
               'entries':sorted([{'fingerprint':e.get_fingerprint(),
                                  'label':e.get_label()}
                                 for e in hj.db.filter (hj.db.EntryType.entry)],
                                key=lambda e:e['label'])}
    return json.dumps (content).encode()

@fapp.route ('/scribe/load', methods=['GET'])
def scribe_load()->bytes:
    eid = flask.request.args.get ('eid')
    return json.dumps (hj.db.fetch ([eid])[eid].as_dict())

@fapp.route ('/scribe/new', methods=['PUT'])
def scribe_new()->bytes:
    ne = hj.Entry(flask.request.args.get ('aids').split (',')
                  if 0 < flask.request.args.get ('aids').find (',') else
                  [flask.request.args.get ('aids')],
                  flask.request.args.get ('label'))

    if not hj.db.contains (ne.get_fingerprint()):
        hj.db.archive (hj.db.EntryType.entry, ne, ne.get_fingerprint())
        pass
    
    return json.dumps ({'fingerprint':ne.get_fingerprint(),
                        'label':ne.get_label()}).encode()

@fapp.route ('/scribe/save', methods=['PUT'])
def scribe_save()->bytes:
    eid = flask.request.args.get ('eid')
    scribble = json.loads (flask.request.data.decode())
    entry = hj.db.fetch ([eid])[eid]
    entry.update (scribble)
    hj.db.archive (hj.db.EntryType.entry, entry, eid)
    return b''
