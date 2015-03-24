'''General utilities for external units to access the front-end'''

import webbrowser

def conjure (port : int) -> None:
    '''Open a browser or tab on a running browser'''
    webbrowser.open_new_tab ('http://localhost:' + str (port))
    return

