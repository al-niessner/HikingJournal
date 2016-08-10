#! /usr/bin/env python3
'''Remove items from the database.'''

import argparse
import logging
import os
import sys

if __name__ == '__main__':
    sys.path.append (os.path.abspath (os.path.join (os.path.dirname (__file__),
                                                    '../..')))
    import hj.config
    import hj.db
    import hj.util.args

    ap = argparse.ArgumentParser(description='This tool allows the hiking journal system to be examined.')
    hj.util.args.base (ap)
    hj.util.args.db (ap, None)
    ap.add_argument ('-n', '--name', required=True, type=str,
                     help='entry name to remove')
    ap.add_argument ('-t', '--type', choices=[e.name for e in hj.db.EntryType],
                     required=True, help='type of entry to 1remove')
    args = ap.parse_args()
    hj.config.load (args.config_file)
    hj.config.wdir = args.working_dir if args.working_dir else hj.config.wdir
    items = [item for item in hj.db.seek ([args.name],
                                          hj.db.EntryType[args.type])]
    
    if len (items) == 0: print ('Did not find anything to remove. Maybe because the name and the type do not match?')
    else:
        for item in items:
            print ('Removing item: ' + item.get_label())
            hj.db.remove (hj.db.EntryType[args.type], item.get_fingerprint())
            pass
    pass
