
import collections
import numpy

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
