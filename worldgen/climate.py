import math

import numpy as np

from worldgen.config import get_config


# def process(world_map):
#     """
#
#     @rtype : recarray
#     """
#     print("Building Climates...")
#     elevation = world_map['elevation']
#     lowest_trench = np.unravel_index(elevation.argmin(), elevation.shape)
#     world_map = flood_fill(lowest_trench[0], lowest_trench[1], world_map, 0.6)
#     trade_winds(world_map)
#     return world_map


def trade_winds(world_map):

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


# def set_oceans(world_map, depth):
#     print("Filling oceans...")
#     for (_, _), location in np.ndenumerate(world_map):
#         if location['elevation'] <= depth:
#             location['water depth'] = 1.0
#         else:
#             location['water depth'] = 0.0


def flood_fill(x, y, world_map, depth):
    print("-Filling oceans")
    queue = [(x, y)]
    while len(queue) > 0:
        node = queue.pop()
        node_x, node_y = node[0], node[1]
        node_x = (node_x + world_map.shape[0] - 1) % (world_map.shape[0] - 1)
        location = world_map[node_x, node_y]
        if location['elevation'] < depth and location['water depth'] == 0:
            world_map[node_x, node_y]['water depth'] = depth - location['elevation']
            queue.append((node_x + 1, node_y))
            queue.append((node_x - 1, node_y))
            if node_y < world_map.shape[1] - 1:
                queue.append((node_x, node_y + 1))
            if node_y > 0:
                queue.append((node_x, node_y - 1))
    return world_map


def draw_wind(world_map, start_at, stop_at, direction):
    step = 1
    if start_at > stop_at:
        step = -1
    moisture_array = np.zeros((world_map.shape[0], 1))
    config_file = get_config()
    winds = config_file.getint('Climate', 'winds')

    for y in range(start_at, stop_at, step):
        for (x, y2), cell in np.ndenumerate(moisture_array):
            if world_map[x, y]['water depth']:
                moisture = config_file.getfloat('Climate', 'moisture_pickup')
                moisture_array[x, y2] += moisture
                world_map[x, y]['precipitation'] = 0.0
            else:
                elevation = world_map[x, y]['elevation']
                moisture = config_file.getfloat('Climate', 'moisture_drop')
                precipitation = moisture_array[x, y2] * (elevation - moisture)
                moisture_array[x, y2] = max(moisture_array[x, y2] - precipitation, 0.0)
                world_map[x, y]['precipitation'] = precipitation
        distance = abs(start_at - stop_at)
        current = abs(y - start_at)
        # As we get further into the trade wind's "territory", they push further.
        shift = int(math.sin(current / float(distance)) * winds * direction)
        moisture_array = np.roll(moisture_array, shift*5)