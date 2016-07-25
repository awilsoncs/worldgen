import math

import numpy as np
import numpy

from worldgen.config import get_config
from worldgen.scaling import normalize


def process(world_map):
    """

    @rtype : recarray
    """
    print("Building Climate...")
    depth = float(get_config()['Parameters']['depth'])
    set_oceans(world_map, depth)
    set_temperature(world_map)
    set_precipitation(world_map)
    normalize(world_map['precipitation'])
    return world_map


def set_oceans(world_map, depth):
    print("- Processing oceans")
    for (x, y), z in np.ndenumerate(world_map):
        if world_map['elevation'][x, y] <= depth:
            world_map['water depth'][x, y] = 1.0
        else:
            world_map['water depth'][x, y] = 0.0


def set_temperature(world_map):
    print("- Processing temperature")
    temperature_map = world_map['temperature']
    size_y = world_map.shape[1]

    for (x, y), z in np.ndenumerate(temperature_map):
        latitude = y / size_y
        temperature_map[x, y] = math.e ** (-5 * (latitude ** 2))
    world_map['temperature'] = numpy.fliplr(temperature_map)


def set_precipitation(world_map):
    print("- Processing precipitation")
    precipitation_map = world_map['precipitation']
    shape = precipitation_map.shape
    world_map['precipitation'] = numpy.random.rand(shape[0], shape[1])
