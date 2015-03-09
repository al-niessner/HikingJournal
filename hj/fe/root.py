'''Root of the hiking journal'''

import os
import twisted.web.resource
import twisted.web.server

class Root(twisted.web.resource.Resource):
    def getChild (self, name, request):
        print ('Root.getChild().name:    ' + str(name))
        print ('Root.getChild().request: ' + str(request))
        return
    pass

class FavIcon(twisted.web.resource.Resource):
    isLeaf = True
    def render_GET (self, request):
        data = b''
        with open (os.path.abspath (os.path.join (os.path.dirname (__file__),
                                                  'resources/favicon.ico')),
                   'rb') as f: data = f.read()
        return data
    pass

class FrontPage(twisted.web.resource.Resource):
    isLeaf = True
    def render_GET (self, request): return b'''
<!DOCTYPE html>
<html>
  <body>
    <title>Hiking Journal</title>
    <h1>Cover</h1>
  </body>
</html>
'''
    pass

def run (port : int) -> None:
    '''Start up the twisted engine as the front-end'''
    root = Root()
    root.putChild (b'', FrontPage())
    root.putChild (b'favicon.ico', FavIcon())
    factory = twisted.web.server.Site(root)
    twisted.internet.reactor.listenTCP (port, factory)
    twisted.internet.reactor.run()
    return
