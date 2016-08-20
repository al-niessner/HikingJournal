
import markdown
import os

def entry (outdir:str, name:str, prologue:str, segments:[str]):
    t = prologue
    for s in segments: t += s
    html = markdown.markdown (t)
    with open (os.path.join (outdir, name + '.html'), 'tw') as f: f.write (html)
    return

def navigate (outdir:str, nav):
    html = markdown.markdown (nav)
    with open (os.path.join (outdir, 'index.html'), 'tw') as f: f.write (html)
    return
