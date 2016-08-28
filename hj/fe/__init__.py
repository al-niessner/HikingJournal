
'''Root of the hiking journal'''

import cherrypy
import cherrypy.wsgiserver
import flask
import hj.fe
import os

fapp = flask.Flask(__name__)
fapp.debug = True
vapp = flask.Flask(__name__)
vapp.debug = True

def _join (template:bytes, **kwds)->bytes:
    for k,v in kwds.items(): kwds[k] = v.decode()
    return (template.decode() % kwds).encode()

@fapp.route ('/')
def _root()->bytes: return _static ('/html/welcome.html')

@vapp.route ('/')
def _vroot()->bytes: return _static ('/index.html')

@vapp.route ('/<filename>')
def _ventry (filename)->bytes:
    return _static (filename)

@vapp.route ('/images/<filename>')
def _vimage (filename)->bytes:
    return _static ('images/' + filename)

def _static (fn:str)->bytes:
    while fn.startswith ('/'): fn = fn[1:]
    ffn = os.path.join (hj.fe._rootdir, fn)
    result = ('<h1>404 File Not Found</h1><p>Error finding static file: ' +
              ffn + '</p>').encode()
    with open (ffn, 'rb') as f: result = f.read()
    return result

@fapp.route ('/stop')
def _stop()->None:
    hj.fe._server.stop()
    return b''

@vapp.route ('/stop')
def _stop()->None:
    hj.fe._vserver.stop()
    return b''

def run (port:int)->None:
    import hj.fe.forms
    import hj.fe.js
    import hj.fe.input
    import hj.fe.metadata
    import hj.fe.pages
    import hj.fe.scribe
    import hj.fe.update
    import hj.fe.viewport

    d = cherrypy.wsgiserver.WSGIPathInfoDispatcher({'/':fapp})
    hj.fe._rootdir = os.path.dirname (os.path.abspath (__file__))
    hj.fe._server = cherrypy.wsgiserver.CherryPyWSGIServer(('0.0.0.0', port), d)
    hj.fe._server.start()
    return

def view (port:int, rdir:str)->None:
    d = cherrypy.wsgiserver.WSGIPathInfoDispatcher({'/':vapp})
    hj.fe._rootdir = rdir
    hj.fe._vserver = cherrypy.wsgiserver.CherryPyWSGIServer(('0.0.0.0', port),d)
    hj.fe._vserver.start()
    return
