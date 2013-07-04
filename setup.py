try:
    from setuptools import setup
except ImportError:
    from distutils.core import setup

config = {
    'version': '0.1a'
    'description': 'World Generator',
    'author': 'Aaron Wilson',
    'url': 'URL to get it at',
    'download_url': 'Where to download it.',
    'author_email': 'aaronwilsonguitar@gmail.com',
    'version': '0.1',
    'install_requires': ['nose'],
    'packages': ['worldgen', 'worldgen.algorithm', 'worldgen.worldmaps'],
    'scripts': [],
    'name': 'worldgen'
}

setup(**config)
