
import collections
import datetime
import enum
import numpy

VERSION = collections.namedtuple ('VERSION', ['design','impl','bugfix'])

class Version(object):
    def __getstate__(self):
        print ('calling get state')
        state = self.__dict__.copy()
        state['_version_'] = self._version()
        return state
    
    def __setstate__ (self,state:{}):
        cur_ver = self._version()
        old_ver = state['_version_']
        print ('calling set state', cur_ver, old_ver)
        del state['_version_']
        
        if self.later (old_ver): self._upgrade (old_ver)
        self.__dict__.update (state)
        return
    
    def _upgrade(self): raise NotImplementedError()
    def _version(self)->VERSION: raise NotImplementedError()

    def later (self, than:VERSION, now:VERSION=None):
        if now is None: now = self._version()
        if than.design == now.design:
            if than.impl == now.impl: result = than.bugfix < now.bugfix
            else: result = than.impl < now.impl
        else: result = than.design < now.design
        return result
    pass

class Annotated(Version):
    def __init__(self, tid:str, mid:str=None, pids:[str]=[], wids:[str]=[]):
        object.__init__(self)
        import hj.db

        self.__facets = dict()
        self.__fp = hj.db._id (('Annotated Track: ' + tid).encode())
        self.__map = mid
        self.__photos = pids
        self.__track = tid
        self.__waypts = wids
        return

    def _upgrade(self): raise NotImplementedError()
    def _version(self)->VERSION: return Version(1,1,0)

    def get_fingerprint (self)->str:
        '''An identifier that is immutable but unique'''
        return self.__fp

    def get_track_fingerprint (self): return self.__track
    def get_track (self):
        import hj.db
        return hj.db.fetch ([self.__track])[self.__track]

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

    def get_facets(self): return self.__facets.copy()
    def set_facets (self, facets:{}): self.__facets = facets.copy()
    def update (self, facets:{}): self.__facets.update (facets)
    pass

class Entry(Version):
    def __init__ (self, aids:[str], label:str):
        object.__init__(self)
        import hj.db
        
        self.__aids = aids
        self.__fp = hj.db._id (('Annotations: ' + '.'.join (aids)).encode())
        self.__label = label
        self.__modified = datetime.datetime.utcnow();
        self.__segment = dict([(aid,'') for aid in self.__aids])
        return

    def _segment (self, a):
        import hj.db

        t = hj.db.fetch ([a])[a].get_track()
        e = [p.elev for p in t.get_points()]
        tim = t.get_points()[0].time
        gain = numpy.diff (e)
        gain = round (gain[0 < gain].sum())
        delta = distance = 'undefined'
        trailend = 'N {1}  W {2}  ev {0:4.0f}'.format (*t.get_points()[-1])
        trailhead = 'N {1}  W {2}  ev {0:4.0f}'.format (*t.get_points()[0])

        if tim is None: dt_stamp = ''
        elif isinstance (tim, datetime.datetime):
            dt_stamp = tim.strftime ('%Y-%m-%d %H:%M')
        else: dt_stamp = str(tim)
        
        return {'aid':a,
                'change':round (e[-1] - e[0]),
                'date':dt_stamp,
                'delta':delta,
                'gain':gain,
                'label':t.get_label(),
                'len':distance,
                'te':trailend, 'th':trailhead,
                'text':self.__segment[a],
                'tid':t.get_fingerprint(),
                'walked':distance}
    
    def _upgrade(self): raise NotImplementedError()
    def _version(self)->VERSION: return Version(1,1,0)

    def as_dict(self)->{}:
        return {'id':self.get_fingerprint(),
                'nsegs':len (self.__aids),
                'mdate':self.__modified.strftime('%Y-%m-%d %H:%M'),
                'segs':[self._segment (a) for a in self.__aids]}
    
    def get_fingerprint (self)->str:
        '''An identifier that is immutable but unique'''
        return self.__fp

    def get_label (self)->str:
        '''User provided and mutable short text description'''
        return self.__label

    def get_points (self):
        import hj.db
        
        pts = []
        for a in self.__aids: pts.extend (hj.db.fetch
                                          ([a])[a].get_track().get_points())
        return pts
                                          
    def get_segment (self, aid:str=None)->str:
        if len(self.__aids) == 1 and aid is None: aid = self.__aids[0]
        if aid is None:
            raise AttributeError('aid must be defined if more than one segment')
        return self.__segment[aid]
    
    def set_label (self, label:str)->None:
        '''Set, potentially updating, the label of this element'''
        self.__label = label
        return

    def set_segment (self, text, aid:str=None)->None:
        if len(self.__aids) == 1 and aid is None: aid = self.__aids[0]
        if aid is None:
            raise AttributeError('aid must be defined if more than one segment')

        if text != self.__segment[aid]:
            self.__modified = datetime.datetime.utcnow()
            self.__segment[aid] = text
            pass
        return
    
    def update (self, d:{})->None:
        for s in d['segs']: self.set_segment (s['text'], s['aid'])
        return
    pass

class GPSElement(Version):
    Point = collections.namedtuple ('Point', ['elev', 'lat', 'lon', 'time'])

    def _upgrade(self): raise NotImplementedError()
    def _version(self)->VERSION: return Version(1,1,0)

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

class Map(Version):
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
    
    def _upgrade(self): raise NotImplementedError()
    def _version(self)->VERSION: return Version(1,1,0)

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
