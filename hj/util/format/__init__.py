
import hj.config
import importlib

def entry (f:str, outdir:str, name:str, prologue:str, segments:[str]):
    mod = importlib.import_module (hj.config.formatters[f])
    mod.entry (outdir, name, prologue, segments)
    return

def navigate (f:str, outdir:str, nav:str):
    mod = importlib.import_module (hj.config.formatters[f])
    mod.navigate (outdir, nav)
    return
