import numpy as np

ds_generated = ['smoothness', 'elevation', 'volcanism',
                'solubility', 'precious minerals',
                'economic minerals']

def world_map(size):
    return np.zeros(size, dtype=[('locked', 'bool8'),
                                 ('smoothness', 'float16'),
                                 ('elevation', 'float16'),
                                 ('volcanism', 'float16'),
                                 ('solubility', 'float16'),
                                 ('precious minerals', 'float16'),
                                ('economic minerals', 'float16'),
                                ('water depth', 'float16'),
                                ('precipitation', 'float16')])