#! /usr/bin/env python3
'''List all of the available routes, tracks, and waypoints.'''

import argparse
import os
import sys

def device (args : argparse.Namespace):
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
    import hj.device
    import hj.util.args
    ap = argparse.ArgumentParser(description='List all of the available routes, tracks, and waypoints over the given devices. Each device takes its own keywords for construction. Please use the tool "device" for getting details on device keywords. For this tool, each device will be followed by its -kw -kv switches.')
    sp = ap.add_subparsers(description='Allow the user to select the input source to search for valid GPX elements.', title='Input Sources')
    dap = hj.util.args.device_input (sp.add_parser('device',
                                                   help='read the GPX information directly from a device'),
                                     device)
    args = ap.parse_args()
    args.call (args)
    pass
