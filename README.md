worldgen 0.2 alpha
========

Worldgen is a procedural generation project.

## Using worldgen

The software does not currently accept any flags or parameters. It will generate a config file when it runs for the first time (or if the config file has been deleted). Simply run

    python __main__.py

Generating the map may take longer than expected. Maps with a very high scale, such as 11 or 12, may take several minutes.

## Config File

The config file can be found in the program directory as

    config.ini
    
## World Building Stages

### Geology
Each geological stage is built using the smoothed diamond-square method found in diamond_square.py.

* Elevation
* Minerals
* Volcanism
* Solubility

### Climate
#### Temperature
#### Precipitation
