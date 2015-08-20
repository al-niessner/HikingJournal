'''Front end factory for reading a variety of devices
'''
import enum
import io
import shutil

class Interface(object):
    '''All GPS units are supported through this interface

    Use the constructor (__init__) to accept kwds from open() to build
    a specific instance of this interface for the rest of the hiking journal
    to use. The interface should make all devices look like a file system in
    the end. It should translate from whatever proprietary format the device
    actually uses to GPX for a uniform data model through the hiking journal.

    At the device level, the user should see the device as a list of files
    with routes, tracks, and waypoints separated into their own files.
    I chose this particular architecture/design because it mimics the half
    dozen or so GPS units that I have examined. After the device layer, the
    hiking journal is free to intermix the types.

    There are 3 generators in this interface which are the part that the rest
    of the interface cares about. When called, the generators should return the
    same name if the same data is present. What this means is that if
    shutil.move() is used and the device is not a filesystem, then when an
    open is done again and the same information is on the device, then it should
    generate the same filenames as the previous time. How exactly that is done
    is solely the responsibility of the implementer but there are two obvious
    mechanisms: One, use the time the item was generated. Two, use unique hash
    like md5 or sha1. The former is the mechanism used by the half dozen or
    so devices I have examined.
    '''

    def __exit__(mgr, *args):
        '''for the "with" clause'''
        return False # does nothing by default so overriding is not required
    
    def __enter__(mgr):
        '''for the "with" clause'''
        return mgr # does nothing by default so overriding is not required

    def _clear(self):
        '''clear the device memory'''
        raise NotImplementedError()
    
    def _close(self):
        '''given the interface a change to close the device if needed'''
        return # does nothing by default so overriding is not required
    
    def fetch (self, dfn:str, move:bool)->io.TextIOBase:
        '''read the specified item from the device into a string buffer

        The device gets stuck with converting its native format to GPX at this
        point. The device driver is already doing the work of making all devices
        look like a file, so it has to go one step further and convert to the
        actual data stream to GPX.
        
        dfn : device file name
        move : move the file erasing it from the driver view but not
               necessarily from the hardware itself (depnds on what the hardware
               can support, but it should not show up in the next update() call)
        returns an io.StringIO with the GPX contents of the file
        '''
        raise NotImplementedError()
    
    def routes(self):
        '''a generator that yields one route filename at a time'''
        raise NotImplementedError()

    def tracks(self):
        '''a generator that yields one track filename at a time'''
        raise NotImplementedError()

    def update (self):
        '''update the data loaded from the device'''
        raise NotImplementedError()
        
    def waypoints(self):
        '''a generator that yields one waypoint filename at a time'''
        raise NotImplementedError()
    pass

class Type(enum.Enum):
    local_file = 0
    garmin_etrex_10 = 1
    pass

def close (di : Interface, clear : bool=False) -> None:
    if clear: di._clear()
    di._close()
    return

def open (t : Type, **kwds) -> Interface:
    g,l = {},{}
    exec ('import hj.device.' + t.name + '\n' +
          'I = hj.device.' + t.name + '.Interface', g, l)
    I = l['I']
    result = None
    
    if len (kwds) == 0: help (I)
    else:
        result = I(**kwds)
        result.update()
        pass
    return result
