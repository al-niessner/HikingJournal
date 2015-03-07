#! /usr/bin/env python3
'''Start a front-end and invoke a browser page'''

import argparse
import os
import sys

def main (browser : str, port : int) -> None:
    hj.fe.util.conjure (browser, port)
    hj.fe.root.run (port)
    return

if __name__ == '__main__':
    sys.path.append (os.path.abspath (os.path.join (os.path.dirname (__file__),
                                                    '../..')))
    import hj.fe.root
    import hj.fe.util

    ap = argparse.ArgumentParser(description='Start the hiking journal. The journal uses the browser as its rendering engine. It uses the twisted platform to tie browswer actions back into modifying the journal data itself.')
    ap.add_argument ('-b', '--browser',
                     choices=[e.name for e in hj.fe.util.Browser],
                     default=hj.fe.util.Browser.chromium.name,
                     help='browser of choice to display the journal [%(default)s]')
    ap.add_argument ('-p', '--port', default=8080, type=int,
                     help='the socket port number for browser <-> journal communications [%(default)s]')
    args = ap.parse_args()
    main (args.browser, args.port)
    pass
else:
    import hj.fe.root
    import hj.fe.util
    pass
