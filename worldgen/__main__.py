import argparse
import sys
import time

import worldgen.climate as climate
import worldgen.geology as geology
import worldgen.saving as saving
import worldgen.world_maps as world_maps
from worldgen.config import get_config


def main():
    t = int(time.time())
    config_file = get_config()

    x = config_file.getint('Parameters', 'size_x')
    y = config_file.getint('Parameters', 'size_y')
    size = (x, y)
    world_map = world_maps.world_map(size)
    print("Random Seed: ", t)
    world_map = geology.process(world_map, seed=t)
    world_map = climate.process(world_map)
    print("Saving")
    saving.SaveHandler(world_map, 'test').world_to_csv()
    saving.SaveHandler(world_map, 'test').world_to_png()
    print("Map Hash: ", hash(str(world_map)))

    print("Ran in {0} seconds.".format(time.time() - t))


def add_args():
    parser = argparse.ArgumentParser("Generate world maps.")
    parser.add_argument("--seed", int, help="The random seed to be used")
    parser.add_argument('-v', '--verbose', action='store_true', help="Print more output during generation")
    return parser

if __name__ == '__main__':
    sys.exit(main())
