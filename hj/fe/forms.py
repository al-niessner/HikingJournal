'''Resused forms from various parts of the GUI
'''

from hj.fe.root import fapp

import json
import hj.config
import hj.device

def input_device() -> bytes:
    return b'''
<form>
  <label for="input_device">Input Device:</label>
  <select id="input_device" name="input_device" onchange="input_dev_change();">
    <option value="e">e</option>
    <option value="f">f</option>
  </select>
</form>
'''

@fapp.route ('/input/device')
def input_device_json() -> bytes:
    data = { 'all':sorted ([t.name for t in hj.device.Type]),
             'current':hj.config.dt}
    return json.dumps (data)
