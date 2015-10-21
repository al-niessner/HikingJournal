
import gdal
import hj
import numpy
import os
import osgeo.ogr
import osgeo.osr

class Quad(hj.Map):
    def __init__(self, fn):
        '''Initialization of a USGS Quadrangle Topographical map
        
        Load the reference information from the USGS historical quad and move
        the actual map file to safety.
        '''

        if os.path.exists (fn) and os.path.isfile (fn):
            ds = gdal.Open (fn)
            grt = ds.GetGeoTransform()
            self._at = hj.Map.Affine(Ox=grt[0], Px=grt[1], Lx=grt[2],
                                     Oy=grt[3], Py=grt[4], Ly=grt[5])
            self._cols = ds.RasterXSize
            self._name = ' '.join (os.path.basename (fn).split ('_')[:-2])
            self._neatline = ds.GetMetadataItem ('NEATLINE')
            self._projection = ds.GetProjection()
            self._rows = ds.RasterYSize
            source = osgeo.osr.SpatialReference()
            source.ImportFromWkt (ds.GetProjection())
            target = osgeo.osr.SpatialReference()
            target.SetWellKnownGeogCS('WGS84')
            transform = osgeo.osr.CoordinateTransformation(source, target)
            self._orig, self._pix, self._wgs = [],[],[]
            for corner in self._neatline[10:-2].split (','):
                c,r = corner.split()
                self._orig.append (hj.Map.Point(lat=r, lon=c))
                # convert to wgs84
                p = osgeo.ogr.CreateGeometryFromWkt ('POINT (' + corner + ')')
                p.Transform (transform)
                lat = p.GetY()
                lon = p.GetX()
                self._wgs.append (hj.Map.Point(lat=lat, lon=lon))
                # convert to pixel
                c = int((numpy.double(c) - self._at.Ox) /
                        (self._at.Px + self._at.Lx))
                r = int((numpy.double(r) - self._at.Oy) /
                        (self._at.Py + self._at.Ly))
                # int uses truncation so need to move the points to the inside
                # of the neatline just for general safety of look, but really
                # nobody is going to notice a single pixle or they should not
                # if they really hike.
                c += 1 if c < self._cols else 0
                r += 1 if r < self._rows else 0
                self._pix.append (hj.Map.Pixel(col=c, row=r))
                pass
            Mx = self._at.Ox + self._at.Px*self._cols + self._at.Lx*self._rows
            My = self._at.Oy + self._at.Py*self._cols + self._at.Ly*self._rows
            p1 = osgeo.ogr.CreateGeometryFromWkt ('POINT (%d %d)' %
                                                  (self._at.Ox, self._at.Oy))
            p2 = osgeo.ogr.CreateGeometryFromWkt ('POINT (%d %d)' %
                                                  (Mx, self._at.Oy))
            p3 = osgeo.ogr.CreateGeometryFromWkt ('POINT (%d %d)' %
                                                  (self._at.Ox, My))
            p4 = osgeo.ogr.CreateGeometryFromWkt ('POINT (%d %d)' % (Mx, My))
            p1.Transform (transform)
            p2.Transform (transform)
            p3.Transform (transform)
            p4.Transform (transform)
            self._wat = hj.Map.Affine(Ox=p1.GetX(),
                                      Px=(p2.GetX() - p1.GetX()) / self._cols,
                                      Lx=(p4.GetX() - p2.GetX()) / self._rows,
                                      Oy=p1.GetY(),
                                      Py=(p4.GetY() - p3.GetY()) / self._cols,
                                      Ly=(p3.GetY() - p1.GetY()) / self._rows)
            self._fingerprint = hj.db.archive (hj.db.EntryType.raw, fn)
            pass
        return

    def get_image(self)->numpy.array:
        ds = gdal.Open (os.path.join (hj.config.wdir, self._fingerprint))
        rgb = ds.ReadAsArray()
        img = numpy.empty (rgb.shape[1:] + (3,), dtype=numpy.uint8)
        for i in range(3): img[:,:,i] = rgb[i]        
        return img

    def get_affine_transform(self)->Affine: return self._wat
    def get_fingerprint(self)->str: return self._fingerprint
    def get_name(self)->str: return self._name
    def get_pixel_bb(self)->[Pixel]: return self._pix.copy()
    def get_wgs84_bb(self)->[Point]: return self._wgs.copy()
    pass


if __name__ == '__main__':
    import hj.usgs.historical

    quad = hj.usgs.historical.Quad('/home/niessner/Hiking/Quads/Rockies/MT_Silver Run Peak_266706_1996_24000_geo.pdf')
    pass
