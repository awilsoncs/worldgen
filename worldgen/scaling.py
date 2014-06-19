import math

import numpy as np


def scale(layer):
    """Scale all values in the array to 0.0-1.0 floats."""
    high = layer.max()
    low = layer.min()
    rng = high - low
    layer[:] = 1.0 - ((high - layer) / rng)


def elevation(x):
    """Return float x adjusted for earth-like elevations"""
    vatan = np.vectorize(math.atan)
    y = 20 * x - 10
    y2 = x - 0.5
    return 0.05 * (vatan(y) + 220 * (y2**5)) + 0.5