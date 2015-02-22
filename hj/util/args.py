'''Helper module for helping with argparse'''

import argparse
import hj.device

def ns2dict (args : argparse.Namespace) -> dict:
    result = vars (args).copy()
    if 'call' in result: del result['call']
    if 'parameters' in result:
        del result['parameters']
        result.update ([p.split ('=') for p in args.parameters])
        pass
    return result

def device_input (ap : argparse.ArgumentParser, call) -> argparse.ArgumentParser:
    '''add the common device block to the arg parser'''
    ap.add_argument
    ap.add_argument ('-t', '--type', dest='t', required=True, type=name2dtype,
                     help='the device type which can be found using "device.py"')
    ap.add_argument ('-p', '--parameters', default=[], nargs='*', type=kvpair,
                     help='device dependent parameters in the form of x=y')
    ap.set_defaults (call=call)
    return ap

def kvpair (s : str) -> str:
    if len (s.split ('=')) != 2:
        raise ValueError('The given input "' + s +
                         '" does not match the expected format of x=y')
    return s

def name2dtype (name : str) -> hj.device.Type:
    '''convert a name to a device type'''
    return hj.device.Type[name]
