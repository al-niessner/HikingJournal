
'''Root of the hiking journal'''

import cherrypy
import cherrypy.wsgiserver
import flask
import hj.fe
import os

fapp = flask.Flask(__name__)
fapp.debug = True

def _join (template : bytes, **kwds) -> bytes:
    for k,v in kwds.items(): kwds[k] = v.decode()
    return (template.decode() % kwds).encode()

@fapp.route ('/')
def _root() -> bytes: return _static ('/html/welcome.html')

def _static (fn : str) -> bytes:
    while fn.startswith ('/'): fn = fn[1:]
    ffn = os.path.join (os.path.dirname (os.path.abspath (__file__)), fn)
    result = ('<h1>404 File Not Found</h1><p>Error finding static file: ' +
              ffn + '</p>').encode()
    with open (ffn, 'rb') as f: result = f.read()
    return result

@fapp.route ('/stop')
def _stop() -> None:
    hj.fe._server.stop()
    return b''

def run (port : int) -> None:
    import hj.fe.forms
    import hj.fe.js
    import hj.fe.input
    import hj.fe.pages
    
    d = cherrypy.wsgiserver.WSGIPathInfoDispatcher({'/': fapp})
    hj.fe._server = cherrypy.wsgiserver.CherryPyWSGIServer(('0.0.0.0', port), d)
    hj.fe._server.start()
    return
