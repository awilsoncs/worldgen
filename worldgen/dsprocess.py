import random

import numpy as np

import scaling
import worldmaps

SOUTH_WEST = [0, 0]
NORTH_WEST = [0, -1]
SOUTH_EAST = [-1, 0]
NORTH_EAST = [-1, -1]


def process(world_map):
    """
    Construct the world map.

    @rtype : recarray
    @type world_map: recarray
    """

    print "Building Geology..."
    smoothness = world_map['smoothness']
    ds_process(smoothness)
    scaling.scale(smoothness)
    print "-Processing smoothness"
    seed_corners(world_map)
    sew_seams(world_map)
    for key in worldmaps.ds_generated:
        print "-Processing %s" % key
        layer = world_map[key]
        ds_process(layer, smoothing_layer=world_map['smoothness'])
        scaling.scale(layer)
    return world_map


def seed_corners(world_map):
    """Get values for the corners of the wm array."""

    print "-Seeding corners..."

    #Only get the western corners, we're going to seed the eastern ones from these.
    world_map[0, 0] = stack_value(world_map[0, 0])
    world_map[0, -1] = stack_value(world_map[0, -1])


def sew_seams(world_map):
    """Insert values into the edges of the map to create continuous lines."""

    print "-Sewing seams..."

    ## Vertical seams
    world_map[0, ] = sew_vertical(world_map[0])
    world_map[-1, ] = world_map[0, ]

    ## Horizontal seams
    world_map[:, 0] = world_map[0, 0]
    world_map[:, -1] = world_map[0, -1]


# @TODO Vertical seam is noticeable in final map. It should not be.
def sew_vertical(seam, iteration=1):
    """

    @type seam:
    @param seam:
    @param iteration:
    @return:
    """
    mid_y = midpoint(seam.shape[0])
    #seam[mid_y] = stack_value(seam[mid_y], [seam[0], seam[-1]], iteration)
    for key in worldmaps.ds_generated:
        seam[mid_y][key] = get_value_from_list([seam[0][key], seam[-1][key]], iteration)
    if mid_y > 1:
        seam[:mid_y + 1] = sew_vertical(seam[:mid_y + 1], iteration + 1)
        seam[mid_y:] = sew_vertical(seam[mid_y:], iteration + 1)
    return seam


def stack_value(stack, values=None, iteration=1, smoothing=1):
    """

    @param stack:
    @param values:
    @param iteration:
    @param smoothing:
    @return:
    """
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
    """


    @rtype : ndarray
    @param layer:
    @param iteration:
    @param smoothing_layer:
    @return:
    """

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
            smoothing_sw = smoothing_layer[:mid_x + 1, :mid_y + 1]
            smoothing_nw = smoothing_layer[mid_x:, :mid_y + 1]
            smoothing_se = smoothing_layer[:mid_x + 1, mid_y:]
            smoothing_ne = smoothing_layer[mid_x:, mid_y:]

            layer[:mid_x + 1, :mid_y + 1] = ds_process(layer[:mid_x + 1, :mid_y + 1], next_iteration, smoothing_sw)
            layer[mid_x:, :mid_y + 1] = ds_process(layer[mid_x:, :mid_y + 1], next_iteration, smoothing_nw)
            layer[:mid_x + 1, mid_y:] = ds_process(layer[:mid_x + 1, mid_y:], next_iteration, smoothing_se)
            layer[mid_x:, mid_y:] = ds_process(layer[mid_x:, mid_y:], next_iteration, smoothing_ne)

    return layer


def diamond(layer, iteration, smoothing_layer=None):
    """

    @param layer:
    @param iteration:
    @param smoothing_layer:
    """

    mid_x = midpoint(layer.shape[0])
    mid_y = midpoint(layer.shape[1])

    if layer[mid_x, mid_y] == 0:
        corner_a = layer[0, 0]
        corner_b = layer[0, -1]
        corner_c = layer[-1, 0]
        corner_d = layer[-1, 0]
        values = [corner_a, corner_b, corner_c, corner_d]
        if smoothing_layer is None:
            value = get_value_from_list(values=values, iteration=iteration)
        else:
            smoothness = smoothing_layer[mid_x, mid_y]
            value = get_value_from_list(values=values, iteration=iteration, smoothing=smoothness)
        layer[mid_x, mid_y] = value


def square(layer, iteration, smoothing_layer=None):
    """
    Perform the Square step of the Diamond-Square algorithm on layer.
    @type  layer: recarray
    @param layer: a single record of a world map
    @type  iteration: integer
    @param iteration: the iteration of the Diamond Square algorithm
    @type  smoothing_layer: recarray
    @param smoothing_layer:
    """

    mid_x = midpoint(layer.shape[0])
    mid_y = midpoint(layer.shape[1])
    layer_ne = layer[-1, -1]
    layer_se = layer[-1, 0]
    layer_nw = layer[0, -1]
    if smoothing_layer is None:
        if layer[mid_x, -1] == 0:
            layer[mid_x, -1] = get_value_from_list([layer_nw, layer_ne], iteration)
        if layer[-1, mid_y] == 0:
            layer[-1, mid_y] = get_value_from_list([layer_se, layer_ne], iteration)
    else:
        if layer[mid_x, -1] == 0:
            smoothness = smoothing_layer[mid_x, -1]
            layer[mid_x, -1] = get_value_from_list([layer_nw, layer_ne], iteration, smoothness)
        if layer[-1, mid_y] == 0:
            smoothness = smoothing_layer[-1, mid_y]
            layer[-1, mid_y] = get_value_from_list([layer_se, layer_ne], iteration, smoothness)


def midpoint(length):
    """Return an integer midpoint of a given length.
    @rtype : int
    @param length: integer
    @return: integer
    """

    return int(length * 0.5)


def get_value_from_list(values=[], iteration=1, smoothing=1.0):
    """
    @rtype : float
    @param values: list
    @param iteration:
    @param smoothing:
    @return:
    """
    value = float(sum(values)) / float(len(values))
    return get_value(value=value, iteration=iteration, smoothing=smoothing)


def get_value(value=1.0, iteration=1, smoothing=1.0):
    """Return a float of random noise plus average of values.
    @type value: float
    @type iteration: int
    @type smoothing: float
    @param value:
    @param iteration:
    @param smoothing:
    @rtype : float
    """

    noise = random.uniform(-1.0, 1.0) * smoothing / float(iteration)
    return value + noise