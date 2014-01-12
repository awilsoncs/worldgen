import math

import numpy as np

def scale(worldmap, values):
    """Scale all values in the array to 0.0-1.0 floats."""
    print "Scaling array..."
    for key in values:
        high = worldmap[key].max()
        low = worldmap[key].min()
        rng = high - low
        worldmap[key] = 1.0 - ((high - worldmap[key]) / rng)
    if 'elevation' in values:
        worldmap['elevation'] = elevation(worldmap['elevation'])


def elevation(x):
    """Return float x adjusted for earthlike elevations"""
    vatan = np.vectorize(math.atan)
    y = 20 * x - 10
    y2 = x - 0.5
    return 0.05 * (vatan(y) + 220 * (y2**5)) + 0.5