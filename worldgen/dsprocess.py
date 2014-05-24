import random

import numpy as np

import scaling
import worldmaps

SOUTH_WEST = [0, 0]
NORTH_WEST = [0, -1]
SOUTH_EAST = [-1, 0]
NORTH_EAST = [-1, -1]


def process(worldmap):
    """Populate and return a Worldmap with values."""
    print "Building Geology..."
    smoothness = worldmap['smoothness']
    ds_process(smoothness)
    scaling.scale(smoothness)
    print "-Processing smoothness"
    seed_corners(worldmap)
    sew_seams(worldmap)
    for key in worldmaps.ds_generated:
        print "-Processing %s" % key
        layer = worldmap[key]
        ds_process(layer, smoothing_layer=worldmap['smoothness'])
        scaling.scale(layer)
    return worldmap


def seed_corners(worldmap):
    """Get values for the corners of the wm array."""
    print "-Seeding corners..."

    #Only get the western corners, we're going to seed the eastern ones from these.
    worldmap[0, 0] = stack_value(worldmap[0, 0])
    worldmap[0, -1] = stack_value(worldmap[0, -1])


def sew_seams(worldmap):
    """Insert values into the edges of the map to create continuous lines."""
    print "-Sewing seams..."

    ## Vertical seams
    worldmap[0, ] = sew_vertical(worldmap[0])
    worldmap[-1, ] = worldmap[0, ]

    ## Horizontal seams
    worldmap[:, 0] = worldmap[0, 0]
    worldmap[:, -1] = worldmap[0, -1]


def sew_vertical(seam, iteration=1):
    mid_y = midpoint(seam.shape[0])
    #seam[mid_y] = stack_value(seam[mid_y], [seam[0], seam[-1]], iteration)
    for key in worldmaps.ds_generated:
        seam[mid_y][key] = get_value([seam[0][key], seam[-1][key]], iteration)
    if mid_y > 1:
        seam[:mid_y + 1] = sew_vertical(seam[:mid_y + 1], iteration + 1)
        seam[mid_y:] = sew_vertical(seam[mid_y:], iteration + 1)
    return seam


def stack_value(stack, values=None, iteration=1, smoothing=1):
    if values is None:
        values = np.ones(stack.size, dtype=[('smoothness', 'float16'),
                                            ('elevation', 'float16'),
                                            ('volcanism', 'float16'),
                                            ('solubility', 'float16'),
                                            ('minerals', 'float16')])
    else:
        #TODO This does not work. We need a workaround to average the values.
        values = float(sum(values)) / float(len(values))
    variance = 5 * smoothing

    for key in worldmaps.ds_generated:
        noise = random.uniform(-1.0, 1.0) * variance / float(iteration)
        stack[key] = values[key] + noise
    return stack


def ds_process(layer, iteration=1, smoothing_layer=None):
    mid_x = midpoint(layer.shape[0])
    mid_y = midpoint(layer.shape[1])

    diamond(layer, iteration, smoothing_layer)
    square(layer, iteration, smoothing_layer)

    next_iteration = iteration + 1

    #Recursion on each quadrant.
    if smoothing_layer is None:
        if mid_x > 1 or mid_y > 1:
            layer[:mid_x + 1, :mid_y + 1] = ds_process(layer[:mid_x + 1, :mid_y + 1], next_iteration)
            layer[mid_x:, :mid_y + 1] = ds_process(layer[mid_x:, :mid_y + 1], next_iteration)
            layer[:mid_x + 1, mid_y:] = ds_process(layer[:mid_x + 1, mid_y:], next_iteration)
            layer[mid_x:, mid_y:] = ds_process(layer[mid_x:, mid_y:], next_iteration)
    else:
        if mid_x > 1 or mid_y > 1:
            layer[:mid_x + 1, :mid_y + 1] = ds_process(layer[:mid_x + 1, :mid_y + 1],
                                                       next_iteration,
                                                       smoothing_layer=smoothing_layer[:mid_x + 1, :mid_y + 1])
            layer[mid_x:, :mid_y + 1] = ds_process(layer[mid_x:, :mid_y + 1],
                                                   next_iteration,
                                                   smoothing_layer=smoothing_layer[mid_x:, :mid_y + 1])
            layer[:mid_x + 1, mid_y:] = ds_process(layer[:mid_x + 1, mid_y:],
                                                   next_iteration,
                                                   smoothing_layer=smoothing_layer[:mid_x + 1, mid_y:])
            layer[mid_x:, mid_y:] = ds_process(layer[mid_x:, mid_y:],
                                               next_iteration,
                                               smoothing_layer=smoothing_layer[mid_x:, mid_y:])
    return layer


def diamond(layer, iteration, smoothing_layer=None):
    """Set the center of layer to the average of the four corners, plus random noise.
    """
    mid_x = midpoint(layer.shape[0])
    mid_y = midpoint(layer.shape[1])

    if layer[mid_x, mid_y] == 0:
        corner_a = layer[0, 0]
        corner_b = layer[0, -1]
        corner_c = layer[-1, 0]
        corner_d = layer[-1, 0]
        values = (corner_a, corner_b, corner_c, corner_d)
        if smoothing_layer is None:
            value = get_value(values, iteration)
        else:
            smoothness = smoothing_layer[mid_x, mid_y]
            value = get_value(values, iteration, smoothness)
        layer[mid_x, mid_y] = value


def square(layer, iteration, smoothing_layer=None):
    """
    Perform the square step of the Diamond-Square algorithm. Assign the results
    @param layer:
    @param iteration:
    @param smoothing_layer:
    """
    mid_x = midpoint(layer.shape[0])
    mid_y = midpoint(layer.shape[1])
    #Amusing bugs, may re-implement later as an option
    #layer[mid_x, 0] = get_value([layer[0, 0], layer[-1, 0]], iteration)
    #layer[0, mid_y] = get_value([layer[0, 0], layer[0, -1]], iteration)
    layer_ne = layer[-1, -1]
    layer_se = layer[-1, 0]
    layer_nw = layer[0, -1]
    if smoothing_layer is None:
        if layer[mid_x, -1] == 0:
            layer[mid_x, -1] = get_value([layer_nw, layer_ne], iteration)
        if layer[-1, mid_y] == 0:
            layer[-1, mid_y] = get_value([layer_se, layer_ne], iteration)
    else:
        if layer[mid_x, -1] == 0:
            smoothness = smoothing_layer[mid_x, -1]
            layer[mid_x, -1] = get_value([layer_nw, layer_ne], iteration, smoothness)
        if layer[-1, mid_y] == 0:
            smoothness = smoothing_layer[-1, mid_y]
            layer[-1, mid_y] = get_value([layer_se, layer_ne], iteration, smoothness)


def midpoint(length):
    """Return an integer midpoint of a given length.
    @param length: integer
    @return: integer
    """
    if length > 2:
        return int(length * 0.5)
    return 1


def get_value(values=1, iteration=1, smoothing=1):
    """Return a float of random noise plus average of values.
    @rtype : float
    """
    if isinstance(values, int):
        value = values
    else:
        value = float(sum(values)) / float(len(values))
    variance = 5 * smoothing
    noise = random.uniform(-1.0, 1.0) * variance / float(iteration)
    return value + noise