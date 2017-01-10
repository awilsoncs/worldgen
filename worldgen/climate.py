import math

import numpy as np

from worldgen.scaling import normalize


def process(world_map, sea_level):
    """Build climate features.

    @rtype : recarray
    """
    print("Building Climate...")
    set_oceans(world_map, sea_level)
    set_temperature(world_map, sea_level)
    set_precipitation(world_map)
    normalize(world_map['precipitation'])
    normalize(world_map['temperature'])
    return world_map


# def smooth_coastlines(world_map):
#     ocean_map = world_map['water depth']
#     elevation_map = world_map['elevation']
#     padded_ocean_map =
#     for (x, y), z in np.ndenumerate(elevation_map):
#         ocean_neighbors =


def set_oceans(world_map, sea_level):
    """Set the ocean map to 0.0 if ocean is present, 1.0 otherwise.

    :param world_map:
    :param depth:
    :return:
    """
    print("- Processing oceans")
    for (x, y), z in np.ndenumerate(world_map):
        if world_map['elevation'][x, y] <= sea_level:
            world_map['water depth'][x, y] = 0.0
        else:
            world_map['water depth'][x, y] = 1.0


def set_temperature(world_map, sea_level):
    """Set temperature based on elevation and latitude.

    :param world_map:
    :return:
    """
    print("- Processing temperature")
    temperature_map = world_map['temperature']
    elevation_map = world_map['elevation']
    size_y = world_map.shape[1]

    for (x, y), z in np.ndenumerate(temperature_map):
        latitude = y / size_y
        elevation = elevation_map[x, y]

        value = math.e ** (-5 * (latitude ** 2))
        temperature_map[x, y] = value * get_temperature(elevation, sea_level)


def get_temperature(elevation, sea_level):
    """Get a temperature adjustment based on elevation. Temperatures over oceans are 80% of normal, for visual reasons.

    :param elevation:
    :param sea_level:
    :return:
    """
    if elevation <= sea_level:
        return 0.8
    else:
        return (-1.0 / (1.0 - sea_level)) * (elevation - sea_level) + 1.0


def set_precipitation(world_map):
    """Set precipitation of the world map, based on the latitude ocean / land ratio and temperature.

    :param world_map:
    :return:
    """
    print("- Processing precipitation")
    ocean_map = world_map['water depth']
    precipitation_map = world_map['precipitation']
    temperature_map = world_map['temperature']

    for (x, y), temp in np.ndenumerate(temperature_map):
        ocean_ratio = 1 - np.average(ocean_map[:, y])
        precipitation_map[x, y] = ocean_ratio * temp * 0.5
        if ocean_map[x, y] == 0.0:
            precipitation_map[x, y] *= 0.5
