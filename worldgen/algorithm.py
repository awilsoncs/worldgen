import numpy as np
import random
import math
import pygame

def process(window, s):
    '''
    Generate a DS heightmap.
    window: Surface to apply the PixelArray
    s: the size tuple of the window.
    '''
    a = get_array((s,s))
    i = 1
    print "Beginning height map..."
    print "This may take a while"
    while s > 2:
        step(a, s, i)
        s = int(math.ceil(s/2.0))
        i += 1
    print "Final pass..."
    step(a, s, i)
    # Finalize the array
    scale_array(a)
    return a

def step(a, s, i):
    '''
    Process one step of Diamond/Square algorithm.
    a: Array to be operated on
    s: The size tuple of the operating square
    i: Int number of iterations
    '''
    ## TO-DO: This could likely be multithreaded to speed it up.
    print "."
    shape = a.shape
    ## To perform a step, iterate across each s*s square in the array twice.
    ## DS requires that the first line of each square is the last line of the
    ## previous square. This leaves an additional column, so iterate one short.
    
    ## Diamond step
    for x in range(0, shape[0]-1, s-1):
        for y in range(0, shape[1]-1, s-1):
            sub_coords = (x, x+s-1, y, y+s-1)
            ## debug sanity check, test for misalignment
            if x+s - x != y+s - y:
                print "ERROR: diamond call"
                print "\tNot a square (%d, %d)" % (x+s - x, y+s -y)
                assert False
            sub_diamond(a, sub_coords, i)
    
    ## Square step
    for x in range(0, shape[0]-1, s-1):
        for y in range(0, shape[1]-1, s-1):
            sub_coords = (x, x+s-1, y, y+s-1)
            ## debug sanity check, test for misalignment
            if x+s - x != y+s - y:
                print "ERROR: square call"
                print "\tNot a square (%d, %d)" % (x+s - x, y+s -y)
                assert False
            sub_square(a, sub_coords, i)

def sub_diamond(a, c, i):
    '''
    Set the center of coords to the average of the four corners, plus random 
    noise.
    a: Array to be operated on
    c: Coordinates to be operated on
        (x1, x2, y1, y2)
    i: Int number of iterations    
    '''
    x = math.ceil((c[0] + c[1]) / 2.0)
    y = math.ceil((c[2] + c[3]) / 2.0)
    
    if a[x, y] == 0.0:
        corner_a = a[c[0], c[2]]
        corner_b = a[c[0], c[3]]
        corner_c = a[c[1], c[2]]
        corner_d = a[c[1], c[3]]
        v = (corner_a, corner_b, corner_c, corner_d)
        v = get_value(v, i)
        a[x, y] = v
        #debug, make sure value was changed
        if a[x, y] == 0.0:
            print "ERROR: Value not assigned at (%d, %d)" % (x, y)
            assert False
            
def sub_square(a, c, i):
    '''
    Array a has four sides with midpoints. Perform sub_square on each side.
    a: Array to be operated on
    c: Coordinates to be operated on
        (x1, x2, y1, y2)
    i: Int number of iterations    
    '''
    sub_a = (c[0], c[1], c[2], c[2])
    sub_b = (c[0], c[1], c[3], c[3])
    sub_c = (c[0], c[0], c[2], c[3])
    sub_d = (c[1], c[1], c[2], c[3])
    subs = [sub_a, sub_b, sub_c, sub_d]
    for sub in subs:
        diamond(a, sub, i)
        
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
    v += random.uniform(-1.0,1.0) / float(i)
    #debug, make sure we're getting a float back
    if type(v) != float:
        print "Error: get_value failed"
        print "\tReturned non-float"
        assert False
    return v
    
## Pre-generation functions

def get_array(s):
    '''
    Generate an array based on size s and call get_value on the corners.
    s: Size tuple of new array.
    '''
    print "Getting new array..."
    a = np.zeros((s[0], s[1]))
    print "Seeding corners..."
    a[0, 0] =       get_value()
    a[0, -1] =      get_value()
    a[-1, 0] =      get_value()
    a[-1, -1] =     get_value()
    return a
    
## Post-generation functions

def scale_array(a):
    '''
    Scales all values in the array to 0.0-1.0 floats.
    a: Array to be operated on.
    '''
    print "Scaling Array..."
    shape = a.shape
    maximum = None
    for x in np.nditer(a):
        if abs(x) > maximum:
            maximum = abs(x)
                
    for x in range(shape[0]):
        for y in range(shape[1]):
            a[x, y] = a[x, y] / (2 * maximum)
            a[x, y] += 0.5
            
            ## Debug, make sure the scaling worked
            if a[x, y] < 0.0:
                print "ERROR: In scale_array debug, found x < 0.0"
                assert False
            elif a[x, y] > 1.0:
                print "ERROR: In scale_array debug, found x > 1.0"
                assert False
                
def build_pxarray(surface, a):
    '''
    Returns a greyscale pxarray based on input array.
    surface: A surface object to add the pxarray to.
    a: An array with values 0.0-1.0
    '''
    print "Rendering..."
    pxarray = pygame.PixelArray(surface)
    for x in range(a.shape[0]):
        for y in range(a.shape[1]):
            v = a[x, y] * 255
            pxarray[x, y] = (v, v, v)
    return pxarray
