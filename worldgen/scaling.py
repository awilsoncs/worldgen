import math

import numpy as np


def scale(worldmap, values):

    """Scale all values in the array to 0.0-1.0 floats."""
    # find the min/max for each key
    print "Scaling array..."
    max_dict = {}
    min_dict = {}
    for (x, y), location in np.ndenumerate(worldmap):
        for key in values:
            if key not in max_dict or location[key] > max_dict[key]:
                max_dict[key] = location[key]
            if key not in min_dict or location[key] < min_dict[key]:
                min_dict[key] = location[key]
    
    # Adjust the values
    for (x, y), location in np.ndenumerate(worldmap):
        for key in values:
            value = location[key] - min_dict[key]
            value = value / (max_dict[key] - min_dict[key])
            if key is 'elevation':
                location[key] = elevation(value)
            else:
                location[key] = value

def elevation(x):
    """Return float x adjusted for earthlike elevations"""
    x = elevation_central(x) + elevation_end(x)
    if x > 1.0:
        x = math.floor(x)
    return x

def elevation_central(x):
    """Adjust central ranges of float x"""
    x = x/4.0 - 0.125
    ## if x is negative, python won't like the math:
    if x < 0:
        ## Real root: 
        ## (-x)**3 = -(x)**3
        x = (-x)**(1.0 / 3.0)
        x = -x
    else:
        x = x**(1.0 / 3.0)
    return 0.5 + 0.25*x

def elevation_end(x):
    """Adjust end ranges of float x"""
    x = (27.0 / 64.0) * (2*x - 1)**5 + 3.0/64.0
    return x