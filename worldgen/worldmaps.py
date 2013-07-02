import numpy as np

class Worldmap(object):
    def __init__(self, size):
        '''
        size: (x, y) size of the Worldmap.
        '''
        self.size = size
        self.shape = size
        self.array = np.empty(size, dtype=object)
        self.ds_generated = ['altitude', 'ore']
        self.has = ['altitude', 'ore']
    
    def get(self, (x, y), get_by):
        '''
        Returns the value for attribute get_by at (x, y).
        (x, y): The int coordinates to search.
        get_by: String to search the dict by.
        '''
        if self.array[x, y] == None:
            self.array[x, y] = {}
        if self.array[x, y].has_key(get_by):
            return self.array[x, y][get_by]
        else:
            return None
        
    def put(self, (x, y), key, value):
        '''
        Places the given kwargs in the map at (x, y).
        (x, y): The int coordinates to place the values.
        **kwargs: Additional values to place at the coordinates.
        '''
        if self.array[x, y] == None:
            self.array[x, y] = dict()
        if key in self.has:
            self.array[x, y].update({key : value})
