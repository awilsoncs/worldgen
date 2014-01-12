import numpy as np

ds_generated = ['elevation']


def world_map(size):
    return np.zeros(size, dtype=[('smoothness', 'float16'),
                                 ('elevation', 'float16')])