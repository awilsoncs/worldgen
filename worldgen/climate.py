import math

import numpy as np

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
    normalize(world_map['temperature'])
    return world_map


def set_oceans(world_map, depth):
    print("- Processing oceans")
    for (x, y), z in np.ndenumerate(world_map):
        if world_map['elevation'][x, y] <= depth:
            world_map['water depth'][x, y] = 0.0
        else:
            world_map['water depth'][x, y] = 1.0


def set_temperature(world_map):
    print("- Processing temperature")
    temperature_map = world_map['temperature']
    elevation_map = world_map['elevation']
    size_y = world_map.shape[1]
    sea_level = float(get_config()['Parameters']['depth'])

    for (x, y), z in np.ndenumerate(temperature_map):
        latitude = y / size_y
        elevation = elevation_map[x, y]

        value = math.e ** (-5 * (latitude ** 2))
        temperature_map[x, y] = value * get_temperature(elevation, sea_level)


def get_temperature(elevation, sea_level):
    if elevation <= sea_level:
        return 0.8
    else:
        return (-1.0 / (1.0 - sea_level)) * (elevation - sea_level) + 1.0


def set_precipitation(world_map):
    print("- Processing precipitation")
    ocean_map = world_map['water depth']
    precipitation_map = world_map['precipitation']
    temperature_map = world_map['temperature']

    for (x, y), temp in np.ndenumerate(temperature_map):
        ocean_ratio = 1 - np.average(ocean_map[:, y])
        precipitation_map[x, y] = ocean_ratio * temp * 0.5
        if ocean_map[x, y] == 0.0:
            precipitation_map[x, y] *= 0.5
