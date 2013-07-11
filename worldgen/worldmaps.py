import numpy as np

from locations import Location

class Worldmap(np.ndarray):

    def __new__(subtype, shape, dtype=object, buffer=None, offset=0,
          strides=None, order=None, info=None):
        obj = np.ndarray.__new__(subtype, shape, dtype, buffer, offset,
                                strides, order)
        obj.info = info
        ## Attributes that should be generated in the DS process.
        obj.ds_generated = ['smoothness', 'elevation', 'volcanism',
                            'solubility', 'precious_minerals', 
                            'economic_minerals']
        return obj

    def __array_finalize__(self, obj):
        if obj is None: return
        self.info = getattr(obj, 'info', None)
    
    def get_view(self, key):
        """Return an array of values based on the key"""
        array = np.empty(self.shape)
        for (x, y), location in np.ndenumerate(self):
            array[x, y] = location[key]
        return array

    def get(self, (x, y), key):
        """Return the value for attribute get_by at (x, y)."""
        if self[x, y] is None:
            self[x, y] = Location((x, y))
        if self[x, y].has_key(key):
            return self[x, y][key]
        else:
            return None
        
    def put(self, (x, y), key, value):
        """Place the value in the map at (x, y)."""
        if self[x, y] is None:
            self[x, y] = Location((x, y))
        if not self[x, y].locked:
            self[x, y].update({key : value})

    def add(self, (x, y), key, value):
        """As put, but adds to the current value instead of replacing."""
        if self[x, y] is None:
            self[x, y] = Location((x, y))
        if not self[x, y].locked:
            if key in self[x, y]:
                value += self.get((x, y), key)
            self.put((x, y), key, value)

    def wmiter(self, x_range=(0, -1), y_range=(0, -1), step=(1, 1)):
        """Improves upon ndenumerate by iterating through a slice of the
        array, and taking steps.
        """
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
            if x % x_step is 0 and y % y_step is 0:
                yield (x, y), loc

    def midpoint_iter(self, x_range=(0, -1), y_range=(0, -1), iteration=1):
        x_min = x_range[0]
        x_max = x_range[1]
        y_min = y_range[0]
        y_max = y_range[1]

        if x_max < 0:
            x_max = self.shape[0] + x_max
        if y_max < 0:
            y_max = self.shape[1] + y_max
        if x_min < x_max - 1 or y_min < y_max - 1:
            yield (x_min, x_max, y_min, y_max, iteration)
            for output in self.midpoint_iter(
                    x_range = (x_min, (x_max + x_min) / 2),
                    y_range = (y_min, (y_max + y_min) / 2),
                    iteration = iteration + 1):
                yield output
            for output in self.midpoint_iter(
                    x_range = ((x_min + x_max) / 2, x_max),
                    y_range = (y_min, (y_max + y_min) / 2),
                    iteration = iteration + 1):
                yield output
            for output in self.midpoint_iter(
                    x_range = (x_min, (x_max + x_min) / 2),
                    y_range = ((y_min + y_max) / 2, y_max),
                    iteration = iteration + 1):
                yield output
            for output in self.midpoint_iter(
                    x_range = ((x_min + x_max) / 2, x_max),
                    y_range = ((y_min + y_max) / 2, y_max),
                    iteration = iteration + 1):
                yield output
