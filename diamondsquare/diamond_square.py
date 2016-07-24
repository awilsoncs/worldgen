import argparse
import random
import sys

import numpy


def setup(seed):
    random.seed(seed)


def diamond_square(array, size, iteration=1, smoothing_array=None, variance=1.0):
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

    for n in range(size, 0, -1):
        print(n)
        working_block_size = 2 ** n + 1
        for x1 in range(0, 2 ** size, 2 ** n):
            for y1 in range(0, 2 ** size, 2 ** n):
                x2 = x1 + working_block_size - 1
                y2 = y1 + working_block_size - 1
                print('x1: {0} x2: {1} y1: {2} y2: {3}'.format(x1, x2, y1, y2))
                diamond(array, x1, y1, x2, y2, iteration=iteration, smoothing_array=smoothing_array, variance=variance)
                square(array, x1, y1, x2, y2, iteration=iteration, smoothing_array=smoothing_array, variance=variance)


def seed_corners(array):
    """Set values to the corners of the array."""

    # Only get the western corners, we're going to seed the eastern ones from these.
    for i in [0, -1]:
        for j in [0, -1]:
            array[i, j] = get_height_value()


def diamond(array, x1, y1, x2, y2, iteration=1, smoothing_array=None, variance=1.0):
    """Perform the Diamond step of the Diamond-Square algorithm on layer."""

    mid_x = int((x1 + x2) * 0.5)
    mid_y = int((y1 + y2) * 0.5)

    corner_a = array[x1, y1]
    corner_b = array[x1, y2]
    corner_c = array[x2, y1]
    corner_d = array[x2, y2]
    values = [corner_a, corner_b, corner_c, corner_d]

    smoothness = smoothing_array[mid_x, mid_y]
    value = get_height_value(values=values, iteration=iteration, smoothing=smoothness, variance=variance)
    array[mid_x, mid_y] = value

    print('x1: {0} x2: {1} y1: {2} y2: {3} value: {4}'.format(x1, x2, y1, y2, value))


def square(array, x1, y1, x2, y2, iteration=1, smoothing_array=None, variance=1.0):
    """Perform the Square step of the Diamond-Square algorithm on layer."""

    mid_x = int((x1 + x2) * 0.5)
    mid_y = int((y1 + y2) * 0.5)
    array_ne = array[x1, y2]
    array_se = array[x2, y2]
    array_nw = array[x1, y1]
    array_sw = array[x2, y1]

    if y1 is 0:
        smoothness_w = smoothing_array[mid_x, y1]
        array[mid_x, y1] = get_height_value([array_sw, array_nw], iteration=iteration, smoothing=smoothness_w,
                                            variance=variance)
    if x1 is 0:
        smoothness_n = smoothing_array[x1, mid_y]
        array[x1, mid_y] = get_height_value([array_nw, array_ne], iteration=iteration, smoothing=smoothness_n,
                                            variance=variance)

    smoothness_e = smoothing_array[mid_x, y2]
    array[mid_x, y2] = get_height_value([array_se, array_ne], iteration=iteration, smoothing=smoothness_e,
                                        variance=variance)

    smoothness_s = smoothing_array[x2, mid_y]
    array[x2, mid_y] = get_height_value([array_se, array_sw], iteration=iteration, smoothing=smoothness_s,
                                        variance=variance)


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
        print("You may need to install matplotlib. (>> pip install matplotlib)")


def main():
    parser = argparse.ArgumentParser(description="Create 2D noise arrays.")
    parser.add_argument('-d', '--destination', type=str, default='default.csv', help='output destination')
    parser.add_argument('-e', '--enlarge', type=int, help='enlarge the map by linear interpolation')
    parser.add_argument('-n', '--normalize', action='store_true', help='normalize to 0.5 mean and 1 range')
    parser.add_argument('-o', '--output', action='store_true', help='print the result to stdout')
    parser.add_argument('-p', '--plot', action='store_true', help='render a plot of the array')
    parser.add_argument('-r', '--random', type=int, default=None, help='random seed')
    parser.add_argument('-s', '--smoothing', action='store_true', help='use a special smoothing array')
    parser.add_argument('-v', '--variance', type=float, default=1.0, help='variance of the array')
    parser.add_argument('size', type=int, help='power of two')
    # parser.add_argument('height', type=int, help='height of the array')
    # parser.add_argument('width', type=int, help='width of the array')
    args = parser.parse_args()

    if args.random:
        setup(args.random)

    size = (2 ** args.size + 1, 2 ** args.size + 1)

    smoothing = numpy.ones(size)
    array = numpy.zeros(size)
    if args.smoothing:
        smoothing = numpy.zeros(size)
        seed_corners(smoothing)
        diamond_square(smoothing, args.size, variance=args.variance)
    seed_corners(array)
    diamond_square(array, args.size, smoothing_array=smoothing, variance=args.variance)

    if args.normalize:
        normalize(array)

    if args.output:
        print(array)

    if args.plot:
        plot(array, size[0], size[1])


if __name__ == '__main__':
    sys.exit(main())
