import worldgen.scaling as scaling
import worldgen.world_maps as world_maps
from diamondsquare.diamond_square import get_height_map


def process(world_map, scale=8, height=250, width=250, variance=1.0, seed=None):
    """
    Construct the world map.

    @type world_map: recarray
    @rtype : recarray
    :param world_map:
    :param seed: 
    """

    print("Building Geology...")
    print("- Processing smoothness")
    smoothing_array = get_height_map(scale=scale,
                                     height=2 ** scale + 1,
                                     width=2 ** scale + 1,
                                     variance=variance,
                                     seed=seed)

    for key in world_maps.geology:
        print('- Processing {0}'.format(key))
        world_map[key] = get_height_map(scale=scale,
                                        height=height,
                                        width=width,
                                        smooth_map=smoothing_array,
                                        variance=variance)

    world_map['elevation'] = scaling.elevation(world_map['elevation'])
    return world_map
