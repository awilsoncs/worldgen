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
    'packages': ['worldgen'],
    'requires': ['numpy', 'pygame'],
    'scripts': [],
    'name': 'worldgen'
}

setup(**config)
