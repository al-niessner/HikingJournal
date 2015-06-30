'''Resused forms from various parts of the GUI
'''

from hj.fe import fapp

import json
import hj.config
import hj.device
import inspect

def input_device()->bytes:
    return b'''
<form>
  <label for="input_device">Input Device:</label>
  <select id="input_device" name="input_device" onchange="input_dev_change();">
    <option value="e">e</option>
    <option value="f">f</option>
  </select>
  <fieldset>
    <legend>Extra Parameters</legend>
    <div id="input_device_extras">
    </div>
  </fieldset>
</form>
'''

@fapp.route ('/input/extras/<device>', methods=['PUT'])
def input_device_extras (device:str) -> bytes:
    l = {}
    result = ''
    exec ('import hj.device.' + device + ' ; d = hj.device. ' +
          device + '.Interface', globals(), l)
    for p in filter (lambda p:p.name != 'self',
                     inspect.signature (l['d'].__init__).parameters.values()):
        label = p.name.replace ('_', ' ')
        val = getattr (hj.config, '__'.join ([device, p.name]), p.default)

        if isinstance (val, inspect._empty): val = None

        if p.annotation == bool:
            result += ('<input %s name="%s" type="checkbox"> %s </input><br/>' %
                       ('checked' if p.default else '', p.name, label))
        elif p.annotation == str:
            result += ('%s: <input name="%s" type="text" value="%s"/><br/>' %
                       (label, p.name, str (val)))
        else: result += '<h3>Un-handled type: %s</h3>' % str (p.annotation)
        pass

    if 0 < len (result):
        result = '<form>' + result + '<button onclick="input_dev_ready();" type="button">Scan</form>'

    return result.encode()

@fapp.route ('/input/device')
def input_device_json()->bytes:
    data = { 'all':sorted ([t.name for t in hj.device.Type]),
             'current':hj.config.dt}
    return json.dumps (data)
