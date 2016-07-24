
import os

def entry (outdir:str, name:str, prologue:str, segments:[str]):
    with open (os.path.join (outdir, name + '.md'), 'tw') as f:
        f.write (prologue)
        for s in segments:
            f.write ('\n')
            f.write (s)
            pass
        pass
    return
