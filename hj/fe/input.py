'''GUI pages for the various sources
'''

from hj.fe import fapp

import flask
import gpxpy
import hashlib
import hj.db
import hj.config
import hj.fe
import hj.fe.forms
import hj.fe.input
import json
import os
import pickle
import shutil
import tempfile

_active = None
_signature = None
def _current (dt:hj.device.Type, **extras)->hj.device.Interface:
    signature = ';'.join ([dt.name] + [str(k) + '=' + str(v) for k,v in
                                       sorted (extras.items(),
                                               key=lambda i:i[0])])

    if _active is None:
        hj.fe.input._active = hj.device.open (dt, **extras)
        hj.fe.input._signature = signature
        pass

    if signature != hj.fe.input._signature:
        hj.device.close (_active)
        hj.fe.input._active = hj.device.open (dt, **extras)
        hj.fe.input._signature = signature
        pass
    
    return hj.fe.input._active

@fapp.route ('/import')
def import_gps()->bytes:
    return hj.fe._join (hj.fe._static ('/html/import.html'),
                        dev_form=hj.fe.forms.input_device())

@fapp.route ('/import/fetch', methods=['PUT'])
def import_fetch()->bytes:
    content = {'routes':[], 'tracks':[], 'waypts':[]}
    xfer_info = json.loads (flask.request.data.decode())
    device_info = xfer_info['device']
    dt = hj.device.Type[device_info['type']]
    extras = hj.fe.forms.extras (dt.name, device_info['extras'])
    with _current (dt, **extras) as device:
        for n in ['routes', 'tracks', 'waypts']:
            for fn in xfer_info[n]:
                data = device.fetch (fn, xfer_info['move']).read()
                gpx = gpxpy.parse (data)

                if 0 < gpx.get_points_no():
                    first = gpx.get_points_data()[0].point
                elif 0 < len (gpx.waypoints): first = gpx.waypoints[0]
                
                m = hashlib.md5()
                m.update (data.encode())
                s = hashlib.sha1()
                s.update (data.encode())
                content[n].append ({'data':data,
                                    'description':'',
                                    'dfn':os.path.basename (fn),
                                    'first':{'lat':first.latitude,
                                             'lon':first.longitude},
                                    'id':'%s_%s' % (m.hexdigest(),
                                                    s.hexdigest()),
                                    'label':''})
                pass
            pass
        device.update()
        pass
    return json.dumps (content).encode()

@fapp.route ('/import/ingest', methods=['PUT'])
def import_ingest()->bytes:
    content = json.loads (flask.request.data.decode())
    for k in ['routes', 'tracks', 'waypts']:
        for item in content[k]:
            fd,fn = tempfile.mkstemp()
            os.close (fd)
            with open (fn, 'wb') as f: pickle.dump (item, f)
            shutil.move (fn, os.path.join (hj.config.wdir, item['id']))
            hj.db.insert (hj.db.EntryType[k[:-1]], item['id'])
            pass
        pass
    return b''

@fapp.route ('/import/scan', methods=['PUT'])
def import_scan_device()->bytes:
    device_info = json.loads (flask.request.data.decode())
    dt = hj.device.Type[device_info['type']]
    extras = hj.fe.forms.extras (dt.name, device_info['extras'])
    r,t,w = ['device failed'],['device failed'],['device failed']
    with _current (dt, **extras) as device:
        device.update()
        r = [r for r in device.routes()]
        t = [t for t in device.tracks()]
        w = [w for w in device.waypoints()]
        pass
    return json.dumps ({'routes':r, 'tracks':t, 'waypts':w}).encode()

@fapp.route ('/import/wipe', methods=['PUT'])
def import_wipe_device()->bytes:
    device_info = json.loads (flask.request.data.decode())
    dt = hj.device.Type[device_info['type']]
    extras = hj.fe.forms.extras (dt.name, device_info['extras'])
    with _current (dt, **extras) as device: hj.device.close (device, True)
    return b''
