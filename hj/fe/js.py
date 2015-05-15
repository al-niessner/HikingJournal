'''Reused scripts for the GUI
'''

from hj.fe import fapp

import hj.fe

@fapp.route ('/scripts/import.js')
def import_js() -> bytes: return hj.fe._static ('/scripts/import.js')

@fapp.route ('/scripts/input_dev.js')
def input_dev() -> bytes: return hj.fe._static ('/scripts/input_dev.js')
