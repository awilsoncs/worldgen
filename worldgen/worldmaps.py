import numpy as np

from locations import Location

def world_map(shape):
    return np.zeros((513, 257,), dtype=(('locked', 'int8')
                                        ('smoothness', 'float16'),
                                        ('elevation', 'float16'),
                                        ('volcanism', 'float16'),
                                        ('solubility', 'float16'),
                                        ('precious minerals', 'float16'),
                                        ('economic minerals', 'float16'),
                                        ('water depth', 'float16'),
                                        ('precipitation', 'float16')))

class Worldmap(np.ndarray):
    def __new__(cls, shape, dtype=object, buffer=None, offset=0,
                strides=None, order=None, info=None):
        obj = np.ndarray.__new__(cls, shape, dtype, buffer, offset,
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
            self[x, y].update({key: value})

    def lock(self, (x, y)):
        self[x, y].locked = True

    def add(self, (x, y), key, value):
        """As put, but adds to the current value instead of replacing."""
        if self[x, y] is None:
            self[x, y] = Location((x, y))
        if not self[x, y].locked:
            if key in self[x, y]:
                value += self.get((x, y), key)
            self.put((x, y), key, value)
