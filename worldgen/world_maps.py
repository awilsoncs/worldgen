import numpy as np

geology = ['elevation',
           'solubility',
           'volcanism',
           'minerals']


def world_map(size):
    """
    @type size : tuple
    @rtype : recarray
    """
    return np.zeros(size, dtype=[('elevation', 'float16'),
                                 ('volcanism', 'float16'),
                                 ('precipitation', 'float16'),
                                 ('solubility', 'float16'),
                                 ('temperature', 'float16'),
                                 ('minerals', 'float16'),
                                 ('water depth', 'float16')])
