'''Root of the hiking journal'''

import cherrypy
import cherrypy.wsgiserver
import flask
import hj.fe.root
import os

fapp = flask.Flask(__name__)
fapp.debug = True

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
    <h1>Cover</h1>
    <form action="input_device">
      <select name="device">
        <option value="0">Local File</option>
        <option value="1">Garmin eTrex 10</option>
      </select>
      <input type="submit" value="Connect"/>
    </form>
    <input type="button" value="Shutdown and Close" onclick="frontEndShutdown();"/>
    <form id="stop_server" action="/stop"><input type="hidden" value="Stop"/></form>
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
