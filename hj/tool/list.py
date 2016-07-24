#! /usr/bin/env python3
'''List all of the available routes, tracks, and waypoints.'''

import argparse
import logging
import os
import sys

def _db_display (title:str, l:[]):
    print (title + ' count is ' + str(len(l)) + ' and the names are:')
    for item in l: print ('   "' + item.get_label() + '"')
    return

def db (args:argparse.Namespace):
    import hj.config
    import hj.db

    if any([args.annotation_only, args.entry_only, args.map_only,
            args.photo_only, args.route_only, args.track_only,
            args.waypoint_only]):
        if args.annotation_only: _db_display ('Annotation', hj.db.filter
                                              (hj.db.EntryType.annot))
        if args.entry_only: _db_display ('Entry', hj.db.filter
                                         (hj.db.EntryType.entry))
        if args.map_only: _db_display ('Map', hj.db.filter
                                       (hj.db.EntryType.map))
        if args.photo_only: _db_display ('Photo', hj.db.filter
                                         (hj.db.EntryType.photo))
        if args.route_only: _db_display ('Route', hj.db.filter
                                         (hj.db.EntryType.route))
        if args.track_only: _db_display ('Track', hj.db.filter
                                         (hj.db.EntryType.track))
        if args.waypoint_only: _db_display ('Waypoint', hj.db.filter
                                            (hj.db.EntryType.waypt))
    else: print ('''
Database Statistics:
  Annotations %(annot)d
  Entries:    %(entry)d
  Maps:       %(map)d
  Photos:     %(photo)d
  Raw:        %(raw)d
  Routes:     %(route)d
  Tracks:     %(track)d
  Waypoints:  %(waypt)d

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
    import hj.config
    import hj.util.args

    ap = argparse.ArgumentParser(description='This tool allows the hiking journal system to be examined.')
    hj.util.args.base (ap)
    sp = ap.add_subparsers(title='subsystem')
    dbap = hj.util.args.db \
           (hj.util.args.select
            (sp.add_parser('db', help='List statistics and information contained in the journal database.')), db)
    dap = hj.util.args.device_input (sp.add_parser('device',
                                                   help='List all of the available routes, tracks, and waypoints over the given devices. Each device takes its own keywords for construction. Please use the tool "device" for getting details on device keywords. For this tool, each device will be followed by its -p switches.'),
                                     device)
    args = ap.parse_args()
    hj.config.load (args.config_file)
    hj.config.wdir = args.working_dir if args.working_dir else hj.config.wdir
    args.call (args)
    pass
