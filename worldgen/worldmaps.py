import numpy as np
from locations import Location

class Worldmap(np.ndarray):
    def __new__(subtype, shape, dtype=object, buffer=None, offset=0,
          strides=None, order=None, info=None):
        obj = np.ndarray.__new__(subtype, shape, dtype, buffer, offset, strides,
                         order)
        obj.info = info
        ## Attributes that should be generated in the DS process.
        obj.ds_generated = ['smoothness','altitude']
        ## All attributes
        obj.has = ['smoothness','altitude']
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

    def wmiter(self, x_range=(0, -1), y_range=(0, -1), step=(1, 1)):
        '''
        Improves upon ndenumerate by iterating through a slice of the
        array, and taking steps.
        x_range: The range of x to slice.
        y_range: The range of y to slice.
        step: Steps between yields, in (x, y)
        '''
        x_min = x_range[0]
        x_max = x_range[1]
        y_min = y_range[0]
        y_max = y_range[1]
        x_step = step[0]
        y_step = step[1]

        if x_max < 0:
            x_max = self.shape[0] + x_max + 1
        if y_max < 0:
            y_max = self.shape[1] + y_max + 1

        for (x, y), loc in np.ndenumerate(self[x_min:x_max, y_min:y_max]):
            if x % x_step == 0 and y % y_step == 0:
                yield (x, y), loc