
import gpxpy
import hj
import hj.db
import io
import logging ; log = logging.getLogger(__name__)
import numpy
import os
import osgeo.ogr

class Element(hj.GPSElement):
    def __init__ (self, bfn:str, points:[hj.GPSElement.Point],
                  typ:hj.db.EntryType, label:str=''):
        '''Initialize a GPX Element type

        bfn  - the base file name assigned by the device
        data - the gpxpy parsed data to be archived
        '''
        hj.GPSElement.__init__(self)
        self._desc = ''
        self._fp = hj.db._id ((typ.name + str(points)).encode())
        self._label = label
        self._name = bfn
        self._points = points
        self._type = typ
        return

    def __getstate__ (self):
        state = super().__getstate__()
        state = self.__dict__.copy()
        state['_points'] = [p._asdict() for p in state['_points']]
        return state

    def __setstate__ (self, state):
        state['_points'] = [hj.GPSElement.Point(**p) for p in state['_points']]
        return super().__setstate__ (state)

    def _arc2km (self, arc:float)->float:
        Re = 6378.1370 # Km
        Rp = 6356.7523 # Km
        lat = numpy.mean([p.lat for p in self._points]) / 180. * numpy.pi
        R = numpy.sqrt (((Re**2 * numpy.cos(lat))**2 + (Rp**2 * numpy.sin(lat))**2)/
                        ((Re * numpy.cos(lat))**2 + (Rp * numpy.sin (lat))**2))
        R += numpy.mean ([p.elev for p in self._points]) / 1000. # Km
        return arc * R * numpy.pi / 180.
    
    def get_desc (self)->str: return self._desc
    def get_distance (self)->(float,float):
        if 1 < len (self._points):
            ep = osgeo.ogr.Geometry(osgeo.ogr.wkbLineString)
            ep.AddPoint(self._points[0].lon, self._points[0].lat)
            ep.AddPoint(self._points[-1].lon, self._points[-1].lat)
            gt = osgeo.ogr.Geometry(osgeo.ogr.wkbLineString)
            for p in self._points: gt.AddPoint(p.lon, p.lat)
            result = self._arc2km (gt.Length()), self._arc2km(ep.Length())
        else: result = 0.0,0.0
        return result
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
        result.extend (trim (Element(bfn, pts, hj.db.EntryType.track, t.name)))
    for w in gpx.waypoints:
        p = hj.GPSElement.Point(elev=w.elevation,
                                lat=w.latitude,
                                lon=w.longitude,
                                time=w.time)
        result.append (Element(bfn, [p], hj.db.EntryType.waypt, w.name))
        pass
    return result

def trim (t:hj.GPSElement)->[hj.GPSElement]:
    dl, dt, pts, result = [],[], t.get_points(),[t]
    for i,p in enumerate(pts[:-1]):
        g0 = osgeo.ogr.Geometry(osgeo.ogr.wkbPoint)
        g0.AddPoint (p.lon, p.lat)
        g1 = osgeo.ogr.Geometry(osgeo.ogr.wkbPoint)
        g1.AddPoint (pts[i+1].lon, pts[i+1].lat)
        dl.append (abs (g0.Distance (g1)) * 6.370e6 * 3.145927 / 180.)
        dt.append ((pts[i+1].time - p.time).total_seconds())
        pass
    
    if 8*3600 < max (dt) or 50e3 < max (dl):
        log.warning ('Trimming: ' + t.get_label())
        idx = min ([dt.index (max (dt)), dl.index (max (dl))]) + 1

        if 20 < idx: 
            result = trim (Element(t._name, pts[:idx], t._type, t._label)) + \
                     trim (Element(t._name, pts[idx:], t._type, t._label))
        else: result = trim (Element(t._name, pts[idx:], t._type, t._label))
        log.info ('Number of segments: ' + str (len (result)))
        log.info ('Length of segments: ' + str ([len (t.get_points())
                                                 for t in result]))
        pass
    
    return result
