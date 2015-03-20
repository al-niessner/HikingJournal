'''General utilities for external units to access the front-end'''

import hj.fe.root
import twisted.internet.reactor
import webbrowser

def conjure (port : int) -> None:
    twisted.internet.reactor.callLater (0.10, hj.fe.util.spawn_browser, port)
    return

def spawn_browser (port : int) -> None:
    '''Open a browser or tab on a running browser'''
    webbrowser.open_new_tab ('http://localhost:' + str (port))
    return

