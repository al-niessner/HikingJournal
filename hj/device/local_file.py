import hj.device
import os
import re
import shutil

class Interface(hj.device.Interface):
    '''Looks in the local file system for GPX files'''
    def __init__ (self, dir:str, follow:bool=False, recurse:bool=False,
                  rid:str='^[Rr]oute.*', tid:str='^[Tt]rack.*', wid:str='^[Ww]aypoint.*'):
        '''Construct an interface that allows access to the local file system

        dir : directory to look within
        follow : follow links when recurse is True
        recurse : descend into directories within the given directory

        rid : a regular expression for identifying route files
        tid : a regular expression for identifying track files
        wid : a regular expression for identifying waypoint files
        '''

        hj.device.Interface.__init__ (self)
        self.__base_dir = os.path.expanduser (os.path.expandvars (dir))
        self.__follow = follow
        self.__recurse = recurse
        self.__rregex = re.compile (rid)
        self.__tregex = re.compile (tid)
        self.__wregex = re.compile (wid)
        return

    def _add (self, dn, fns):
        for fn in fns:
            ffn = os.path.join (dn, fn)

            if self.__rregex.match (fn): self.__rfns.append (ffn)
            if self.__tregex.match (fn): self.__tfns.append (ffn)
            if self.__wregex.match (fn): self.__wfns.append (ffn)
            pass
        return

    def _clear(self):
        for fn in self.__rfns + self.__tfns + self.__wfns:
            if os.path.exists (fn): os.remove (fn)
            pass
        return
    
    def routes(self):
        for rfn in self.__rfns: yield rfn
        return
    
    def tracks(self):
        for tfn in self.__tfns: yield tfn
        return
    
    def update (self):
        '''walk the directories and find all of the items'''
        self.__rfns = []
        self.__tfns = []
        self.__wfns = []

        if self.__recurse:
            for p,d,f in os.walk (self.__base_dir, followlinks=self.__follow):
                self._add (p, f)
                pass
            pass
        else: self._add (self.__base_dir, os.listdir (self.__base_dir))

        self.__rfns.sort()
        self.__tfns.sort()
        self.__wfns.sort()
        return

    def waypoints(self):
        for wfn in self.__wfns: yield wfn
        return
    pass
