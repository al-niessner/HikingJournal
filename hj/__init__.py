
import collections
import numpy

class Annotated(object):
    def __init__(self, track:'GPSElement', maps:'[Map]'=[],
                 photos:'[Photo]'=[], waypts:'[GPSElement]'=[]):
        object.__init__(self)
        self.__maps = [m.fingerprint() for m in maps]
        self.__photos = [p.fingerprint() for p in photos]
        self.__track = track.fingerprint()
        self.__waypts = [w.fingerprint() for w in waypts]
        return

    def get_fingerprint (self)->str:
        '''An identifier that is immutable but unique'''
        return self.__track

    def get_track_fingerprint (self): return self.__track
    def get_track (self):
        import hj.db
        result = [t.fingerprint() == self.__track
                  for t in hj.db.filter (hj.db.EntryType.track)]
        return result[0]

    def get_map_fingerprints (self)->[str]: return self.__maps
    def get_maps (self)->'[Map]':
        import hj.db
        result = []
        for m in hj.db.filter (hj.db.EntryType.map):
            if 0 < self.__maps.count (m.fingerprint()): result.append (m)
            pass
        return result
    
    def get_photo_fingerprints (self)->[str]: return self.__photos
    def get_photos (self)->'[Photo]':
        import hj.db
        result = []
        for p in hj.db.filter (hj.db.EntryType.photo):
            if 0 < self.__photos.count (p.fingerprint()): result.append (p)
            pass
        return result

    def get_waypoint_fingerprints (self)->[str]: return self.__waypts
    def get_waypoints (self)->'[GPSElement]':
        import hj.db
        result = []
        for w in hj.db.filter (hj.db.EntryType.waypt):
            if 0 < self.__waypts.count (w.fingerprint()): result.append (w)
            pass
        return result

    def set_maps (self, maps:'[Map]')->None:
        '''Set, potentially updating, the maps annotating the related track'''
        self.__maps = [m.fingerprint() for m in maps]
        return
    
    def set_photos (self, photos:'[Photo]')->None:
        '''Set, potentially updating, the photos annotating the related track'''
        self.__photos = [p.fingerprint() for p in photos]
        return

    def set_waypoints (self, waypts:'[GPSElement]')->None:
        '''Set, potentially updating, the waypoints annotating the related track'''
        self.__waypts = [w.fingerprint() for w in waypts]
        return    
    pass

class GPSElement(object):
    Point = collections.namedtuple ('Point', ['elev', 'lat', 'lon', 'time'])

    def as_dict (self)->{}:
        return {'description':self.get_desc(),
                'fingerprint':self.get_fingerprint(),
                'label':self.get_label(),
                'name':self.get_label()}
    
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
    # the affine transform given pixel p and line l in a raster is:
    #   X(p,l) = Ox + Px * p + Lx * l
    #   Y(p,l) = Oy + Py * p + Ly * l
    Affine = collections.namedtuple ('Affine', ['Ox', 'Px', 'Lx',
                                                'Oy', 'Py', 'Ly'])
    
    # these two named tuples are used for the bounding box
    Pixel = collections.namedtuple ('Pixel', ['col', 'row'])
    Point = collections.namedtuple ('Point', ['lat', 'lon'])
    
    def get_affine_transform(self)->Affine:
        '''Return the affine transform for PIXEL to WGS84
        '''
        raise NotImplementedError()

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

    def get_wgs84_bb(self)->[Point]:
        '''Return the bounding box in WGS84 coordinates
        '''
        raise NotImplementedError()
    pass

class Photos(object):
    pass
