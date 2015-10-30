
import gpxpy
import hj
import hj.db
import io
import os

class Element(hj.GPSElement):
    def __init__ (self, bfn:str, points:[hj.GPSElement.Point], typ:hj.db.EntryType):
        '''Initialize a GPX Element type

        bfn  - the base file name assigned by the device
        data - the gpxpy parsed data to be archived
        '''
        self._desc = ''
        self._fp = hj.db._id ((typ.name + str(points)).encode())
        self._label = ''
        self._name = bfn
        self._points = points
        self._type = typ
        return

    def __getstate__ (self):
        state = self.__dict__.copy()
        state['_points'] = [p._asdict() for p in state['_points']]
        return state

    def __setstate__ (self, state):
        state['_points'] = [hj.GPSElement.Point(**p) for p in state['_points']]
        return self.__dict__.update (state)
    
    def get_desc (self)->str: return self._desc
    def get_fingerprint (self)->str: return self._fp
    def get_label (self)->str: return self._label
    def get_name (self)->str: return self._name
    def get_points (self)->[hj.GPSElement.Point]: return self._points.copy()
    def get_type (self)->hj.db.EntryType: return self._type
    def set_desc (self, description:str)->None: self._desc = description
    def set_label (self, label:str)->None: self._label = label
    pass

def parse (data:io.TextIOBase, fn:str)->[Element]:
    bfn = os.path.basename (fn)
    gpx = gpxpy.parse (data)
    result = []
    for r in gpx.routes: raise NotImplementedError()
    for t in gpx.tracks:
        pts = []
        for s in t.segments:
            for p in s.points: pts.append (hj.GPSElement.Point(elev=p.elevation,
                                                               lat=p.latitude,
                                                               lon=p.longitude,
                                                               time=p.time))
            pass
        result.append (Element(bfn, pts, hj.db.EntryType.track))
        result[-1].set_label (t.name)
    for w in gpx.waypoints:
        p = hj.GPSElement.Point(elev=w.elevation,
                                lat=w.latitude,
                                lon=w.longitude,
                                time=w.time)
        result.append (Element(bfn, [p], hj.db.EntryType.waypt))
        result[-1].set_label (w.name)
        pass
    return result
