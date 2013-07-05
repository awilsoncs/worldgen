import math
import numpy as np
import random
    
def process(wm):
    '''
    Populate a Worldmap with values required by ds_generated.
    wm: The Worldmap object to operate on.
    '''
    s = wm.shape
    i = 1
    seed_corners(wm)
    sew_seams(wm)
    print "Beginning map..."
    print "This may take a while"
    while s[0] > 2 and s[1] > 2:
        step(wm, s, i)
        x = int(math.ceil(s[0]/2.0))
        y = int(math.ceil(s[1]/2.0))
        s = (x, y)
        i += 1
    print "Final pass..."
    step(wm, s, i)
    # Finalize the array
    scale_array(wm)
    return wm

def step(wm, s, i):
    '''
    Process one step of Diamond/Square algorithm.
    wm: Worldmap object to be operated on
    s: The size tuple of the operating square
    i: Int number of iterations
    '''
    print "."
    shape = wm.shape
    ## DS requires that the first line of each square is the last line of the
    ## previous square.
    square_x = s[0]-1
    square_y = s[1]-1
    ## This leaves an additional column, so iterate one short.
        
    for x in xrange(0, shape[0]-1, square_x):
        for y in xrange(0, shape[1]-1, square_y):
            sub_coords = (x, x+square_x, y, y+square_y)

            diamond(wm, sub_coords, i)
            square(wm, sub_coords, i)

def diamond(wm, c, i):
    '''
    Set the center of coords to the average of the four corners, plus random 
    noise.
    wm: Worldmap object to be operated on
    c: Coordinates to be operated on
        (x1, x2, y1, y2)
    i: Int number of iterations    
    '''
    x = math.ceil((c[0] + c[1]) / 2.0)
    y = math.ceil((c[2] + c[3]) / 2.0)
    
    for key in wm.ds_generated:
        if wm[x, y] == None or wm[x, y].locked == False:
            corner_a = wm[c[0], c[2]][key]
            corner_b = wm[c[0], c[3]][key]
            corner_c = wm[c[1], c[2]][key]
            corner_d = wm[c[1], c[3]][key]
            v = (corner_a, corner_b, corner_c, corner_d)
            v = get_value(v, i)
            wm.put((x, y), key, v) 
    wm[x, y].locked = True     

def square(wm, c, i):
    '''
    Array a has four sides with midpoints. Perform sub_diamond on each side.
    wm: The Worldmap object to operate.
    c: Coordinates to be operated on
        (x1, x2, y1, y2)
    i: Int number of iterations    
    '''
    sub_a = (c[0], c[1], c[2], c[2])
    sub_b = (c[0], c[1], c[3], c[3])
    sub_c = (c[0], c[0], c[2], c[3])
    sub_d = (c[1], c[1], c[2], c[3])
    subs = [sub_a, sub_b, sub_c, sub_d]
    # for a 1D subarray, diamond works the same as square should.
    for sub in subs:
        diamond(wm, sub, i)
        
## Utilities

def get_value(values=1, i=1):
    '''
    Returns float average of values +- an amount of random noise based on i.
    values: Tuple of values to be averaged.
    i: Int number of iterations
    '''
    if type(values) == int:
        v = values
    else:
        v = float(sum(values)) / float(len(values))
    v += random.uniform(-5.0,5.0) / float(i)
    return v

## Pre-generation functions

def seed_corners(wm):
    '''
    Get values for the corners of the wm array.
    wm: Worldmap object to operate on.
    '''
    print "Seeding corners..."
    for key in wm.ds_generated:
        value_a = get_value()
        value_b = get_value()
        wm.put((0, 0), key, value_a)
        wm.put((0, -1), key, value_b)
        wm.put((-1, 0), key, value_a)
        wm.put((-1, -1), key, value_b)
        
def sew_seams(wm):
    '''
    Inserts values into the edges of the map to create continuous lines.
    wm: Worldmap object to be operated on.
    '''
    print "Sewing seams..."
    
    ## Vertical seams
    height = wm.shape[1]
    i = 1
    while height > 1:
        for y in xrange(0, wm.shape[1]-1, height-1):
            for key in wm.ds_generated:
                top_value =    wm[0, y][key]
                bottom_value = wm[0, y+height-1][key]  

                v = get_value((top_value, bottom_value), i)
                
                wm.put((0, y + height / 2), key, v)
                wm.put((-1, y + height / 2), key, v)
            
            wm[0, y].locked = True
            wm[-1, y].locked = True
        
        i += 1
        height = int(math.ceil(height / 2.0))
    ## Horizonal seams
    north_loc = wm[0, 0]
    south_loc = wm[0, -1]
    for x in xrange(wm.shape[0]):
        for key in wm.ds_generated:
            v1 = north_loc[key]
            v2 = south_loc[key]
            
            wm.put((x, 0), key, v1)
            wm.put((x, -1), key, v2)
        wm[x, 0].locked = True
        wm[x, -1].locked = True
    
## Post-generation functions

def scale_array(wm):
    '''
    Scales all values in the array to 0.0-1.0 floats.
    wm: Worldmap object to be operated on.
    '''
    # find the min/max for each key
    max_dict = {}
    min_dict = {}

    for key in wm.ds_generated:
        for (x, y), location in np.ndenumerate(wm):
            if key not in max_dict or location[key] > max_dict[key]:
                max_dict[key] = location[key]
            if key not in min_dict or location[key] < min_dict[key]:
                min_dict[key] = location[key]
    
    # Adjust the values
    for (x, y), location in np.ndenumerate(wm):
        for key in wm.ds_generated:
            value = location[key] + abs(min_dict[key])
            value = value / (max_dict[key] + abs(min_dict[key]))
            location[key] = value