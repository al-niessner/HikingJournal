
import collections
import enum
import numpy

class Annotated(object):
    def __init__(self, tid:str, mid:str=None, pids:[str]=[], wids:[str]=[]):
        object.__init__(self)
        import hj.db

        self.__fp = hj.db._id (('Annotated Track: ' + tid[0]).encode()) 
        self.__map = mid
        self.__photos = pids
        self.__track = tid[0]
        self.__waypts = wids
        return

    def get_fingerprint (self)->str:
        '''An identifier that is immutable but unique'''
        return self.__fp

    def get_track_fingerprint (self): return self.__track
    def get_track (self):
        import hj.db
        return hj.db.fetch (self.__track)[self.__track]

    def get_map_fingerprint (self)->[str]: return self.__map
    def get_maps (self)->'Map':
        import hj.util.geo
        return hj.util.geo.Joined(fp=self.__map)
    
    def get_photo_fingerprints (self)->[str]: return self.__photos
    def get_photos (self)->'[Photo]':
        import hj.db
        return [p for p in hj.db.fetch (self.__photos).values()]

    def get_waypoint_fingerprints (self)->[str]: return self.__waypts
    def get_waypoints (self)->'[GPSElement]':
        import hj.db
        return [w for w in hj.db.fetch (self.__waypts).values()]
    pass

class GPSElement(object):
    Point = collections.namedtuple ('Point', ['elev', 'lat', 'lon', 'time'])

    def as_dict (self)->{}:
        return {'description':self.get_desc(),
                'fingerprint':self.get_fingerprint(),
                'first':{'lat':self.get_points()[0].lat,
                         'lon':self.get_points()[0].lon},
                'label':self.get_label(),
                'name':self.get_name()}
    
    def get_desc (self)->str:
        '''User provided amd mutaable text scribing this GPS Element'''
        raise NotImplementedError()
    
    def get_fingerprint (self)->str:
        '''An identifier that is immutable but unique

        The identifier should only be based on [Point] contain within this
        element. It shoud not change when the description or label change as
        these items are user mutable over the life of any instance of this
        element.
        '''
        raise NotImplementedError()

    def get_label (self)->str:
        '''User provided and mutable short text description'''
        raise NotImplementedError()
    
    def get_name (self)->str:
        '''The original file name that provided this GPS data

        This is the name assigned by the device during the import phase.
        '''
        raise NotImplementedError()
    
    def get_points (self)->[Point]:
        '''The list of GPS data'''
        raise NotImplementedError()

    def get_rawfp (self)->str:
        '''Return the fingerprint of the raw content backed by this wrapper

        If this object backs a raw content item, then it should return a
        string represeting the fingerprint of the raw content. Otherwise, it
        should not implement this method resulting in a NotImplementedError.
        '''
        raise NotImplementedError('Not backed by a raw object')
    
    def get_type (self):
        '''Return the hj.db.EntryType for route, track, or waypoint'''
        raise NotImplementedError()

    def set_desc (self, description:str)->None:
        '''Set, potentially updating, the description of this element'''
        raise NotImplementedError()

    def set_label (self, label:str)->None:
        '''Set, potentially updating, the label of this element'''
        raise NotImplementedError()

    def update (self, d:{})->None:
        if 'description' in d: self.set_desc (d['description'])
        if 'label' in d: self.set_label (d['label'])
        return
    pass

class Map(object):
    class Corner(enum.Enum):
        NorthEast = 0
        SouthEast = 1
        SouthWest = 2
        NorthWest = 3
        pass
    
    # the affine transform given pixel p and line l in a raster is:
    #   X(p,l) = Ox + Px * p + Lx * l
    #   Y(p,l) = Oy + Py * p + Ly * l
    Affine = collections.namedtuple ('Affine', ['Ox', 'Px', 'Lx',
                                                'Oy', 'Py', 'Ly'])
    
    # these two named tuples are used for the bounding box
    Pixel = collections.namedtuple ('Pixel', ['col', 'row'])
    Point = collections.namedtuple ('Point', ['lat', 'lon'])

    def _affine_transform(self)->Affine:
        '''Return the affine transform for PIXEL to WGS84
        '''
        raise NotImplementedError()

    def _contains (self, pts:[Point]):
        import hj.util.geo
        import matplotlib.path
        import numpy
        
        bb = matplotlib.path.Path([(p.lon, p.lat) for p in self.get_wgs84_bb()],
                                  [matplotlib.path.Path.MOVETO] +
                                  [matplotlib.path.Path.LINETO
                                   for i in range(len(self.get_wgs84_bb())-2)] +
                                  [matplotlib.path.Path.CLOSEPOLY])
        p = hj.util.geo.as_numpy_array (pts)
        path = numpy.empty ((p.shape[0],2))
        path[:,0] = p[:,hj.util.geo.LON]
        path[:,1] = p[:,hj.util.geo.LAT]
        return bb.contains_points (path)
    
    def all (self, pts:[Point])->bool:
        '''Determine of any of the given points are contained in the map

        Returns a single boolean. True if ALL of the points are contained
        within this map. False otherwise.
        '''
        return self._contains (pts).all()

    def any (self, pts:[Point])->bool:
        '''Determine of any of the given points are contained in the map

        Returns a single boolean. True if ANY of the points are contained
        within this map. False otherwise.
        '''
        return self._contains (pts).any()
    
    def get_fingerprint(self)->str:
        '''Return the fingerprint of the map
        '''
        raise NotImmplementedError()
        
    def get_image(self)->numpy.array:
        '''Return the full image
        '''
        raise NotImplementedError()

    def get_name(self)->str:
        '''Return the string representation of the map
        '''
        raise NotImplementedError()
    
    def get_pixel_bb(self)->[Pixel]:
        '''Return the bounding box in pixel coordinates
        '''
        raise NotImplementedError()

    def get_rawfp (self)->str:
        '''Return the fingerprint of the raw content backed by this wrapper

        If this object backs a raw content item, then it should return a
        string represeting the fingerprint of the raw content. Otherwise, it
        should not implement this method resulting in a NotImplementedError.
        '''
        raise NotImplementedError('Not backed by a raw object')
    
    def get_wgs84_bb(self)->[Point]:
        '''Return the bounding box in WGS84 coordinates
        '''
        raise NotImplementedError()

    def inverse (self, p:Point, ca:float=0.5, ra:float=0.5)->Pixel:
        '''Use the inverse affine to copute the Pixel from a Point

        ca : column adjust where 0.5 mimics rounding
        ra : row adjust where 0.5 mimics rounding
        '''
        T = self._affine_transform()
        Ox = p.lon - T.Ox
        Oy = p.lat - T.Oy
        return Map.Pixel(col=int((Oy/T.Ly - Ox/T.Lx)/(T.Py/T.Ly - T.Px/T.Lx) + .5),
                         row=int((Oy/T.Py - Ox/T.Px)/(T.Ly/T.Py - T.Lx/T.Px) + .5))

    def raw_shape(self)->Pixel:
        '''Return the number of rows and columns for the entire image
        '''
        raise NotImplementedError()

    def transform (self, p:Pixel)->Point:
        T = self._affine_transform()
        return Map.Point(lat=T.Oy + T.Py*p.col + T.Ly*p.row,
                         lon=T.Ox + T.Px*p.col + T.Lx*p.row)
    
    def which (self, pts:[Point])->[int]:
        '''Determine which of the points are contained within the map

        Returns the index of those points that are contained within this map
        '''
        import matplotlib.mlab
        return matplotlib.mlab.find (self._contains (pts))
    pass

class Photos(object):
    pass
