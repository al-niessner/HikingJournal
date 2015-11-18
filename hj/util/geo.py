'''Utilities that make it simpler to use gdal and work with GPS data
'''

import collections
import hj
import hj.db
import matplotlib.mlab
import numpy
import os
import osgeo.ogr
import shapely
import shapely.geometry
import tempfile

ELV = 2
LAT = 0
LON = 1
TIM = 3

Clipbox = collections.namedtuple ('Clipbox', ['offset', 'nw', 'ne', 'se', 'sw'])

class Joined(hj.Map):
    def __init__ (self, ml:[hj.Map]=None, fp:str=None):
        if (ml is None and fp is None) or (ml is not None and fp is not None):
            raise ValueError('Initialization is either by a list of maps or a fingerprint')
        if fp: md = hj.db.fetch (fp.split (':'))
        else: md = dict([(m.get_fingerprint(), m) for m in ml])

        self._fp = ':'.join (sorted ([k for k in md.keys()]))
        self._md = md
        self._name = ':'.join ([md[k].get_name() for k in sorted (md.keys())])
        self._tiles = self._tile()
        self._bb()
        self._make_fm()
        self._fill_fm()
        return

    def _oml(self): return [self._md[k] for k in sorted (self._md.keys())]

    def _bb(self)->None:
        self._bb = [m.get_wgs84_bb() for m in self._oml()]
        for r in range (1,self._tiles.shape[0]):
            b0,b1 = [],[]
            for c in range (self._tiles.shape[1]):
                if -1 < self._tiles[r,c]:
                    b0.extend ([corner (self._bb[self._tiles[r,c]],
                                        hj.Map.Corner.NorthWest),
                                corner (self._bb[self._tiles[r,c]],
                                        hj.Map.Corner.NorthEast)])
                else: b0.extend ([hj.Map.Point(numpy.nan, numpy.nan)])
                if -1 < self._tiles[r-1,c]:
                    b1.extend ([corner (self._bb[self._tiles[r-1,c]],
                                        hj.Map.Corner.SouthWest),
                                corner (self._bb[self._tiles[r-1,c]],
                                        hj.Map.Corner.SouthEast)])
                else: b1.extend ([hj.Map.Point(numpy.nan, numpy.nan)])
                pass
            b0 = [p for p in filter (lambda x:not numpy.isnan(x).any(), b0)]
            b1 = [p for p in filter (lambda x:not numpy.isnan(x).any(), b1)]
            lat = (min([p.lat for p in b0]) + max([p.lat for p in b1])) / 2.0
            lon = [p.lon for p in b0] + [p.lon for p in b1]
            edge = shapely.geometry.LineString([(min (lon)-.1,lat),
                                                (max (lon)+.1,lat)])
            for c in range (self._tiles.shape[1]):
                if -1 < self._tiles[r-1,c]:
                    self._replace (self._bb[self._tiles[r-1,c]], edge)
                if -1 < self._tiles[r,c]:
                    self._replace (self._bb[self._tiles[r,c]], edge)
            pass
        for c in range (1, self._tiles.shape[1]):
            b0,b1 = [],[]
            for r in range (self._tiles.shape[0]):
                if -1 < self._tiles[r,c]:
                    b0.extend ([corner (self._bb[self._tiles[r,c]],
                                        hj.Map.Corner.NorthEast),
                                corner (self._bb[self._tiles[r,c]],
                                        hj.Map.Corner.SouthEast)])
                else: b0.extend ([hj.Map.Point(numpy.nan, numpy.nan)])
                if -1 < self._tiles[r,c-1]:
                    b1.extend ([corner (self._bb[self._tiles[r,c-1]],
                                        hj.Map.Corner.NorthWest),
                                corner (self._bb[self._tiles[r,c-1]],
                                        hj.Map.Corner.SouthWest)])
                else: b1.extend ([hj.Map.Point(numpy.nan, numpy.nan)])
                pass
            b0 = [p for p in filter (lambda x:not numpy.isnan(x).any(), b0)]
            b1 = [p for p in filter (lambda x:not numpy.isnan(x).any(), b1)]
            lat = [p.lat for p in b0] + [p.lat for p in b1]
            lon = (min([p.lon for p in b0]) + max([p.lon for p in b1])) / 2.0
            edge = shapely.geometry.LineString([(lon, min (lat)-.1),
                                                (lon, max (lat)+.1)])
            for r in range (self._tiles.shape[0]):
                if -1 < self._tiles[r,c-1]:
                    self._replace (self._bb[self._tiles[r,c-1]], edge)
                if -1 < self._tiles[r,c]:
                    self._replace (self._bb[self._tiles[r,c]], edge)
            pass
        return

    def _fill_fm (self)->None:
        fmm = numpy.empty (self._fm.shape[:-1], dtype=numpy.bool)
        fmi = numpy.empty (fmm.shape + (2,), dtype=numpy.int)
        fmi[:,:,0],fmi[:,:,1] = numpy.meshgrid ([c for c in range (fmm.shape[1])], [r for r in range(fmm.shape[0])])
        for cb,m in zip(self._cb, self._oml()):
            imm = numpy.empty (m.raw_shape(), dtype=numpy.bool).transpose()
            imi = numpy.empty (imm.shape + (2,))
            imi[:,:,0],imi[:,:,1] = numpy.meshgrid ([c for c in range (imm.shape[1])], [r for r in range(imm.shape[0])])
            pimg = matplotlib.path.Path([(p.col, p.row) for p in [cb.nw, cb.ne, cb.se, cb.sw, cb.nw]])
            pfm = matplotlib.path.Path([(cb.offset.col + p.col - cb.nw.col, cb.offset.row + p.row - cb.nw.row) for p in [cb.nw, cb.ne, cb.se, cb.sw, cb.nw]])
            imm[:,:] = pimg.contains_points((imi.reshape (imm.shape[0]*imm.shape[1],2))).reshape (imm.shape)
            fmm[:,:] = pfm.contains_points ((fmi.reshape (fmm.shape[0]*fmm.shape[1],2))).reshape (fmm.shape)
            self._fm[fmm] = m.get_image()[imm]
            pass
        return
    
    def _make_fm (self)->None:
        o = hj.Map.Pixel (0,0)
        clipbox = [Clipbox(hj.Map.Pixel(-1,-1),o,o,o,o) for m in self._oml()]
        height,width = numpy.zeros (self._tiles.shape),numpy.zeros (self._tiles.shape)
        for rc,i in filter (lambda e:-1 < e[1], numpy.ndenumerate (self._tiles)):
            r,c = rc
            co,ro = 0 if c == 0 else -1,0 if r == 0 else -1
            bb,cb,m = self._bb[i],clipbox[i],self._oml()[i]
            nb = 0 < r and -1 < self._tiles[r-1,c]
            eb = c+1 < self._tiles.shape[1] and -1 < self._tiles [r,c+1]
            sb = r+1 < self._tiles.shape[0] and -1 < self._tiles [r+1,c]
            wb = 0 < c and -1 < self._tiles[r,c-1]

            if nb or wb: nwc = m.inverse (corner (bb, hj.Map.Corner.NorthWest))
            if nb or eb: nec = m.inverse (corner (bb, hj.Map.Corner.NorthEast))
            if sb or wb: swc = m.inverse (corner (bb, hj.Map.Corner.SouthWest))
            if sb or eb: sec = m.inverse (corner (bb, hj.Map.Corner.SouthEast))

            cb = cb._replace (nw=hj.Map.Pixel (col=0 if not wb else nwc.col,
                                               row=0 if not nb else nwc.row),
                              ne=hj.Map.Pixel (col=m.raw_shape().col-1 if not eb else nec.col,
                                               row=0 if not nb else nec.row),
                              sw=hj.Map.Pixel (col=0 if not wb else swc.col,
                                               row=m.raw_shape().row-1 if not sb else swc.row),
                              se=hj.Map.Pixel (col=m.raw_shape().col-1 if not eb else sec.col,
                                               row=m.raw_shape().row-1 if not sb else sec.row))
            
            if wb:
                if -1 < clipbox[self._tiles[r,c-1]].offset.col: co = clipbox[self._tiles[r,c-1]].ne.col - (nwc.col - cb.nw.col)
                if -1 < clipbox[self._tiles[r,c-1]].offset.row: ro = clipbox[self._tiles[r,c-1]].ne.row - (nwc.row - cb.nw.row)
                pass
            if nb:
                if -1 < clipbox[self._tiles[r-1,c]].offset.col: co = clipbox[self._tiles[r-1,c]].sw.col - (nwc.col - cb.nw.col)
                if -1 < clipbox[self._tiles[r-1,c]].offset.row: ro = clipbox[self._tiles[r-1,c]].sw.row - (nwc.row - cb.nw.row)
                pass
    
            clipbox[i] = cb._replace (offset=hj.Map.Pixel(col=co, row=ro))
            pass
        while any([cb.offset.col == -1 or cb.offset.row == -1
                   for cb in clipbox]):
            for rc,i in filter (lambda e:-1 < e[1], numpy.ndenumerate (self._tiles)):
                r,c = rc
                co,ro = 0 if c == 0 else -1,0 if r == 0 else -1
                bb,cb,m = self._bb[i],clipbox[i],self._oml()[i]
                nb = 0 < r and -1 < self._tiles[r-1,c]
                eb = c+1 < self._tiles.shape[1] and -1 < self._tiles [r,c+1]
                sb = r+1 < self._tiles.shape[0] and -1 < self._tiles [r+1,c]
                wb = 0 < c and -1 < self._tiles[r,c-1]

                if -1 < cb.offset.col and -1 < cb.offset.row: continue

                if nb or wb: nwc = m.inverse(corner(bb,hj.Map.Corner.NorthWest))
                if nb or eb: nec = m.inverse(corner(bb,hj.Map.Corner.NorthEast))
                if sb or wb: swc = m.inverse(corner(bb,hj.Map.Corner.SouthWest))
                if sb or eb: sec = m.inverse(corner(bb,hj.Map.Corner.SouthEast))
                
                if eb:
                    if -1 < clipbox[self._tiles[r,c+1]].offset.col: co = clipbox[self._tiles[r,c+1]].offset.col - (nec.col - cb.nw.col)
                    if -1 < clipbox[self._tiles[r,c+1]].offset.row: ro = clipbox[self._tiles[r,c+1]].offset.row - (nec.row - cb.nw.row)
                    pass
                if sb:
                    if -1 < clipbox[self._tiles[r+1,c]].offset.col: co = clipbox[self._tiles[r+1,c]].offset.col - (swc.col - cb.nw.col)
                    if -1 < clipbox[self._tiles[r+1,c]].offset.row: ro = clipbox[self._tiles[r+1,c]].offset.row - (swc.row - cb.nw.row)
                    pass
                
                clipbox[i] = cb._replace (offset=hj.Map.Pixel(col=co, row=ro))
                pass
            pass
        cols,rows = [],[]
        for c in range (self._tiles.shape[1]):
            cb = clipbox[self._tiles[-1,c]]
            rows.append (cb.offset.row + cb.sw.row - cb.nw.row)
            pass
        for r in range (self._tiles.shape[0]):
            cb = clipbox[self._tiles[r,-1]]
            cols.append (cb.offset.col + cb.ne.col - cb.nw.col)
            pass
        self._cb = clipbox
        self._fm = numpy.zeros ((max(rows)+1, max(cols)+1, 3),dtype=numpy.uint8)
        return
    
    def _replace (self, bb:[hj.Map.Point],
                  edge:shapely.geometry.linestring.LineString)->None:
        d = numpy.empty ((len (bb),))
        nlr = shapely.geometry.LinearRing([(p.lon,p.lat) for p in bb])
        for ip in nlr.intersection (edge):
            d = [numpy.sqrt (numpy.square (ip.y - b.lat) +
                             numpy.square (ip.x - b.lon)) for b in bb]
            for idx in matplotlib.mlab.find (numpy.array(d) < 0.001):
                bb[idx] = hj.Map.Point(lat=ip.y, lon=ip.x)
                pass
            pass
        return
    
    def _tile(self)->None:
        ml = [v for v in self._md.values()]
        tile = numpy.empty ((1,1,2))
        m = ml.pop(0)
        tile[0,0,:] = m._affine_transform().Ox, m._affine_transform().Oy
        while 0 < len (ml):
            m = ml.pop (0)
            x,y = m._affine_transform().Ox, m._affine_transform().Oy
            for r in range (tile.shape[0]):
                for c in range (tile.shape[1]):
                    dx,dy = x - tile[r,c,0], y - tile[r,c,1]
                    nr,nc = r,c
            
                    if .1 < abs (dx) and abs (dx) < .2 and abs (dy) < .1:
                        # left or right of r,c
                        nc = c + (-1 if 0 < dx else 1) * (-1 if x < 0 else 1)
                        pass
                    if .1 < abs (dy) and abs (dy) < .2 and abs (dx) < .1:
                        # top or bottom of r,c
                        nr = r + (-1 if 0 < dy else 1) * (-1 if y < 0 else 1)
                        pass
                    if .1 < abs (dx) and abs (dx) < .2 and \
                           .1 < abs (dy) and abs (dy) < .2:
                        # diagonal
                        nc = c + (-1 if 0 < dx else 1) * (-1 if x < 0 else 1)
                        nr = r + (-1 if 0 < dy else 1) * (-1 if y < 0 else 1)
                        pass
                    if nc != c or nr != r:
                        if nc < 0 or nc == tile.shape[1]:
                            nt = numpy.empty ((tile.shape[0], tile.shape[1]+1, 2))
                            nt[:,:,:] = numpy.nan
                    
                            if nc < 0:
                                nt[:,1:,:] = tile
                                nc += 1
                            else: nt[:,:-1,:] = tile
                            
                            tile = nt
                            pass
                
                        if nr < 0 or nr == tile.shape[0]:
                            nt = numpy.empty ((tile.shape[0]+1, tile.shape[1], 2))
                            nt[:,:,:] = numpy.nan
                    
                            if nr < 0:
                                nt[1:,:,:] = tile
                                nr += 1
                            else: nt[:-1,:,:] = tile
                    
                            tile = nt
                            pass
                
                        tile[nr,nc,:] = x,y 
                        m = None
                        break
                    pass
                if m is None: break
                pass
            pass
        tiles = numpy.empty (tile.shape[:-1], dtype=int)
        tiles[:,:] = -1
        ml = self._oml()
        for r in range (tiles.shape[0]):
            for c in range (tiles.shape[1]):
                if not numpy.isnan (tile[r,c,0]):
                    for i,m in enumerate (ml):
                        dx = abs (tile[r,c,0] - m._affine_transform().Ox)
                        dy = abs (tile[r,c,1] - m._affine_transform().Oy)
                        if dx < .001 and dy < .001: tiles[r,c] = i
                        pass
                    pass
                pass
            pass
        return tiles
    
    def all (self, pts:[hj.Map.Point])->bool:
        return len (self.which (pts)) == len (pts)

    def any (self, pts:[hj.Map.Point])->bool:
        return any ([m.any (pts) for m in self._md])
    
    def get_fingerprint(self)->str: return self._fp
    def get_image(self)->numpy.array: return self._fm
    def get_name(self)->str: return self._name

    
    def overlay (self, data:[hj.Map.Point], icon:bool=False)->[hj.Map.Pixel]:
        '''Overlay data onto the map (temporary)

        The overlay is temporary and is not recorded in the database!
        All overlays are accumulated and can be viewed by calling get_image().
        
        data : the GPS data to lay onto the map
        icon : when True, an icon is placed at each of the points
               when False, a line is drawn from point to point in order
               
        Returns a list of the pixel locations of those centers or an empty list
                when icon is None.
        '''
        raise NotImplementedError()
    
    def which (self, pts:[hj.Map.Point])->[int]:
        idx = set()
        for m in self._md.values(): idx.update (set (m.which (pts)))
        return sorted (idx)
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

def corner (pts:[hj.Map.Point], which:hj.Map.Corner)->hj.Map.Point:
    result = None
    lat = [p.lat for p in pts]
    lon = [p.lon for p in pts]
    n,s = max(lat), min(lat)
    e,w = max(lon), min(lon)
    c = hj.Map.Point(lat=n, lon=e) if which is hj.Map.Corner.NorthEast else None
    c = hj.Map.Point(lat=n, lon=w) if which is hj.Map.Corner.NorthWest else c
    c = hj.Map.Point(lat=s, lon=e) if which is hj.Map.Corner.SouthEast else c
    c = hj.Map.Point(lat=s, lon=w) if which is hj.Map.Corner.SouthWest else c
    d = [numpy.sqrt (numpy.square (p.lat - c.lat) + numpy.square (p.lon - c.lon))
         for p in pts]
    return pts[d.index (min (d))]

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
