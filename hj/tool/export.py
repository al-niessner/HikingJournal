#! /usr/bin/env python3
'''Export journal elements to more end-user friendly forms'''

import argparse
import logging
import os
import shutil
import sys

def _entry (e, fmt, idir, odir, th, ts):
    e.write_images (idir)
    this = e.as_dict()
    hdr = _replace (th, this)
    seg = [_replace (ts, this, s) for s in this['segs']]
    for f in fmt: hj.util.format.entry (f, odir, e.get_label(), hdr, seg)
    return

def _navigate (el, fmt, idir, odir, nv):
    vals = {}
    for line in nv.split('\n'):
        if -1 < line.find ('${'): vals[line] = []
        pass
    for e in sorted (el, key=lambda k:k.get_label()):
        for l in vals.keys(): vals[l].append (_replace (l, e.as_dict(), item=e))
        pass
    for l,v in vals.items(): nv = nv.replace (l, '\n'.join (vals[l]))
    for f in fmt: hj.util.format.navigate (f, odir, nv)
    return

def _replace (t:str, this={}, segment={}, item=None)->str:
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

def _viewer (bdir, port):
    print (bdir, port)
    hj.fe.util.conjure (port)
    hj.fe.view (port, bdir)
    return

def entry (args):
    import hj.db
    import hj.util.format
    
    if not os.path.exists (args.output_dir): os.makedirs (args.output_dir)
    if not os.path.isdir (args.output_dir): raise ValueError('Given output path is not a directory.')

    image_dir = os.path.join (args.output_dir, 'images')
    if not os.path.isdir (image_dir): os.makedirs (image_dir)
    
    with open (args.template_header, 'rt') as f: th = f.read()
    with open (args.template_segment, 'rt') as f: ts = f.read()
    for e in hj.db.seek (args.name, hj.db.EntryType.entry): \
        _entry (e, args.format, image_dir, args.output_dir, th, ts)
    return

def journal (args):
    import hj.db
    import hj.fe
    import hj.fe.util
    import hj.util.format
    
    if not os.path.exists (args.output_dir): os.makedirs (args.output_dir)
    if not os.path.isdir (args.output_dir): raise ValueError('Given output path is not a directory.')

    image_dir = os.path.join (args.output_dir, 'images')
    if not os.path.isdir (image_dir): os.makedirs (image_dir)

    with open (args.template_navigate, 'rt') as f: nv = f.read()
    with open (args.template_header, 'rt') as f: th = f.read()
    with open (args.template_segment, 'rt') as f: ts = f.read()
    items = hj.db.filter (hj.db.EntryType.entry)
    _navigate (items, args.format, image_dir, args.output_dir, nv)
    for item in items: \
        _entry (item, args.format, image_dir, args.output_dir, th, ts)
    favicon = os.path.abspath (os.path.join (os.path.join
                                             (os.path.dirname (__file__),
                                              '..'),
                                             'fe/resources/favicon.ico'))
    shutil.copy (favicon, args.output_dir)
    if args.view: _viewer (args.output_dir, args.port)
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
    eap = hj.util.args.entry (sp.add_parser('entry', help='Convert an entry to specified form'), entry)
    jap = hj.util.args.journal (sp.add_parser('journal', help='Convert the entire journal specified form'), journal)
    args = ap.parse_args()
    hj.config.load (args.config_file)
    hj.config.wdir = args.working_dir if args.working_dir else hj.config.wdir
    args.call (args)
else:
    import hj.config
    import hj.db
    import hj.util.format
    pass
