'''Utilities that make it simpler to use gdal and work with GPS data
'''

import hj
import hj.db
import matplotlib.mlab
import numpy
import os
import osgeo.ogr
import tempfile

ELV = 2
LAT = 0
LON = 1
TIM = 3

class Joined(hj.Map):
    def __init__ (self, ml:[hj.Map]=None, fp;str=None):
        if (ml is None and fp is None) or (ml is not None and fp is not None):
            raise ValueError('Initialization is either by a list of maps or a fingerprint')
        if fp: ml = hj.db.fetch (fp.split (','))
        return
    pass

def as_numpy_array (pts:[hj.GPSElement.Point], naxis=2)->numpy.array:
    result = numpy.empty ((len (pts), naxis))
    for i,p in enumerate (pts):
        if 0 < naxis: result[i,LAT] = p.lat
        if 1 < naxis: result[i,LON] = p.lon
        if 2 < naxis: result[i,ELV] = p.elev
        if 3 < naxis: result[i,TIM] = p.time
        pass
    return result

def as_ogr_line (t:hj.GPSElement):
    gt = osgeo.ogr.Geometry(osgeo.ogr.wkbLineString)
    for p in t.get_points(): gt.AddPoint(p.lon, p.lat, p.elev)
    return gt

def as_ogr_point (w:hj.GPSElement):
    g = osgeo.ogr.Geometry(osgeo.ogr.wkbPoint)
    g.AddPoint (w.get_points()[0].lon,
                w.get_points()[0].lat,
                w.get_points()[0].elev)
    return g

def indices (t:hj.GPSElement, ws:[hj.GPSElement]):
    gt = as_ogr_line (t)
    d = []
    for w in ws:
        p = as_ogr_point (w)
        d.append (abs (gt.Distance (p)) * 6.370e6 * 3.145927 / 180.)
        pass
    return matplotlib.mlab.find (numpy.array (d) < 100.)

def make_map (t:hj.GPSElement, maps:[hj.Map])->str:
    relevant = [m for m in filter (m.contains (t), maps)]
    fid,fn = tempfile.mkstemp (suffix='.png', prefix='map_')
    os.close (fid)
    return fn
