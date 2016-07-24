#! /usr/bin/env python3
'''Export journal elements to more end-user friendly forms'''

import argparse
import logging
import os
import sys

def _replace (t:str, this={}, segment={})->str:
    index = t.find ('${')
    while -1 < index:
        l = t.find ('}', index+2)

        if index < l:
            val = eval (t[index+2:l])
            t = t.replace (t[index:l+1], val)
        else: index += 2
        
        index = t.find ('${', index)
        pass
    return t

def entry (args):
    import hj.db
    import hj.util.format
    
    if not os.path.exists (args.output_dir): os.makedirs (args.output_dir)
    if not os.path.isdir (args.output_dir): raise ValueError('Given output path is not a directory.')
    
    with open (args.template_header, 'rt') as f: th = f.read()
    with open (args.template_segment, 'rt') as f: ts = f.read()
    for e in hj.db.seek (args.name, hj.db.EntryType.entry):
        this = e.as_dict()
        hdr = _replace (th, this)
        seg = [_replace (ts, this, s) for s in this['segs']]
        for f in args.format: hj.util.format.entry (f,
                                                    args.output_dir,
                                                    e.get_label(),
                                                    hdr, seg)
        pass
    return

if __name__ == '__main__':
    sys.path.append (os.path.abspath (os.path.join (os.path.dirname (__file__),
                                                    '../..')))
    import hj.config
    import hj.util.args

    ap = argparse.ArgumentParser(description='This tool allows the hiking journal to be exported to other forms.')
    hj.util.args.base (ap)
    hj.util.args.db (ap, None)
    sp = ap.add_subparsers(title='subsystem')
    iap = hj.util.args.entry (sp.add_parser('entry', help='Convert an entry to specified form'), entry)
    args = ap.parse_args()
    hj.config.load (args.config_file)
    hj.config.wdir = args.working_dir if args.working_dir else hj.config.wdir
    args.call (args)
    pass
