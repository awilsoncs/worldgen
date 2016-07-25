import sys
import time

import worldgen.climate as climate
import worldgen.geology as geology
import worldgen.saving as saving
import worldgen.world_maps as world_maps
from worldgen.config import get_config


def main():
    t = time.time()

    config_file = get_config()

    x = config_file.getint('Parameters', 'size_x')
    y = config_file.getint('Parameters', 'size_y')
    size = (x, y)
    world_map = world_maps.world_map(size)
    world_map = geology.process(world_map)
    world_map = climate.process(world_map)
    print("Saving")
    saving.SaveHandler(world_map, 'test').world_to_csv()
    saving.SaveHandler(world_map, 'test').world_to_png()

    print("Ran in {0} seconds.".format(time.time() - t))


if __name__ == '__main__':
    sys.exit(main())
