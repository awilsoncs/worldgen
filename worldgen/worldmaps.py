import numpy as np

ds_generated = ['smoothness']


def world_map(size):
    return np.zeros(size, dtype=[('smoothness', 'float16')])