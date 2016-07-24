'''Helper module for helping with argparse'''

import argparse
import hj.device
import logging
import os

def _filename (fn:str)->str:
    if not os.path.exists (fn):
        raise ValueError('A file wth the filename "' + fn + '" does not exist.')
    if not os.path.isfile (fn):
        raise ValueError('The file wth the filename "' + fn +
                         '" is not a regulear file')
    return fn

def _log_level (l):
    """Allow log level to be symbolic or an integer"""
    try: ll = int(l)
    except: ll = eval (l)
    return ll

def _path (p:str)->str:
    if not os.path.exists (p):
        raise ValueError('The path "' + p + '" does not exist.')
    if not os.path.isdir (p):
        raise ValueError('The path "' + p + '" is not a directory.')
    return p

def ns2dict (args:argparse.Namespace) -> dict:
    result = vars (args).copy()
    if 'call' in result: del result['call']
    if 'parameters' in result:
        del result['parameters']
        result.update ([p.split ('=') for p in args.parameters])
        pass
    return result

def base (ap:argparse.ArgumentParser, lfn:str=None)->argparse.ArgumentParser:
    ap.add_argument ('-c', '--config-file', default='${HOME}/.hj.cnf',
                     help='location of the configuration file to use')
    ap.add_argument ('-l', '--log-file', default=lfn,
                     required=False,
                     help='the log filename [%(default)s]')
    ap.add_argument ('-L', '--log-level', default=logging.WARNING,
                     required=False, type=_log_level,
                     help='set the log verbosity [logging.WARNING]')
    return ap

def db (ap:argparse.ArgumentParser, call)->argparse.ArgumentParser:
    '''add the common db args to the arg parser'''
    ap.add_argument ('-W', '--working-dir', default=None,  type=_path,
                     help='the journals working directory where all of the data is kept')
    ap.set_defaults (call=call)
    return ap

def device_input (ap:argparse.ArgumentParser, call) -> argparse.ArgumentParser:
    '''add the common device block to the arg parser'''
    ap.add_argument ('-t', '--type', dest='t', required=True, type=name2dtype,
                     help='the device type which can be found using "device.py"')
    ap.add_argument ('-p', '--parameters', default=[], nargs='*', type=kvpair,
                     help='device dependent parameters in the form of x=y')
    ap.set_defaults (call=call)
    return ap

def entry (ap:argparse.ArgumentParser, call) -> argparse.ArgumentParser:
    '''add the specific entry conversion arguments'''
    ap.add_argument ('-f', '--format', nargs='+', required=True,
                     choices=['html','markdown'],
                     help='one or more of the possible export formats')
    ap.add_argument ('-n', '--name', nargs='+', required=True, type=str,
                     help='one of more entry names')
    ap.add_argument ('-O', '--output-dir', required=True,
                     help='deposit all of the transforms into this directory')
    ap.add_argument ('-s', '--template-segment',
                     default=os.path.join (os.path.dirname (__file__),
                                           'templates/segment.md'),
                     required=False, type=_filename,
                     help='template in markdown for each segment')
    ap.add_argument ('-t', '--template-header',
                     default=os.path.join (os.path.dirname (__file__),
                                           'templates/header.md'),
                     required=False, type=_filename,
                     help='template in markdown for an entry header')
    ap.set_defaults (call=call)
    return ap

def kvpair (s:str) -> str:
    if len (s.split ('=')) != 2:
        raise ValueError('The given input "' + s +
                         '" does not match the expected format of x=y')
    return s

def name2dtype (name:str) -> hj.device.Type:
    '''convert a name to a device type'''
    return hj.device.Type[name]

def select (ap:argparse.ArgumentParser) -> argparse.ArgumentParser:
    '''add the ability to select specific items'''
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
    return ap
