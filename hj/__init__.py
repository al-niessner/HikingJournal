
import collections
import numpy

class GPSElement(object):
    Point = collections.namedtuple ('Point', ['elev', 'lat', 'lon', 'time'])

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
        '''The original file name that provided this GPS data'''
        raise NotImplementedError()
    
    def get_points (self)->[Point]:
        '''The list of GPS data'''
        raise NotImplementedError()
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
