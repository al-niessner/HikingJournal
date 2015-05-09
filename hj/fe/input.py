'''GUI pages for the various sources
'''

from hj.fe.root import fapp

import flask
import hj.fe.forms
import json

@fapp.route ('/import')
def dev_select() -> bytes:
    return b'''<!DOCTYPE html> 
<html>
  <head>
    <script src="/input_dev.js"></script>
    <script>
      window.onload = function ()
      {
        input_dev_init();
      }

      function input_dev_change()
      {
        console.log ("change");
        console.log (document.getElementById ("input_device").value);

        var connection = new XMLHttpRequest();
        connection.onreadystatechange = function()
        {
          if (connection.readyState == 4 && connection.status == 200)
          {
            console.log ("got something from the put");
            console.log (connection.responseText);
          }
        }
        connection.open("PUT", "/import/scan" , true);
        connection.send(JSON.stringify ({device:document.getElementById ("input_device").value}));
      }
    </script>
    <title>Input Tracks and Waypoints</title>
  </head> 
  <body>
''' + hj.fe.forms.input_device() +  b'''
    <form>
      <label for="routes">Routes</label>
      <select id="routes" multiple="multiple" name="routes">
        <option value="g">g</option>
        <option value="h">h</option>
      </select>
      <label for="tracks">Tracks</label>
      <select id="tracks" multiple="multiple" name="tracks">
        <option value="a">a</option>
        <option value="b">b</option>
      </select>
      <label for="waypoints">Waypoints</label>
      <select id="waypoints" multiple="multiple" name="waypoints">
        <option value="c">c</option>
        <option value="d">d</option>
      </select>
    </form>
  </body>
</html> 
'''
@fapp.route ('/import/scan', methods=['PUT'])
def scan() -> bytes:
    request = json.loads (flask.request.data.decode())
    dt = hj.device.Type[request['device']]
    del request['device']
    dev = hj.device.open (dt, **request)
    return b'''hello'''
