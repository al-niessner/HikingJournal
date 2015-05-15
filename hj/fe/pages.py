
import os

from hj.fe import fapp, _static

@fapp.route ('/resources/cover.jpg')
def background() -> bytes: return _static ('/resources/cover.jpg')

@fapp.route ('/pages/cover')
def cover() -> bytes: return _static ('/html/cover.html')

