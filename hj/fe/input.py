'''GUI pages for the various sources
'''

from hj.fe.root import fapp

import hj.fe.forms

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
      }
    </script>
    <title>Input Tracks and Waypoints</title>
  </head> 
  <body>
''' + hj.fe.forms.input_device() +  b'''
    <form>
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
