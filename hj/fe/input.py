'''GUI pages for the various sources
'''

from hj.fe import fapp

import flask
import hj.fe
import hj.fe.forms
import json

@fapp.route ('/import')
def import_gps() -> bytes:
    return hj.fe._join (hj.fe._static ('/html/import.html'),
                        dev_form=hj.fe.forms.input_device())

@fapp.route ('/import/scan', methods=['PUT'])
def scan() -> bytes:
    request = json.loads (flask.request.data.decode())
    dt = hj.device.Type[request['device']]
    del request['device']
    dev = hj.device.open (dt, **request)
    return b'''hello'''
