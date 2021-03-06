#! /usr/bin/env python3
'''List help on all of the devices.'''

import argparse
import os
import sys

if __name__ == '__main__':
    sys.path.append (os.path.abspath (os.path.join (os.path.dirname (__file__),
                                                    '../..')))
    import hj.device
    import hj.util.args
    ap = argparse.ArgumentParser(description='List all of the available help for one or all of the devices currently supported by this project.')
    ap.add_argument ('-q', '--quiet', action='store_true', default=False,
                     required=False,
                     help='print just the available device types and exit')
    ap.add_argument ('-t', '--type', default=[], nargs='*',
                     type=hj.util.args.name2dtype,
                     help='list of device types that you would like to view with an empty list meaning all of them.')
    args = ap.parse_args()

    if args.quiet:
        for n in sorted ([t.name for t in hj.device.Type]): print (n)
        pass
    else:
        for t in hj.device.Type if len (args.type) == 0 else \
                sorted (list (set (args.type))): hj.device.open (t)
        pass
    pass
