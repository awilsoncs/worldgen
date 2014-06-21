import random

import numpy as np

from config import config
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

    #TODO Should separate this and the algorithm functions to provide portability.
    # Should be a height map module and a world_map factory module.

    print "Building Geology..."
    smoothness = world_map['smoothness']
    print "-Processing smoothness"
    ds_height_map(smoothness)
    scaling.scale(smoothness)
    seed_corners(world_map)
    sew_seams(world_map)
    for key in worldmaps.ds_generated:
        print "-Processing %s" % key
        layer = world_map[key]
        ds_height_map(layer, smoothing_layer=world_map['smoothness'])
        scaling.scale(layer)
    return world_map


def seed_corners(world_map):
    """Set values to the corners of the world_map array."""

    print "-Seeding corners..."

    #Only get the western corners, we're going to seed the eastern ones from these.
    world_map[0, 0] = stack_value(world_map[0, 0])
    world_map[0, -1] = stack_value(world_map[0, -1])


def sew_seams(world_map):
    """Set values to the edges of the map to create continuous lines."""

    print "-Sewing seams..."

    ## Vertical seams
    world_map[0, ] = sew_vertical(world_map[0])
    world_map[-1, ] = world_map[0, ]

    ## Horizontal seams - top and bottom rows are all equal values
    world_map[:, 0] = world_map[0, 0]
    world_map[:, -1] = world_map[0, -1]


def sew_vertical(seam, iteration=1):
    """
    @type seam:
    @param seam:
    @param iteration:
    @return:
    """
    mid_y = _midpoint(seam.shape[0])
    smoothing = seam[mid_y]["smoothness"]
    for key in worldmaps.ds_generated:
        seam[mid_y][key] = _get_value_from_list([seam[0][key], seam[-1][key]], iteration, smoothing)
    if mid_y > 1:
        seam[:mid_y + 1] = sew_vertical(seam[:mid_y + 1], iteration + 1)
        seam[mid_y:] = sew_vertical(seam[mid_y:], iteration + 1)
    return seam


def stack_value(stack, values=None, iteration=1, smoothing=1.0):
    """
    @type stack: recarray
    @type values: recarray
    @type iteration: int
    @type smoothing: float
    """
    if values is None:
        values = np.ones(stack.size, dtype=[('smoothness', 'float16'),
                                            ('elevation', 'float16'),
                                            ('volcanism', 'float16'),
                                            ('solubility', 'float16'),
                                            ('minerals', 'float16')])
    variance = config.getfloat('Parameters', 'variance') * smoothing

    for key in worldmaps.ds_generated:
        noise = random.uniform(-1.0, 1.0) * variance / float(iteration)
        stack[key] = values[key] + noise
    return stack


def ds_height_map(layer, iteration=1, smoothing_layer=None):
    """
    Assign a randomized height map to layer, with values 0.0-1.0.

    @type layer: ndarray
    @type iteration: int
    @type smoothing_layer: ndarray
    @rtype : ndarray

    @param layer:
    @param iteration:
    @param smoothing_layer:
    @return:
    """

    mid_x = _midpoint(layer.shape[0])
    mid_y = _midpoint(layer.shape[1])

    _square(layer, iteration, smoothing_layer)
    _diamond(layer, iteration, smoothing_layer)

    next_iteration = iteration + 1

    #Recursion on each quadrant.
    if smoothing_layer is None:
        if mid_x > 1 or mid_y > 1:
            layer[:mid_x + 1, :mid_y + 1] = ds_height_map(layer[:mid_x + 1, :mid_y + 1], next_iteration)
            layer[mid_x:, :mid_y + 1] = ds_height_map(layer[mid_x:, :mid_y + 1], next_iteration)
            layer[:mid_x + 1, mid_y:] = ds_height_map(layer[:mid_x + 1, mid_y:], next_iteration)
            layer[mid_x:, mid_y:] = ds_height_map(layer[mid_x:, mid_y:], next_iteration)
    else:
        if mid_x > 1 or mid_y > 1:
            smoothing_sw = smoothing_layer[:mid_x + 1, :mid_y + 1]
            smoothing_nw = smoothing_layer[mid_x:, :mid_y + 1]
            smoothing_se = smoothing_layer[:mid_x + 1, mid_y:]
            smoothing_ne = smoothing_layer[mid_x:, mid_y:]

            layer[:mid_x + 1, :mid_y + 1] = ds_height_map(layer[:mid_x + 1, :mid_y + 1], next_iteration, smoothing_sw)
            layer[mid_x:, :mid_y + 1] = ds_height_map(layer[mid_x:, :mid_y + 1], next_iteration, smoothing_nw)
            layer[:mid_x + 1, mid_y:] = ds_height_map(layer[:mid_x + 1, mid_y:], next_iteration, smoothing_se)
            layer[mid_x:, mid_y:] = ds_height_map(layer[mid_x:, mid_y:], next_iteration, smoothing_ne)

    return layer


