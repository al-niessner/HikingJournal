import hj.device
import os
import re

class Interface(hj.device.Interface):
    '''Looks in the local file system for GPX files'''
    def __init__ (self, dir, follow=False, recurse=False,
                  rid='^[Rr]oute.*', tid='^[Tt]rack.*', wid='^[Ww]aypoint.*'):
        '''Construct and interface that allows access to the local file system

        dir : directory to look within
        follow : follow links when recurse is True
        recurse : descend into directories within the given directory

        rid : a regular expression for identifying route files
        tid : a regular expression for identifying track files
        wid : a regular expression for identifying waypoint files
        '''

        hj.device.Interface.__init__ (self)
        self.__base_dir = dir
        self.__follow = follow
        self.__recurse = recurse
        self.__rfns = []
        self.__rregex = re.compile (rid)
        self.__tfns = []
        self.__tregex = re.compile (tid)
        self.__wfns = []
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
    
    def _load(self):
        '''walk the directories and find all of the items'''
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

    def routes(self):
        for rfn in self.__rfns: yield rfn
        return
    
    def tracks(self):
        for tfn in self.__tfns: yield tfn
        return
    
    def waypoints(self):
        for wfn in self.__wfns: yield wfn
        return
    pass

if __name__ == '__main__':
    di = Interface(dir='/home/niessner/Hiking/garmin', recurse=False)
    di._load()
    print ('Routes:')
    for rfn in di.routes(): print ('   ' + rfn)
    print ('Tracks:')
    for tfn in di.tracks(): print ('   ' + tfn)
    print ('Waypoints:')
    for wfn in di.waypoints(): print ('   ' + wfn)
    pass
