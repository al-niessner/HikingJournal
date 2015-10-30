
import gpxpy
import hj
import hj.db
import io

class Element(hj.GPSElement):
    def __init__ (self, bfn:str, data):
        '''Initialize a GPX Element type

        bfn  - the base file name assigned by the device
        data - the gpxpy parsed data to be archived
        '''
        self.__desc = ''
        self.__fp = ''
        self.__label = ''
        self.__name = ''
        self.__points = []
        return

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
    
    def get_points (self)->[hj.GPSElement.Point]:
        '''The list of GPS data'''
        raise NotImplementedError()

    def get_type (self)->hj.db.EntryType:
        '''Return the hj.db.EntryType for route, track, or waypoint'''
        raise NotImplementedError()

    def set_desc (self, description:str)->None:
        '''Set, potentially updating, the description of this element'''
        raise NotImplementedError()

    def set_label (self, label:str)->None:
        '''Set, potentially updating, the label of this element'''
        raise NotImplementedError()
    pass

def parse (data:io.TextIOBase)->[Element]:
    result = []
    gpx = gpxpy.parse (data)
    return result
