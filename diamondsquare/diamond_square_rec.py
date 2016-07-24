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


def diamond(array, iteration, smoothing_layer=None, variance=1.0):
    """Perform the Diamond step of the Diamond-Square algorithm on layer."""

    mid_x = midpoint(array.shape[0])
    mid_y = midpoint(array.shape[1])

    if array[mid_x, mid_y] == 0:
        corner_a = array[0, 0]
        corner_b = array[0, -1]
        corner_c = array[-1, 0]
        corner_d = array[-1, -1]
        values = [corner_a, corner_b, corner_c, corner_d]

        smoothness = smoothing_layer[mid_x, mid_y]
        value = get_height_value(values=values, iteration=iteration, smoothing=smoothness, variance=variance)
        array[mid_x, mid_y] = value


def square(array, iteration, smoothing_array=None, variance=1.0):
    """Perform the Square step of the Diamond-Square algorithm on layer."""

    mid_x = midpoint(array.shape[0])
    mid_y = midpoint(array.shape[1])
    array_ne = array[0, -1]
    array_se = array[-1, -1]
    array_nw = array[0, 0]
    array_sw = array[-1, 0]

    smoothness_e = smoothing_array[mid_x, -1]
    array[mid_x, -1] = get_height_value([array_se, array_ne], iteration, smoothness_e, variance=variance)

    smoothness_s = smoothing_array[-1, mid_y]
    array[-1, mid_y] = get_height_value([array_se, array_sw], iteration, smoothness_s, variance=variance)

    smoothness_n = smoothing_array[0, mid_y]
    array[0, mid_y] = get_height_value([array_nw, array_ne], iteration, smoothness_n, variance=variance)

    smoothness_w = smoothing_array[mid_x, 0]
    array[mid_x, 0] = get_height_value([array_sw, array_nw], iteration, smoothness_w, variance=variance)


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


def normalize(array):
    """Scale all values in the array to 0.0-1.0 floats."""
    high = array.max()
    low = array.min()
    rng = high - low
    array[:] = 1.0 - ((high - array) / rng)


def array_to_csv(array, path):
    """Save a single layer as a CSV file."""
    file_path = path + ".csv"
    try:
        numpy.savetxt(file_path, array, delimiter=",", fmt="%s")
    except PermissionError:
        print("Error saving file: {0}".format(file_path))
        print("Check to make sure you do not have the file open in another program.")


def plot(array, x, y):
    try:
        import matplotlib.pyplot as plt
        fig, ax = plt.subplots()
        heatmap = ax.pcolor(array, cmap=plt.cm.Blues)
        ax.invert_yaxis()
        ax.xaxis.tick_top()
        plt.show()

    except Exception as ex:
        print("Could not plot: {0}".format(ex))
        print("You may need to install seaborn.")


def main():
    parser = argparse.ArgumentParser(description="Create 2D noise arrays.")
    parser.add_argument('-d', '--destination', type=str, default='default.csv', help='output destination')
    parser.add_argument('-n', '--normalize', action='store_true', help='normalize to 0.5 mean and 1 range')
    parser.add_argument('-o', '--output', action='store_true', help='print the result to stdout')
    parser.add_argument('-p', '--plot', action='store_true', help='render a plot of the array')
    parser.add_argument('-r', '--random', type=int, default=None, help='random seed')
    parser.add_argument('-s', '--smoothing', action='store_true', help='use a special smoothing array')
    parser.add_argument('-v', '--variance', type=float, default=1.0, help='variance of the array')
    parser.add_argument('height', type=int, help='height of the array')
    parser.add_argument('width', type=int, help='width of the array')
    args = parser.parse_args()

    if args.random:
        setup(args.random)

    size = (args.height, args.width)

    smoothing = numpy.ones(size)
    array = numpy.zeros(size)
    if args.smoothing:
        smoothing = numpy.zeros(size)
        seed_corners(smoothing)
        diamond_square(smoothing, variance=args.variance)
    seed_corners(array)
    diamond_square(array, smoothing_array=smoothing, variance=args.variance)

    if args.normalize:
        normalize(array)

    if args.output:
        print(array)

    if args.plot:
        plot(array, size[1], size[0])


if __name__ == '__main__':
    sys.exit(main())
