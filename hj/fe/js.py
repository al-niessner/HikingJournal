'''Reused scripts for the GUI
'''

from hj.fe import fapp

import hj.fe

@fapp.route ('/scripts/gpsi.js')
def gpsi_js() -> bytes: return hj.fe._static ('/scripts/gpsi.js')

@fapp.route ('/scripts/import.js')
def import_js() -> bytes: return hj.fe._static ('/scripts/import.js')

@fapp.route ('/scripts/input_dev.js')
def input_dev() -> bytes: return hj.fe._static ('/scripts/input_dev.js')

@fapp.route ('/scripts/metadata.js')
def metadata_js() -> bytes: return hj.fe._static ('/scripts/metadata.js')

@fapp.route ('/scripts/viewport.js')
def viewport_js() -> bytes: return hj.fe._static ('/scripts/viewport.js')

