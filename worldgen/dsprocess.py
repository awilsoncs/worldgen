from copy import copy
import math
import random
import config
import numpy as np

import scaling


def process(worldmap):
    """Populate and return a Worldmap with values."""
    seed_corners(worldmap)
    sew_seams(worldmap)
    step(worldmap)
    scaling.scale(worldmap, worldmap.ds_generated)
    return worldmap


def step(worldmap):
    """Perform the diamond-square algorithm."""
    print "Beginning map..."
    print "This may take a while"

    for coords in midpoint_iter(worldmap):
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

    if worldmap[x, y] is None or worldmap[x, y].locked is False:
        for key in worldmap.ds_generated:
            corner_a = worldmap.get((coords[0], coords[2]), key)
            corner_b = worldmap.get((coords[0], coords[3]), key)
            corner_c = worldmap.get((coords[1], coords[2]), key)
            corner_d = worldmap.get((coords[1], coords[3]), key)
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


def get_value(values=1, iteration=1, smoothing=1):
    """Return a float of random noise plus average of values.
    @rtype : float
    """
    if isinstance(values, int):
        value = values
    else:
        value = float(sum(values)) / float(len(values))
    variance = smoothing * 5.0
    value += random.uniform(-variance, variance) / float(iteration)
    return value


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

    worldmap.lock((0, 0))
    worldmap.lock((0, -1))
    worldmap.lock((-1, 0))
    worldmap.lock((-1, -1))


def sew_seams(worldmap):
    """Insert values into the edges of the map to create continuous lines."""
    print "Sewing seams..."

    ## Vertical seams
    height = worldmap.shape[1]
    iteration = 1
    while height > 1:
        box = (1, height-1)
        for (x, y), _ in wmiter(worldmap, (0, 1), (0, -2), box):
            if config.verbose:
                print "Sewing y: %d" % y
            coords = (0, 0, y, y + box[1])
            diamond(worldmap, coords, iteration)
            worldmap[-1, y] = copy(worldmap[0, y])
        iteration += 1
        height = int(math.ceil(height / 2.0))

    ## Horizontal seams
    north_loc = worldmap[0, 0]
    south_loc = worldmap[0, -1]
    for x in xrange(worldmap.shape[0]):
        worldmap[x, 0] = copy(north_loc)
        worldmap[x, -1] = copy(south_loc)


def midpoint_iter(world_map, x_range=(0, -1), y_range=(0, -1), iteration=1):
    x_min = x_range[0]
    x_max = x_range[1]
    y_min = y_range[0]
    y_max = y_range[1]

    if x_max < 0:
        x_max = world_map.shape[0] + x_max
    if y_max < 0:
        y_max = world_map.shape[1] + y_max
    if x_min < x_max - 1 or y_min < y_max - 1:
        yield (x_min, x_max, y_min, y_max, iteration)
        for output in midpoint_iter(
                world_map,
                x_range=(x_min, (x_max + x_min) / 2),
                y_range=(y_min, (y_max + y_min) / 2),
                iteration=iteration + 1):
            yield output
        for output in midpoint_iter(
                world_map,
                x_range=((x_min + x_max) / 2, x_max),
                y_range=(y_min, (y_max + y_min) / 2),
                iteration=iteration + 1):
            yield output
        for output in midpoint_iter(
                world_map,
                x_range=(x_min, (x_max + x_min) / 2),
                y_range=((y_min + y_max) / 2, y_max),
                iteration=iteration + 1):
            yield output
        for output in midpoint_iter(
                world_map,
                x_range=((x_min + x_max) / 2, x_max),
                y_range=((y_min + y_max) / 2, y_max),
                iteration=iteration + 1):
            yield output


def wmiter(world_map, x_range=(0, -1), y_range=(0, -1), step=(1, 1)):
        """Improves upon ndenumerate by iterating through a slice of the
        array, and taking steps.
        """
        if config.verbose:
            print "Call to wmiter"
        x_min = x_range[0]
        x_max = x_range[1]
        y_min = y_range[0]
        y_max = y_range[1]
        x_step = step[0]
        y_step = step[1]

        if x_max < 0:
            x_max = world_map.shape[0] + x_max + 1
        if y_max < 0:
            y_max = world_map.shape[1] + y_max + 1

        for (x, y), loc in np.ndenumerate(world_map[x_min:x_max, y_min:y_max]):
            if config.verbose:
                print "wmiter: loc found at x: %d y: %d" % (x, y)
            if (x % x_step == 0) and (y % y_step == 0):
                if config.verbose:
                    print "Yielding x: %d y: %d" % (x, y)
                yield (x, y), loc