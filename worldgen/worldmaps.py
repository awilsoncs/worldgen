import numpy as np
from locations import Location

class Worldmap(np.ndarray):
    def __new__(subtype, shape, dtype=object, buffer=None, offset=0,
          strides=None, order=None, info=None):
        obj = np.ndarray.__new__(subtype, shape, dtype, buffer, offset, strides,
                         order)
        obj.info = info
        ## Attributes that should be generated in the DS process.
        obj.ds_generated = ['altitude']
        ## All attributes
        obj.has = ['altitude']
        return obj

    def __array_finalize__(self, obj):
        if obj is None: return
        self.info = getattr(obj, 'info', None)
    
    def get(self, (x, y), get_by):
        '''
        Returns the value for attribute get_by at (x, y).
        (x, y): The int coordinates to search.
        get_by: String to search the dict by.
        '''
        if self[x, y] == None:
            self[x, y] = Location((x, y))
        if self[x, y].has_key(get_by):
            return self[x, y][get_by]
        else:
            return None
        
    def put(self, (x, y), key, value):
        '''
        Places the given kwargs in the map at (x, y).
        (x, y): The int coordinates to place the values.
        **kwargs: Additional values to place at the coordinates.
        '''
        if self[x, y] == None:
            self[x, y] = Location((x, y))
        if self[x, y].locked == False:
            self[x, y].update({key : value})