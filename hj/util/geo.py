'''Utilities that make it simpler to use gdal and work with GPS data
'''

import collections
import hj
import hj.db
import matplotlib.mlab
import matplotlib.pyplot
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

        self._blue = numpy.array([0,0,255])
        self._cyan = numpy.array([0,255,255])
        self._green = self._cyan - self._blue
        self._magenta = numpy.array([255,0,255])
        self._red = self._magenta - self._blue
        self._yellow = self._green + self._red
        
        self._fp = ':'.join (sorted ([k for k in md.keys()]))
        self._md = md
        self._name = ':'.join ([md[k].get_name() for k in sorted (md.keys())])
        self._tiles = self._tile()
        self._bb()
        self._make_fm()
        self._fill_fm()

        # build local footprint when drawing track
        x,y = numpy.meshgrid ([x for x in range (15)], [y for y in range (15)])
        R = numpy.sqrt ((x - 7)**2 + (y - 7)**2)
        matplotlib.pyplot.imshow (R < 7.25)
        idx = matplotlib.mlab.find (R < 7.25)
        fp = numpy.empty ((len (idx), 2),dtype=numpy.int8)
        fp[:,0] = idx/15
        fp[:,1] = idx - fp[:,0]*15        
        self._mask = fp - 7
        self._fps = (15,15)
        return

    def _oml(self): return [self._md[k] for k in sorted (self._md.keys())]

    def _bb(self)->None:
        self._bb = [self._parallelagram (m.get_wgs84_bb()) for m in self._oml()]
        for rc,i in filter (lambda e:-1 < e[1],
                            numpy.ndenumerate (self._tiles)):
            r,c = rc
            nw = 0 < c and 0 < r and -1 < self._tiles[r-1,c-1]
            nb = 0 < r and -1 < self._tiles[r-1,c]
            ne = c+1 < self._tiles.shape[1] and 0 < r and \
                 -1 < self._tiles[r-1,c+1]
            eb = c+1 < self._tiles.shape[1] and -1 < self._tiles[r,c+1]
            sb = r+1 < self._tiles.shape[0] and -1 < self._tiles[r+1,c]
            se = c+1 < self._tiles.shape[1] and r+1 < self._tiles.shape[0] and \
                 -1 < self._tiles[r+1,c+1]
            wb = 0 < c and -1 < self._tiles[r,c-1]
            sw = 0 < c and r+1 < self._tiles.shape[0] and \
                 -1 < self._tiles[r+1,c-1]
        
            if any ([nw,nb,wb]):
                cs = [corner (self._bb[self._tiles[r,c]],
                              hj.Map.Corner.NorthWest)]
                if nw: cs.append (corner (self._bb[self._tiles[r-1,c-1]]
                                          , hj.Map.Corner.SouthEast))
                if nb: cs.append (corner (self._bb[self._tiles[r-1,c]],
                                          hj.Map.Corner.SouthWest))
                if wb: cs.append (corner (self._bb[self._tiles[r,c-1]],
                                          hj.Map.Corner.NorthEast))
            
                nc = hj.Map.Point(lat=numpy.mean ([p.lat for p in cs]),
                                  lon=numpy.mean ([p.lon for p in cs]))
            
                self._replace (self._bb[self._tiles[r,c]], nc,
                               hj.Map.Corner.NorthWest)
                if nw: self._replace (self._bb[self._tiles[r-1,c-1]], nc,
                                      hj.Map.Corner.SouthEast)
                if nb: self._replace (self._bb[self._tiles[r-1,c]], nc,
                                      hj.Map.Corner.SouthWest)
                if wb: self._replace (self._bb[self._tiles[r,c-1]], nc,
                                      hj.Map.Corner.NorthEast)
                pass
        
            if any ([ne,nb,eb]):
                cs = [corner (self._bb[self._tiles[r,c]],
                              hj.Map.Corner.NorthEast)]
                if ne: cs.append (corner (self._bb[self._tiles[r-1,c+1]],
                                          hj.Map.Corner.SouthWest))
                if nb: cs.append (corner (self._bb[self._tiles[r-1,c]],
                                          hj.Map.Corner.SouthEast))
                if eb: cs.append (corner (self._bb[self._tiles[r,c+1]],
                                          hj.Map.Corner.NorthWest))
            
                nc = hj.Map.Point(lat=numpy.mean ([p.lat for p in cs]),
                                  lon=numpy.mean ([p.lon for p in cs]))
            
                self._replace (self._bb[self._tiles[r,c]], nc,
                               hj.Map.Corner.NorthEast)
                if ne: self._replace (self._bb[self._tiles[r-1,c+1]], nc,
                                      hj.Map.Corner.SouthWest)
                if nb: self._replace (self._bb[self._tiles[r-1,c]], nc,
                                      hj.Map.Corner.SouthEast)
                if eb: self._replace (self._bb[self._tiles[r,c+1]], nc,
                                      hj.Map.Corner.NorthWest)
                pass
        
            if any ([se,sb,eb]):
                cs = [corner (self._bb[self._tiles[r,c]],
                              hj.Map.Corner.SouthEast)]
                if se: cs.append (corner (self._bb[self._tiles[r+1,c+1]],
                                          hj.Map.Corner.NorthWest))
                if sb: cs.append (corner (self._bb[self._tiles[r+1,c]],
                                          hj.Map.Corner.NorthEast))
                if eb: cs.append (corner (self._bb[self._tiles[r,c+1]],
                                          hj.Map.Corner.SouthWest))
            
                nc = hj.Map.Point(lat=numpy.mean ([p.lat for p in cs]),
                                  lon=numpy.mean ([p.lon for p in cs]))
            
                self._replace (self._bb[self._tiles[r,c]], nc,
                               hj.Map.Corner.SouthEast)
                if se: self._replace (self._bb[self._tiles[r+1,c+1]], nc,
                                      hj.Map.Corner.NorthWest)
                if sb: self._replace (self._bb[self._tiles[r+1,c]], nc,
                                      hj.Map.Corner.NorthEast)
                if eb: self._replace (self._bb[self._tiles[r,c+1]], nc,
                                      hj.Map.Corner.SouthWest)
                pass
        
            if any ([sw,sb,wb]):
                cs = [corner (self._bb[self._tiles[r,c]],
                              hj.Map.Corner.SouthWest)]
                if sw: cs.append (corner (self._bb[self._tiles[r+1,c-1]],
                                          hj.Map.Corner.NorthEast))
                if sb: cs.append (corner (self._bb[self._tiles[r+1,c]],
                                          hj.Map.Corner.NorthWest))
                if wb: cs.append (corner (self._bb[self._tiles[r,c-1]],
                                          hj.Map.Corner.SouthEast))
            
                nc = hj.Map.Point(lat=numpy.mean ([p.lat for p in cs]),
                                  lon=numpy.mean ([p.lon for p in cs]))
            
                self._replace (self._bb[self._tiles[r,c]], nc,
                               hj.Map.Corner.SouthWest)
                if sw: self._replace (self._bb[self._tiles[r+1,c-1]], nc,
                                      hj.Map.Corner.NorthEast)
                if sb: self._replace (self._bb[self._tiles[r+1,c]], nc,
                                      hj.Map.Corner.NorthWest)
                if wb: self._replace (self._bb[self._tiles[r,c-1]], nc,
                                      hj.Map.Corner.SouthEast)
                pass
            pass
        return

    def _fill_fm (self)->None:
        fmm = numpy.empty (self._fm.shape[:-1], dtype=numpy.bool)
        fmi = numpy.empty (fmm.shape + (2,), dtype=numpy.int32)
        fmi[:,:,0],fmi[:,:,1] = numpy.meshgrid ([c for c in range (fmm.shape[1])], [r for r in range(fmm.shape[0])])
        for cb,m in zip(self._cb, self._oml()):
            imm = numpy.empty (m.raw_shape(), dtype=numpy.bool).transpose()
            imi = numpy.empty (imm.shape + (2,), dtype=numpy.int32)
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
        clipbox = [Clipbox(hj.Map.Pixel(None,None),o,o,o,o)
                   for m in self._oml()]
        for rc,i in filter (lambda e:-1 < e[1],
                            numpy.ndenumerate (self._tiles)):
            r,c = rc
            bb,cb,m = self._bb[i],clipbox[i],self._oml()[i]
            nb = 0 < r and -1 < self._tiles[r-1,c]
            eb = c+1 < self._tiles.shape[1] and -1 < self._tiles [r,c+1]
            sb = r+1 < self._tiles.shape[0] and -1 < self._tiles [r+1,c]
            wb = 0 < c and -1 < self._tiles[r,c-1]
            nwc = m.inverse (corner (bb, hj.Map.Corner.NorthWest))
            nec = m.inverse (corner (bb, hj.Map.Corner.NorthEast))
            swc = m.inverse (corner (bb, hj.Map.Corner.SouthWest))
            sec = m.inverse (corner (bb, hj.Map.Corner.SouthEast))
            cb = cb._replace (nw=hj.Map.Pixel (col=0 if not wb else nwc.col,
                                               row=0 if not nb else nwc.row),
                              ne=hj.Map.Pixel (col=m.raw_shape().col-1 if not eb else nec.col,
                                               row=0 if not nb else nec.row),
                              sw=hj.Map.Pixel (col=0 if not wb else swc.col,
                                               row=m.raw_shape().row-1 if not sb else swc.row),
                              se=hj.Map.Pixel (col=m.raw_shape().col-1 if not eb else sec.col,
                                               row=m.raw_shape().row-1 if not sb else sec.row))

            if r == 0 or c == 0: cb = cb._replace (offset=hj.Map.Pixel(col=0 if c == 0 else None, row=0 if r == 0 else None))
            
            if nb and not wb:
                swc = self._oml()[self._tiles[r-1,c]].inverse (corner (self._bb[self._tiles[r-1,c]], hj.Map.Corner.SouthWest))
                ocb = clipbox[self._tiles[r-1,c]]
                cb = cb._replace (offset=hj.Map.Pixel(col=swc.col - nwc.col,row=ocb.offset.row + (ocb.sw.row - ocb.nw.row)))
                pass
        
            if wb and not nb:
                nec = self._oml()[self._tiles[r,c-1]].inverse (corner (self._bb[self._tiles[r,c-1]], hj.Map.Corner.NorthEast))
                ocb = clipbox[self._tiles[r,c-1]]
                cb = cb._replace (offset=hj.Map.Pixel(col=ocb.offset.col + (ocb.ne.col - ocb.nw.col),row=nec.row - nwc.row))
                pass

            if wb and nb:
                ncb = clipbox[self._tiles[r-1,c]]
                wcb = clipbox[self._tiles[r,c-1]]
                cb = cb._replace (offset=hj.Map.Pixel(col=wcb.offset.col + (wcb.ne.col - wcb.nw.col),row=ncb.offset.row + (ncb.sw.row - ncb.nw.row)))
            
                if ncb.offset.col is None:
                    nwc = self._oml()[self._tiles[r-1,c]].inverse (corner (self._bb[self._tiles[r-1,c]], hj.Map.Corner.NorthWest))
                    swc = self._oml()[self._tiles[r-1,c]].inverse (corner (self._bb[self._tiles[r-1,c]], hj.Map.Corner.SouthWest))
                    clipbox[self._tiles[r-1,c]] = ncb._replace (offset=hj.Map.Pixel(col=cb.offset.col - (swc.col - nwc.col) - (nwc.col - ncb.nw.col), row=ncb.offset.row))
                    pass

                if wcb.offset.row is None:
                    nec = self._oml()[self._tiles[r,c-1]].inverse (corner (self._bb[self._tiles[r,c-1]], hj.Map.Corner.NorthEast))
                    nwc = self._oml()[self._tiles[r,c-1]].inverse (corner (self._bb[self._tiles[r,c-1]], hj.Map.Corner.NorthWest))
                    clipbox[self._tiles[r,c-1]] = wcb._replace (offset=hj.Map.Pixel(col=wcb.offset.col, row=cb.offset.row - (nec.row - nwc.row) - (nwc.row - wcb.nw.row)))
                    pass
                pass
        
            clipbox[i] = cb
            pass
        cols,rows = [],[]
        for cb in clipbox:
            cols.append (cb.offset.col)
            rows.append (cb.offset.row)
            pass
        mc,mr = min (cols),min (rows)
        for i,cb in enumerate (clipbox): clipbox[i] = cb._replace(offset=hj.Map.Pixel(col=cb.offset.col - mc, row=cb.offset.row - mr))
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
    
    def _parallelagram (self, pts:[hj.Map.Point])->[hj.Map.Point]:
        return [corner (pts, hj.Map.Corner.NorthWest),
                corner (pts, hj.Map.Corner.NorthEast),
                corner (pts, hj.Map.Corner.SouthEast),
                corner (pts, hj.Map.Corner.SouthWest),
                corner (pts, hj.Map.Corner.NorthWest)]

    def _replace (self, bb:[hj.Map.Point],
                  nc:hj.Map.Point,
                  which:hj.Map.Corner)->None:
        bb[which.value + 1] = nc
        if which == hj.Map.Corner.NorthWest: bb[0] = nc
        return
    
    def _segment (lp, p, fms, fp, fps):
        alp = numpy.array([lp.row, lp.col])
        ap = numpy.array([p.row, p.col])
        clp = fp + alp
        clp[clp < 0] = 0
        cp = fp + ap
        cp[cp < 0] = 0
        ue,be = fps[0]//2, fps[0] - fps[0]//2
        le,re = fps[1]//2, fps[1] - fps[1]//2
        pts = [tuple(clp[i]) for i in range (clp.shape[0])]
        pts.extend ([tuple(cp[i]) for i in range (cp.shape[0])])
            
        if p.col == lp.col:
            for r in range (min (p.row, lp.row),max (p.row, lp.row)+1):
                for c in range (max (0, p.col-le), min (p.col+re, fms[1])): pts.append ((r, c))
                pass
        elif p.row == lp.row:
            for c in range (min (p.col, lp.col),max (p.col, lp.col)+1):
                for r in range (max (0, p.row-ue), min (p.row+be, fms[0])): pts.append ((r, c))
                pass
        else:
            c,r = numpy.meshgrid ([c for c in range (max (0, min (p.col, lp.col) - le), min (max (p.col, lp.col)+re, fms[1]))],
                                  [r for r in range (max (0, min (p.row, lp.row) - ue), min (max (p.row, lp.row)+be, fms[0]))])
            dc = p.col - lp.col
            dr = p.row - lp.row
            dcr = p.col * lp.row - p.row * lp.col
            d = abs (dr*c - dc*r + dcr) / numpy.sqrt (dc*dc + dr*dr)
            pts.extend ([(pr,pc) for pr,pc in zip(r[d<ue],c[d<le])])
            pass
        return pts

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
        pdata = [(p.lon, p.lat) for p in data]
        gdata = [None for p in data]
        for bb,cb,mm in zip (self._bb, self._cb, self._oml()):
            pbb = matplotlib.path.Path([(p.lon, p.lat) for p in bb])
            for i,yes in enumerate (pbb.contains_points (pdata)):
                if yes:
                    lp = mm.inverse (data[i])
                    gdata[i] = hj.Map.Pixel(col=lp.col+cb.offset.col-cb.nw.col,
                                            row=lp.row+cb.offset.row-cb.nw.row)
                    pass
                pass
            pass

        if any ([p is None for p in gdata]):
            print (len (self._bb))
            raise ValueError('GPSElement is over the edge of the map? \n\t' +
                             'Waypoint: ' + str (icon) +
                             ('\n\ttotal: %d\n\toutside %d' %
                              (len (data), sum ([p is None for p in gdata]))))
        
        if icon:
            for p in gdata:
                self._fm[max ([0, p.row-17]):min ([p.row+18,
                                                   self._fm.shape[0]]),
                         max ([0, p.col-17]):min ([p.col+18,
                                                   self._fm.shape[1]]),:] = \
                                                   self._blue
                pass
        else:
            lp = gdata[0]
            pts = []
            seg = []
            for p in gdata:
                if self._fps[0]//2 < numpy.sqrt ((p.col - lp.col)**2 +
                                                 (p.row - lp.row)**2):
                    seg.append ((lp, p, self._fm.shape, self._mask, self._fps))
                    lp = p
                    pass
                pass
            seg = [Joined._segment (*s) for s in seg]
            for s in seg: pts.extend ([self._fm.shape[1]*int(p[0]) + int(p[1])
                                       for p in s])
            for pt in set(pts):
                rc = (pt//self._fm.shape[1],
                      pt - (pt//self._fm.shape[1])*self._fm.shape[1])
                self._fm[rc] = self._fm[rc] + \
                               numpy.uint8(0.6 * (self._magenta - self._fm[rc]))
                pass
            pass
        return gdata
    
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
    for p in t.get_points(): gt.AddPoint(p.lon, p.lat)
    return gt

def as_ogr_point (w:hj.GPSElement):
    g = osgeo.ogr.Geometry(osgeo.ogr.wkbPoint)
    g.AddPoint (w.get_points()[0].lon,
                w.get_points()[0].lat)
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
