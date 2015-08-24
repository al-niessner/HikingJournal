#! /usr/bin/env python3
'''List all of the available routes, tracks, and waypoints.'''

import argparse
import os
import sys

def db (args:argparse.Namespace):
    import hj.config
    import hj.db

    hj.config.wdir = args.working_dir
    print ('''
Database Statistics:
  Entries:   %(entry)d
  Legs:      %(leg)d
  Quads:     %(quad)d
  Routes:    %(route)d
  Tracks:    %(track)d
  Waypoints: %(waypt)d

  Total:     %(total)d
    ''' % hj.db.stats())
    return

def device (args : argparse.Namespace):
    import hj
    di = hj.device.open (**hj.util.args.ns2dict (args))
    print ('Routes:')
    for rfn in di.routes(): print ('   ' + rfn)
    print ('Tracks:')
    for tfn in di.tracks(): print ('   ' + tfn)
    print ('Waypoints:')
    for wfn in di.waypoints(): print ('   ' + wfn)
    return

if __name__ == '__main__':
    sys.path.append (os.path.abspath (os.path.join (os.path.dirname (__file__),
                                                    '../..')))
    import hj.util.args

    ap = argparse.ArgumentParser(description='This tool allows the hiking journal system to be examined.')
    sp = ap.add_subparsers(title='subsystem')
    dbap = hj.util.args.db (sp.add_parser('db',
                                          help='List statistics and information contained in the journal database.'),
                            db)
    dap = hj.util.args.device_input (sp.add_parser('device',
                                                   help='List all of the available routes, tracks, and waypoints over the given devices. Each device takes its own keywords for construction. Please use the tool "device" for getting details on device keywords. For this tool, each device will be followed by its -p switches.'),
                                     device)
    args = ap.parse_args()
    args.call (args)
    pass
