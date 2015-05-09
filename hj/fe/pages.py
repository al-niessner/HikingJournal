
import os

from hj.fe.root import fapp

@fapp.route ('/pages/cover/background.jpg')
def background() -> bytes:
    fn = os.path.join (os.path.join (os.path.dirname (__file__), 'resources'),
                       'background.jpg')
    with open (fn, 'rb') as f: img = f.read()
    return img

@fapp.route ('/pages/cover')
def cover() -> bytes:
    return b'''
<!DOCTYPE html>
<html>
  <head/>
  <body style="background-image:url('/pages/cover/background.jpg'); background-repeat:no-repeat; background-attachment:fixed">
    <title>Hiking Journal Cover</title>
    <h1 style="color:gold ; text-align:center">My Hiking Journal</h1>
  </body>
</html>
    '''
