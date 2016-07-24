import worldgen.scaling as scaling
import worldgen.world_maps as world_maps
from diamondsquare.diamond_square import diamond_square
from diamondsquare.diamond_square import seed_corners
from worldgen.config import get_config


def process(world_map):
    """
    Construct the world map.

    @rtype : recarray
    @type world_map: recarray
    """

    print("Building Geology...")
    smoothness = world_map['smoothness']
    print("-Processing smoothness")
    config_file = get_config()
    variance = float(config_file['Parameters']['variance'])
    diamond_square(smoothness, size=variance, variance=variance)
    scaling.normalize(smoothness)
    for key in world_maps.ds_generated:
        print("-Processing ", key)
        layer = world_map[key]
        seed_corners(layer)
        diamond_square(layer, size=world_map['smoothness'], smoothing_array=world_map['smoothness'], variance=variance)
        scaling.normalize(layer)
    return world_map
