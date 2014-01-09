import math
import numpy as np

from config import Config


def build_climate(world_map):
    set_oceans(world_map, 0.6)

    # Southern westerlies
    start_at = int(world_map.shape[1] * 2.0 / 3.0)
    stop_at = world_map.shape[1]
    draw_wind(world_map, start_at, stop_at, 2)

    # Northern westerlies
    start_at = int(world_map.shape[1] * 1.0 / 3.0)
    stop_at = -1
    draw_wind(world_map, start_at, stop_at, 2)

    # Southern trades
    start_at = int(world_map.shape[1] * 2.0 / 3.0)
    stop_at = world_map.shape[1] / 2 - 1
    draw_wind(world_map, start_at, stop_at, -2)

    # Northern trades
    start_at = int(world_map.shape[1] * 1.0 / 3.0)
    stop_at = world_map.shape[1] / 2 + 2
    draw_wind(world_map, start_at, stop_at, -2)


def set_oceans(world_map, depth):
    print "Filling oceans..."
    for (_, _), location in np.ndenumerate(world_map):
        if location['elevation'] <= depth:
            location['ocean'] = 1.0
        else:
            location['ocean'] = 0.0


def draw_wind(world_map, start_at, stop_at, direction):
    step = 1
    if start_at > stop_at:
        step = -1
    moisture_array = np.zeros((world_map.shape[0], 1))
    config_file = Config('config.txt')
    winds = int(config_file['winds'])

    for y in range(start_at, stop_at, step):
        for (x, y2), cell in np.ndenumerate(moisture_array):
            if world_map[x, y]['ocean']:
                moisture = float(config_file['moisture_pickup'])
                moisture_array[x, y2] += moisture
                world_map[x, y]['precipitation'] = 0.0
            else:
                elevation = world_map[x, y]['elevation']
                moisture = float(config_file['moisture_drop'])
                precipitation = moisture_array[x, y2] * (elevation - moisture)
                moisture_array[x, y2] -= precipitation
                world_map[x, y]['precipitation'] = precipitation
        distance = abs(start_at - stop_at)
        current = abs(y - start_at)
        #As we get further into the trade wind's "territory", they push further.
        shift = int(math.sin(current / float(distance)) * winds * direction)
        moisture_array = np.roll(moisture_array, shift*5)