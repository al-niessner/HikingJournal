#! /usr/bin/env python3
'''Start a front-end and invoke a browser page'''

import argparse
import logging
import os
import sys

def log_level (l):
    """Allow log level to be symbolic or an integer"""
    try: ll = int(l)
    except: ll = eval (l)
    return ll

def main (config:str, port:int)->None:
    hj.config.load (config)
    hj.fe.util.conjure (port)
    hj.fe.run (port)
    hj.config.save (config)
    return

if __name__ == '__main__':
    sys.path.append (os.path.abspath (os.path.join (os.path.dirname (__file__),
                                                    '../..')))
    import hj.tool.start

    ap = argparse.ArgumentParser(description='Start the hiking journal. The journal uses the browser as its rendering engine. It uses the twisted platform to tie browswer actions back into modifying the journal data itself.')
    ap.add_argument ('-c', '--config-file', default='${HOME}/.hj.cnf',
                     help='location of the configuration file to use')
    ap.add_argument ('-l', '--log-file', default='${HOME}/.hj.log',
                     required=False,
                     help='the log filename [%(default)s]')
    ap.add_argument ('-L', '--log-level', default=logging.WARNING,
                     required=False, type=log_level,
                     help='set the log verbosity [logging.WARNING]')
    ap.add_argument ('-p', '--port', default=8080, type=int,
                     help='the socket port number for browser <-> journal communications [%(default)s]')
    args = ap.parse_args()
    logging.basicConfig (filename=os.path.expanduser
                         (os.path.expandvars (args.log_file)),
                         level=args.log_level)
    hj.tool.start.main (args.config_file, args.port)
    pass
else:
    import hj.config
    import hj.fe
    import hj.fe.util
    pass
