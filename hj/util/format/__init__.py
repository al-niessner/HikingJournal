
import hj.config
import importlib

def entry (f:str, outdir:str, name, prologue, segments):
    mod = importlib.import_module (hj.config.formatters[f])
    mod.entry (outdir, name, prologue, segments)
    return
