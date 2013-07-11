from copy import copy
import math
import numpy as np
import random
    
def process(worldmap):
    """Populate and return a Worldmap with values."""
    seed_corners(worldmap)
    sew_seams(worldmap)
    step(worldmap)
    scale_array(worldmap)
    return worldmap

def step(worldmap):
    """Perform the diamond-square algorithm."""
    print "Beginning map..."
    print "This may take a while"

    for coords in worldmap.midpoint_iter():
        x1, x2 = coords[0], coords[1]
        y1, y2 = coords[2], coords[3]
        sub_coords = (x1, x2, y1, y2)
        iteration = coords[4]

        diamond(worldmap, sub_coords, iteration)
        square(worldmap, sub_coords, iteration)

def diamond(worldmap, coords, iteration):
    """Set the center of coords to the average of the four corners, plus
    random noise.   
    """
    x = math.ceil((coords[0] + coords[1]) / 2.0)
    y = math.ceil((coords[2] + coords[3]) / 2.0)
    
    if worldmap[x, y] == None or worldmap[x, y].locked == False:
        for key in worldmap.ds_generated:
            corner_a = worldmap[coords[0], coords[2]][key]
            corner_b = worldmap[coords[0], coords[3]][key]
            corner_c = worldmap[coords[1], coords[2]][key]
            corner_d = worldmap[coords[1], coords[3]][key]
            values = (corner_a, corner_b, corner_c, corner_d)
            if key == 'smoothness':
                value = get_value(values, iteration)
            else:
                smoothness = worldmap[x, y]['smoothness']
                value = get_value(values, iteration, smoothness)
            worldmap.add((x, y), key, value) 
        worldmap[x, y].locked = True     

def square(worldmap, coords, iteration):
    """Perform diamond on the four sides of the coords."""
    x1, x2 = coords[0], coords[1]
    y1, y2 = coords[2], coords[3]

    side_a = (x1, x2, y1, y1)
    side_b = (x1, x2, y2, y2)
    side_c = (x1, x1, y1, y2)
    side_d = (x2, x2, y1, y2)
    sides = [side_a, side_b, side_c, side_d]
    
    # for a 1D subarray, diamond works the same as square should.
    for side in sides:
        diamond(worldmap, side, iteration)
        
## Utilities

def get_value(values=1, iteration=1, smoothing=1):
    """Return a float of random noise plus average of values."""
    if type(values) == int:
        value = values
    else:
        value = float(sum(values)) / float(len(values))
    variance = smoothing * 5.0;
    value += random.uniform(-variance, variance) / float(iteration)
    return value

## Pre-generation functions

def seed_corners(worldmap):
    """Get values for the corners of the wm array."""
    print "Seeding corners..."
    for key in worldmap.ds_generated:
        value_a = get_value()
        value_b = get_value()
    
        worldmap.add((0, 0), key, value_a)
        worldmap.add((-1, 0), key, value_a)

        worldmap.add((0, -1), key, value_b)
        worldmap.add((-1, -1), key, value_b)
    
    worldmap[0, 0].locked = True
    worldmap[0, -1].locked = True
    worldmap[-1, 0].locked = True
    worldmap[-1, -1].locked = True

def sew_seams(worldmap):
    """Insert values into the edges of the map to create continuous lines."""
    print "Sewing seams..."
    
    ## Vertical seams
    height = worldmap.shape[1]
    iteration = 1
    while height > 1:
        box = (1, height - 1)
        for (x, y), location in worldmap.wmiter((0, 1), (0, -2), box):
            coords = (0, 0, y, y + box[1])
            diamond(worldmap, coords, iteration)
            worldmap[-1, y] = copy(worldmap[0, y])
        iteration += 1
        height = int(math.ceil(height / 2.0))

    ## Horizonal seams
    north_loc = worldmap[0, 0]
    south_loc = worldmap[0, -1]
    for x in xrange(worldmap.shape[0]):
        worldmap[x, 0] = copy(north_loc)
        worldmap[x, -1] = copy(south_loc)
    
## Post-generation functions

def scale_array(worldmap):
    """Scale all values in the array to 0.0-1.0 floats."""
    # find the min/max for each key
    print "Scaling array..."
    max_dict = {}
    min_dict = {}

    for (x, y), location in np.ndenumerate(worldmap):
        for key in worldmap.ds_generated:
            if key not in max_dict or location[key] > max_dict[key]:
                max_dict[key] = location[key]
            if key not in min_dict or location[key] < min_dict[key]:
                min_dict[key] = location[key]
    
    # Adjust the values
    for (x, y), location in np.ndenumerate(worldmap):
        for key in worldmap.ds_generated:
            value = location[key] - min_dict[key]
            value = value / (max_dict[key] - min_dict[key])
            if key == 'elevation':
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
    x = x / 4.0 - 0.125
    ## if x is negative, python won't like the math:
    if x < 0:
        ## Real root: 
        ## (-x)**3 = -(x)**3
        x = (-x)**(1.0 / 3.0)
        x = -x
    else:
        x = x**(1.0 / 3.0)
    return (0.5) + (0.25) * x

def elevation_end(x):
    """Adjust end ranges of float x"""
    x = (27.0 / 64.0) * (2 * x - 1)**5 + 3.0 / 64.0
    return x