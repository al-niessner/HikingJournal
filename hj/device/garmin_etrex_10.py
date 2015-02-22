import hj.device
import os

class Interface(hj.device.Interface):
    def __init__ (self, mp, rloc='Garmin/GPX', suffix='.gpx'):
        '''Construct an interface that allows access to the Garmin ETrex-10

        mp : mount point
        rloc : relative location of the GPX files on the Garmin device
        suffix : the suffix used
        '''
        hj.device.Interface.__init__ (self)
        self.__mp = mp
        self.__rfns = []
        self.__rloc = rloc
        self.__suffix = suffix
        self.__tfns = []
        self.__wfns = []
        return
    
    def _clear(self):
        for fn in self.__rfns + self.__tfns + self.__wfns:
            if os.path.exists (fn): os.remove (fn)
            pass
        return

    def _load(self):
        bdir = os.path.abspath (os.path.join (self.__mp, self.__rloc))

        if not (os.path.exists (bdir) and os.path.isdir (bdir)):
            raise ValueError('The mount point (mp) and relative location (rloc) "' + bdir + '" do not exist. Is the device mounted? Are the paths correct?')

        for fn in filter (lambda fn:fn.endswith (self.__suffix),
                          os.listdir (bdir)):
            ffn = os.path.join (bdir, fn)
            f = open (ffn, 'rt')
            gpx = f.read (2000)
            f.close()

            if 0 < gpx.find ('<trkpt '): self.__tfns.append (ffn)
            if 0 < gpx.find ('<wpt '): self.__wfns.append (ffn)
            pass
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

            
