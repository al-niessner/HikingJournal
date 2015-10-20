
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
            pass
        return
    pass


if __name__ == '__main__':
    import hj.usgs.historical

    quad = hj.usgs.historical.Quad('/home/niessner/Hiking/Quads/Rockies/MT_Silver Run Peak_266706_1996_24000_geo.pdf')
    pass
