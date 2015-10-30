
import os

from hj.fe import fapp, _static

@fapp.route ('/resources/cover.jpg')
def background() -> bytes: return _static ('/resources/cover.jpg')

@fapp.route ('/pages/cover')
def cover() -> bytes: return _static ('/html/cover.html')

@fapp.route ('/pages/metadata')
def metadata() -> bytes: return _static ('/html/metadata.html')

@fapp.route ('/favicon.ico')
def favicon() -> bytes: return _static ('/resources/favicon.ico')

@fapp.route ('/photos/xmas.jpg')
def xmas()->bytes: return _static ('/resources/xmas.jpg')
