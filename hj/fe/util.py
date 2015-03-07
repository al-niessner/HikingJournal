'''General utilities for external units to access the front-end'''

import enum
import hj.fe.root
import subprocess
import twisted.internet.reactor

class Browser(enum.Enum):
    chrome = 0
    chromium = 1
    firefox = 2
    pass

def conjure (browser : str, port : int) -> None:
    twisted.internet.reactor.callLater (0.10,
                                        hj.fe.util.spawn_browser,
                                        Browser[browser],
                                        port)
    return

def spawn_browser (browser : Browser, port : int) -> None:
    '''Open a browser or tab on a running browser'''
    name = browser.name
    url = 'http://localhost:' + str (port)
    cmd = [name, url]
    
    if browser == Browser.chromium: cmd[0] = 'chromium-browser'
    subprocess.Popen(cmd)
    return

