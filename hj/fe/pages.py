
import os

from hj.fe import fapp, _static

@fapp.route ('/resources/cover.jpg')
def background() -> bytes: return _static ('/resources/cover.jpg')

@fapp.route ('/pages/cover')
def cover() -> bytes:
    return b'''
<!DOCTYPE html>
<html>
  <head/>
  <body style="background-image:url('/resources/cover.jpg'); background-repeat:no-repeat; background-attachment:fixed">
    <title>Hiking Journal Cover</title>
    <h1 style="color:gold ; text-align:center">My Hiking Journal</h1>
  </body>
</html>
    '''
