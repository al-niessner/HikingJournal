
import os

from hj.fe.root import fapp

@fapp.route ('/pages/cover/background.jpg')
def background() -> str:
    fn = os.path.join (os.path.join (os.path.dirname (__file__), 'resources'),
                       'background.jpg')
    with open (fn, 'rb') as f: img = f.read()
    return img

@fapp.route ('/pages/cover')
def cover() -> str:
    return b'''
<!DOCTYPE html>
<html>
  <head/>
  <body>
    <title>Hiking Journal Cover</title>
    <img src="/pages/cover/background.jpg"/>
  </body>
</html>
    '''
