import numpy as np

ds_generated = ['elevation',
                'volcanism',
                'solubility',
                'minerals']


def world_map(size):
    """
    @type size : tuple
    @rtype : recarray
    """
    return np.zeros(size, dtype=[('depth', 'float16'),
                                 ('smoothness', 'float16'),
                                 ('elevation', 'float16'),
                                 ('volcanism', 'float16'),
                                 ('solubility', 'float16'),
                                 ('minerals', 'float16'),
                                 ('water depth', 'float16')])