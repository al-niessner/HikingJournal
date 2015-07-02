'''GUI pages for the various sources
'''

from hj.fe import fapp

import flask
import hj.fe
import hj.fe.forms
import json

@fapp.route ('/import')
def import_gps()->bytes:
    return hj.fe._join (hj.fe._static ('/html/import.html'),
                        dev_form=hj.fe.forms.input_device())

@fapp.route ('/import/scan', methods=['PUT'])
def import_scan_device()->bytes:
    device_info = json.loads (flask.request.data.decode())
    dt = hj.device.Type[device_info['type']]
    extras = hj.fe.forms.extras (dt.name, device_info['extras'])
    routes,tracks = ['device failed'],['device failed']
    waypoints = ['device failed']
    with hj.device.open (dt, **extras) as device:
        routes = [r for r in device.routes()]
        tracks = [t for t in device.tracks()]
        waypoints = [w for w in device.waypoints()]
        pass
    return json.dumps ({'routes':routes,
                        'tracks':tracks,
                        'waypts':waypoints}).encode()
