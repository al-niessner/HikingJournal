'''Root of the hiking journal'''

import cherrypy
import cherrypy.wsgiserver
import flask
import hj.fe.root
import os

fapp = flask.Flask(__name__)
fapp.debug = True

import hj.fe.forms
import hj.fe.js
import hj.fe.input
import hj.fe.pages

@fapp.route ('/')
def _root() -> bytes:
    return b'''
<!DOCTYPE html>
<html>
  <head>
    <script> 
      function frontEndShutdown()
      {
        document.getElementById("stop_server").submit();
        window.close();
      } 
    </script>
    <title>Hiking Journal</title>
  </head>
  <body>
    <form action="/pages/cover" style="float:left ; margin-right:10px" target="workspace"><input type="submit" value="Home"/></form>
    <form action="/import" style="float:left ; margin-right:10px" target="workspace"><input type="submit" value="Import"/></form>
    <form action="/scribe" style="float:left ; margin-right:10px" target="workspace"><input type="submit" value="Scribe Entry"/></form>
    <form action="/setup" style="float:left ; margin-right:10px" target="workspace"><input type="submit" value="Settup"/></form>
    <input style="float:left" type="button" value="Quit" onclick="frontEndShutdown();"/>
    <form id="stop_server" action="/stop"><input type="hidden" value="Stop"/></form>
    <iframe id="workspace"
            name="workspace"
            src="/pages/cover"
            style="border:medium solid black; height:95vh; width:90%;"/>
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
