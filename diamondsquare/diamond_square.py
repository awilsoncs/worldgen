import argparse
import random
import sys

import numpy


def setup(seed):
    random.seed(seed)


def diamond_square(array, iteration=1, smoothing_array=None, variance=1.0):
    """
    Assign a randomized height map to an array, with values 0.0-1.0.

    @type array: ndarray
    @type iteration: int
    @type smoothing_array: ndarray
    @type variance: float
    @rtype : ndarray

    @param array:
    @param iteration:
    @param smoothing_array:
    @param variance:
    @return:
    """

    mid_x = midpoint(array.shape[0])
    mid_y = midpoint(array.shape[1])

    square(array, iteration, smoothing_array, variance=variance)
    diamond(array, iteration, smoothing_array, variance=variance)

    next_iteration = iteration + 1

    # Recursion on each quadrant.
    if smoothing_array is None:
        if mid_x > 1 or mid_y > 1:
            array[:mid_x + 1, :mid_y + 1] = diamond_square(array[:mid_x + 1, :mid_y + 1], next_iteration)
            array[mid_x:, :mid_y + 1] = diamond_square(array[mid_x:, :mid_y + 1], next_iteration)
            array[:mid_x + 1, mid_y:] = diamond_square(array[:mid_x + 1, mid_y:], next_iteration)
            array[mid_x:, mid_y:] = diamond_square(array[mid_x:, mid_y:], next_iteration)
    else:
        if mid_x > 1 or mid_y > 1:
            smoothing_sw = smoothing_array[:mid_x + 1, :mid_y + 1]
            smoothing_nw = smoothing_array[mid_x:, :mid_y + 1]
            smoothing_se = smoothing_array[:mid_x + 1, mid_y:]
            smoothing_ne = smoothing_array[mid_x:, mid_y:]

            array[:mid_x + 1, :mid_y + 1] = diamond_square(array[:mid_x + 1, :mid_y + 1], next_iteration, smoothing_sw)
            array[mid_x:, :mid_y + 1] = diamond_square(array[mid_x:, :mid_y + 1], next_iteration, smoothing_nw)
            array[:mid_x + 1, mid_y:] = diamond_square(array[:mid_x + 1, mid_y:], next_iteration, smoothing_se)
            array[mid_x:, mid_y:] = diamond_square(array[mid_x:, mid_y:], next_iteration, smoothing_ne)

    return array


def seed_corners(array):
    """Set values to the corners of the array."""

    # Only get the western corners, we're going to seed the eastern ones from these.
    for i in [0, -1]:
        for j in [0, -1]:
            array[i, j] = get_height_value()


def diamond(layer, iteration, smoothing_layer=None, variance=1.0):
    """Perform the Diamond step of the Diamond-Square algorithm on layer."""

    mid_x = midpoint(layer.shape[0])
    mid_y = midpoint(layer.shape[1])

    if layer[mid_x, mid_y] == 0:
        corner_a = layer[0, 0]
        corner_b = layer[0, -1]
        corner_c = layer[-1, 0]
        corner_d = layer[-1, -1]
        values = [corner_a, corner_b, corner_c, corner_d]
        if smoothing_layer is None:
            value = get_height_value(values=values, iteration=iteration, variance=variance)
        else:
            smoothness = smoothing_layer[mid_x, mid_y]
            value = get_height_value(values=values,
                                     iteration=iteration,
                                     smoothing=smoothness,
                                     variance=variance)
        layer[mid_x, mid_y] = value


def square(layer, iteration, smoothing_layer=None, variance=1.0):
    """Perform the Square step of the Diamond-Square algorithm on layer."""

    mid_x = midpoint(layer.shape[0])
    mid_y = midpoint(layer.shape[1])
    layer_ne = layer[-1, -1]
    layer_se = layer[-1, 0]
    layer_nw = layer[0, -1]
    if smoothing_layer is None:
        if layer[mid_x, -1] == 0:
            layer[mid_x, -1] = get_height_value([layer_nw, layer_ne],
                                                iteration,
                                                variance=variance)
        if layer[-1, mid_y] == 0:
            layer[-1, mid_y] = get_height_value([layer_se, layer_ne],
                                                iteration,
                                                variance=variance)
    else:
        if layer[mid_x, -1] == 0:
            smoothness = smoothing_layer[mid_x, -1]
            layer[mid_x, -1] = get_height_value([layer_nw, layer_ne],
                                                iteration,
                                                smoothness,
                                                variance=variance)
        if layer[-1, mid_y] == 0:
            smoothness = smoothing_layer[-1, mid_y]
            layer[-1, mid_y] = get_height_value([layer_se, layer_ne],
                                                iteration,
                                                smoothness,
                                                variance=variance)


def midpoint(length):
    """Return an integer midpoint of a given length.
    @rtype : int
    @param length: integer
    @return: integer
    """

    return int(length * 0.5)


def get_height_value(values=None, iteration=1, smoothing=1.0, variance=1.0):
    """Average values, then adjust it based on random noise.
    @type values: list
    @param iteration:
    @param smoothing:
    @param variance:
    @rtype : float
    @return:
    """
    noise = random.uniform(-1.0, 1.0) * variance * smoothing / float(iteration)
    if not values:
        return noise
    value = float(sum(values)) / float(len(values))
    return value + noise


def array_to_csv(array, path):
    """Save a single layer as a CSV file."""
    file_path = path + ".csv"
    try:
        numpy.savetxt(file_path, array, delimiter=",", fmt="%s")
    except PermissionError:
        print("Error saving file: {0}".format(file_path))
        print("Check to make sure you do not have the file open in another program.")


def plot(array):
    pass


def main():
    parser = argparse.ArgumentParser(description="Create 2D noise arrays.")
    parser.add_argument('-d', '--destination', type=str, default='default.csv', help='output destination')
    parser.add_argument('-p', '--plot', action='store_true', help='render a plot of the array')
    parser.add_argument('-r', '--random', type=int, default=None, help='random seed')
    parser.add_argument('-s', '--smoothing', action='store_true', help='use a special smoothing array')
    parser.add_argument('-v', '--variance', type=float, default=1.0, help='variance of the array')
    parser.add_argument('height', type=int, help='height of the array')
    parser.add_argument('width', type=int, help='width of the array')
    args = parser.parse_args()


if __name__ == '__main__':
    sys.exit(main())
