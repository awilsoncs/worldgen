import numpy as np


def elevation(array):
    # Coefficients calculated from real-world data. See https://github.com/awilsoncs/earth-elevation-regression
    print("- Adjusting elevation")
    theta = [-1.35781688e+04, 4.63803433e+04, -5.80711361e+04, 3.11929158e+04, -5.29419797e+03, -8.60736418e+02,
             3.73555701e+02, 5.27074085e+01]
    for (x, y), z in np.ndenumerate(array):
        value = [z ** n for n in range(7, -1, -1)]
        array[x, y] = np.dot(theta, value)
    normalize(array)
    return array


# def elevation(x):
#     """Return float x adjusted for earth-like elevations"""
#     vector_atan = np.vectorize(math.atan)
#     y = 20 * x - 10
#     y2 = x - 0.5
#     return 0.05 * (vector_atan(y) + 220 * (y2 ** 5)) + 0.5


def normalize(array):
    """Scale all values in the array to 0.0-1.0 floats."""
    high = array.max()
    low = array.min()
    rng = high - low
    array[:] = 1.0 - ((high - array) / rng)
