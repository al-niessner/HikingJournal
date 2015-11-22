
'''GUI routines for using maps.google.com to show the track and waypoints
'''

from hj.fe import fapp

import flask
import hj.db
import json

@fapp.route ('/viewport/fetch', methods=['GET'])
def fetch()->bytes:
    id = flask.request.args.get ('id')
    gpsdata = [(p.lat, p.lon) for p in (hj.db.fetch ([id])[id]).get_points()]
    return json.dumps (gpsdata).encode()

@fapp.route ('/viewport/open', methods=['GET'])
def open()->bytes:
    id = flask.request.args.get ('id')
    return ('<!DOCTYPE html><html><head><script src="https://maps.googleapis.com/maps/api/js"></script><script src="/scripts/viewport.js"></script><title>GPS Data on Google Maps</title><style>html, body {height: 100%%;margin: 0;padding: 0;} #map_canvas {height: 100%%;}</style></head><body onload="viewport_init(\'%s\');"><div id="map_canvas"></div></body></html>' % id).encode()
