worldgen 0.2 alpha
========

A world generator, designed for worldbuilders and DMs who want information beyond maps.

## Using worldgen

The software does not currently accept any flags or parameters. It will generate a config file when it runs for the first time (or if the config file has been deleted).

Generating the map may take longer than expected. Large maps (dimensions larger than 513x513) can take several minutes.

## Config File

======Parameters=====
size_x: the x dimension of the map
size_y: the y dimension of the map
depth: the depth of the ocean, a float between 0 and 1.

=======Climate=======
moisture_pickup: Float. The rate of moisture pickup from trade winds.
moisture_drop: Float. The rate of precipitation dropped on land from trade winds.
winds: Integer. How rapidly the trade winds cross the map.

=======Controls======
scroll=5