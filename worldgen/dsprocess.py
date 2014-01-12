import random

import scaling
import worldmaps


def process(worldmap):
    """Populate and return a Worldmap with values."""
    smoothness = worldmap['smoothness']
    seed_corners(smoothness)
    sew_seams(smoothness)
    print "Processing smoothness"
    ds_process(smoothness)
    print "Scaling smoothness"
    scaling.scale(smoothness)
    for key in worldmaps.ds_generated:
        layer = worldmap[key]
        seed_corners(layer)
        sew_seams(layer)
        ds_process(layer)
        scaling.scale(layer)
    return worldmap


def seed_corners(layer):
    """Get values for the corners of the wm array."""
    print "Seeding corners..."
    value_a = get_value()
    value_b = get_value()

    layer[0, 0] += value_a
    layer[-1, 0] += value_a
    layer[-1, -1] += value_b
    layer[0, -1] += value_b


def sew_seams(layer):
    """Insert values into the edges of the map to create continuous lines."""
    print "Sewing seams..."

    ## Vertical seams
    layer[0, ] = sew_vertical(layer[0, ])
    layer[-1, ] = layer[0, ]

    ## Horizontal seams
    north_loc = layer[0, 0]
    south_loc = layer[0, -1]
    for x in xrange(layer.shape[0]):
        layer[x, 0] = north_loc
        layer[x, -1] = south_loc


def sew_vertical(seam, iteration=1):
    mid_y = midpoint(seam.shape[0])
    seam[mid_y] = get_value([seam[0], seam[-1]], iteration)
    if mid_y > 1:
        seam[:mid_y+1] = sew_vertical(seam[:mid_y+1], iteration+1)
        seam[mid_y:] = sew_vertical(seam[mid_y:], iteration+1)
    return seam


def ds_process(layer, iteration=1, smoothing_layer=None):
    mid_x = midpoint(layer.shape[0])
    mid_y = midpoint(layer.shape[1])

    diamond(layer, iteration, smoothing_layer)
    square(layer, iteration, smoothing_layer)

    next_iter = iteration + 1
    if smoothing_layer is None:
        if mid_x > 1 or mid_y > 1:
            layer[:mid_x+1, :mid_y+1] = ds_process(layer[:mid_x+1, :mid_y+1], next_iter)
            layer[mid_x:, :mid_y+1] = ds_process(layer[mid_x:, :mid_y+1], next_iter)
            layer[:mid_x+1, mid_y:] = ds_process(layer[:mid_x+1, mid_y:], next_iter)
            layer[mid_x:, mid_y:] = ds_process(layer[mid_x:, mid_y:], next_iter)
    return layer


def diamond(layer, iteration, smoothing_layer=None):
    """Set the center of coords to the average of the four corners, plus
    random noise.   
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
    #Edges of the layer

    mid_x = midpoint(layer.shape[0])
    mid_y = midpoint(layer.shape[1])

    #layer[mid_x, 0] = get_value([layer[0, 0], layer[-1, 0]], iteration)
    layer[mid_x, -1] = get_value([layer[0, -1], layer[-1, -1]], iteration)
    #layer[0, mid_y] = get_value([layer[0, 0], layer[0, -1]], iteration)
    layer[-1, mid_y] = get_value([layer[-1, 0], layer[-1, -1]], iteration)


def midpoint(length):
    """
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
    variance = smoothing * 5
    noise = random.uniform(-1.0, 1.0)*variance / float(iteration)
    return value + noise