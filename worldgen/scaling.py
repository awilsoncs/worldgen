import math

import numpy as np


def elevation(x):
    """Return float x adjusted for earth-like elevations"""
    vector_atan = np.vectorize(math.atan)
    y = 20 * x - 10
    y2 = x - 0.5
    return 0.05 * (vector_atan(y) + 220 * (y2 ** 5)) + 0.5


def normalize(array):
    """Scale all values in the array to 0.0-1.0 floats."""
    high = array.max()
    low = array.min()
    rng = high - low
    array[:] = 1.0 - ((high - array) / rng)
