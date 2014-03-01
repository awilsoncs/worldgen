import numpy as np

ds_generated = ['elevation',
                'volcanism',
                'solubility',
                'minerals']


def world_map(size):
    return np.zeros(size, dtype=[('smoothness', 'float16'),
                                 ('elevation', 'float16'),
                                 ('volcanism', 'float16'),
                                 ('solubility', 'float16'),
                                 ('minerals', 'float16')])