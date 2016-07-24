import errno
import os

import numpy


class SaveHandler:

    def __init__(self, world_map, path):
        self.world_map = world_map
        self.path = path
        _set_up_dir('worlds')
        _set_up_dir('worlds/' + path)

    def pickle(self):
        """Pickle the world map"""
        raise NotImplementedError

    def world(self):
        """Save the entire world map as a .world"""
        raise NotImplementedError

    def layer_to_csv(self, layer_name):
        """Save a single layer as a CSV file."""
        file_path = 'worlds' + "/" + self.path + "/" + layer_name + ".csv"
        try:
            layer = self.world_map[layer_name]
            numpy.savetxt(file_path, layer, delimiter=",", fmt="%s")
        except PermissionError:
            print("Error saving file: {0}".format(file_path))
            print("Check to make sure you do not have the file open in another program.")

    def world_to_csv(self):
        """Save the entire world map into a directory."""
        for key in self.world_map.dtype.names:
            self.layer_to_csv(key)

    def layer_to_bitmap(self):
        """Export a height map as a bitmap"""
        raise NotImplementedError


def _set_up_dir(path):
    try:
        os.makedirs(path)
    except OSError as exception:
        if exception.errno != errno.EEXIST:
            raise