def _diamond(layer, iteration, smoothing_layer=None):
    """Perform the Diamond step of the Diamond-Square algorithm on layer."""

    mid_x = _midpoint(layer.shape[0])
    mid_y = _midpoint(layer.shape[1])

    if layer[mid_x, mid_y] == 0:
        corner_a = layer[0, 0]
        corner_b = layer[0, -1]
        corner_c = layer[-1, 0]
        corner_d = layer[-1, -1]
        values = [corner_a, corner_b, corner_c, corner_d]
        if smoothing_layer is None:
            value = _get_value_from_list(values=values, iteration=iteration)
        else:
            smoothness = smoothing_layer[mid_x, mid_y]
            value = _get_value_from_list(values=values, iteration=iteration, smoothing=smoothness)
        layer[mid_x, mid_y] = value


def _square(layer, iteration, smoothing_layer=None):
    """Perform the Square step of the Diamond-Square algorithm on layer."""

    mid_x = _midpoint(layer.shape[0])
    mid_y = _midpoint(layer.shape[1])
    layer_ne = layer[-1, -1]
    layer_se = layer[-1, 0]
    layer_nw = layer[0, -1]
    if smoothing_layer is None:
        if layer[mid_x, -1] == 0:
            layer[mid_x, -1] = _get_value_from_list([layer_nw, layer_ne], iteration)
        if layer[-1, mid_y] == 0:
            layer[-1, mid_y] = _get_value_from_list([layer_se, layer_ne], iteration)
    else:
        if layer[mid_x, -1] == 0:
            smoothness = smoothing_layer[mid_x, -1]
            layer[mid_x, -1] = _get_value_from_list([layer_nw, layer_ne], iteration, smoothness)
        if layer[-1, mid_y] == 0:
            smoothness = smoothing_layer[-1, mid_y]
            layer[-1, mid_y] = _get_value_from_list([layer_se, layer_ne], iteration, smoothness)


def _midpoint(length):
    """Return an integer midpoint of a given length.
    @rtype : int
    @param length: integer
    @return: integer
    """

    return int(length * 0.5)


def _get_value_from_list(values, iteration=1, smoothing=1.0):
    """
    @type values: list
    @param iteration:
    @param smoothing:
    @rtype : float
    @return:
    """
    value = float(sum(values)) / float(len(values))
    return _get_value(value=value, iteration=iteration, smoothing=smoothing)


def _get_value(value=1.0, iteration=1, smoothing=1.0):
    """Return a float of random noise plus average of values.
    @type value: float
    @type iteration: int
    @type smoothing: float
    @param value:
    @param iteration:
    @param smoothing:
    @rtype : float
    """

    variance = config.getfloat('Parameters', 'variance') * smoothing
    noise = random.uniform(-1.0, 1.0) * variance / float(iteration)
    return value + noise