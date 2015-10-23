
import os

def homogenize (sdir:str, recurse:bool):
    if recurse:
        for [dp, dns, fns] in os.walk (sdir):
            for fn in fns: yield (dp, fn)
            pass
    else:
        fns = os.listdir (sdir)
        for fn in fns: yield (sdir, fn)
        pass
    return
