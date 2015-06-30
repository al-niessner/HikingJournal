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
