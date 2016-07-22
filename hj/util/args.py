'''Helper module for helping with argparse'''

import argparse
import hj.device
import os

def _path (p:str)->str:
    if not os.path.exists (p):
        raise ValueError('The path "' + p + '" does not exist.')
    if not os.path.isdir (p):
        raise ValueError('The path "' + p + '" is not a directory.')
    return p

def ns2dict (args : argparse.Namespace) -> dict:
    result = vars (args).copy()
    if 'call' in result: del result['call']
    if 'parameters' in result:
        del result['parameters']
        result.update ([p.split ('=') for p in args.parameters])
        pass
    return result

def db (ap : argparse.ArgumentParser, call) -> argparse.ArgumentParser:
    '''add the common db args to the arg parser'''
    ap.add_argument ('-W', '--working-dir', required=True, type=_path,
                     help='the journals working directory where all of the data is kept')
    ap.add_argument ('-a', '--annotation-only', action='store_true',
                     default=False, required=False,
                     help='list the annotation names')
    ap.add_argument ('-e', '--entry-only', action='store_true',
                     default=False, required=False,
                     help='list the entry names')
    ap.add_argument ('-m', '--map-only', action='store_true',
                     default=False, required=False,
                     help='list the map names')
    ap.add_argument ('-p', '--photo-only', action='store_true',
                     default=False, required=False,
                     help='list the photo names')
    ap.add_argument ('-r', '--route-only', action='store_true',
                     default=False, required=False,
                     help='list the route names')
    ap.add_argument ('-t', '--track-only', action='store_true',
                     default=False, required=False,
                     help='list the track names')
    ap.add_argument ('-w', '--waypoint-only', action='store_true',
                     default=False, required=False,
                     help='list the waypoint names')
    ap.set_defaults (call=call)
    return ap

def device_input (ap : argparse.ArgumentParser, call) -> argparse.ArgumentParser:
    '''add the common device block to the arg parser'''
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
