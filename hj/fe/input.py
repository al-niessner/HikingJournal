'''GUI pages for the various sources
'''

from hj.fe import fapp

import flask
import hj.config
import hj.fe
import hj.fe.forms
import hj.fe.input
import json
import os

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

@fapp.route ('/import/move', methods=['PUT'])
def import_move_data()->bytes:
    xfer_info = json.loads (flask.request.data.decode())
    device_info = xfer_info['device']
    dt = hj.device.Type[device_info['type']]
    extras = hj.fe.forms.extras (dt.name, device_info['extras'])
    with _current (dt, **extras) as device:
        xfer = device.move if xfer_info['move'] else device.copy
        for fn in (xfer_info['routes'] +
                   xfer_info['tracks'] + xfer_info['waypts']):
            bn = os.path.basename (fn)
            xfer (fn, os.path.join (hj.config.wdir, bn))
            pass
        device.update()
        pass
    return b''

@fapp.route ('/import/scan', methods=['PUT'])
def import_scan_device()->bytes:
    device_info = json.loads (flask.request.data.decode())
    dt = hj.device.Type[device_info['type']]
    extras = hj.fe.forms.extras (dt.name, device_info['extras'])
    r,t,w = ['device failed'],['device failed'],['device failed']
    with _current (dt, **extras) as device:
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
