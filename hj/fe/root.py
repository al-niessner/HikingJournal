'''Root of the hiking journal'''

import cherrypy
import cherrypy.wsgiserver
import flask
import hj.fe.root
import os

fapp = flask.Flask(__name__)
fapp.debug = True

import hj.fe.pages

@fapp.route ('/')
def _root() -> str:
    return b'''
<!DOCTYPE html>
<html>
  <head>
    <script language="javascript" type="text/javascript"> 
      function frontEndShutdown() { 
      document.getElementById("stop_server").submit();
      window.open('','_parent',''); 
      window.close();
      } 
    </script>
  </head>
  <body>
    <title>Hiking Journal</title>
    <form action="/pages/cover" target="workspace"><input type="submit" value="Home"/></form>
    <form action="/import/device" target="workspace"><input type="submit" value="Import"/></form>
    <form action="/entry/scribe" target="workspace"><input type="submit" value="Scribe Entry"/></form>
    <input type="button" value="Quit" onclick="frontEndShutdown();"/>
    <form id="stop_server" action="/stop"><input type="hidden" value="Stop"/></form>
    <iframe name="workspace"
            src="/pages/cover"
            style="border:medium solid black; height:90vh; width:90%;"/>
  </body>
</html>
'''

@fapp.route ('/stop')
def _stop() -> None:
    _server.stop()
    return b''

def run (port : int) -> None:
    d = cherrypy.wsgiserver.WSGIPathInfoDispatcher({'/': fapp})
    hj.fe.root._server = cherrypy.wsgiserver.CherryPyWSGIServer(('0.0.0.0', port), d)
    _server.start()
    return
