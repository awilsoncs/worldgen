try:
    from setuptools import setup
except ImportError:
    from distutils.core import setup

config = {
    'version': '0.1a',
    'description': 'World Generator',
    'author': 'Aaron Wilson',
    'author_email': 'aaronwilsonguitar@gmail.com',
    'install_requires': ['nose'],
    'packages': ['worldgen', 'worldgen.algorithm', 'worldgen.worldmaps',
                 'numpy'],
    'scripts': [],
    'name': 'worldgen'
}

setup(**config)
