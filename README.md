worldgen 0.2 alpha
========

A world generator, designed for worldbuilders and DMs who want information beyond maps.

## Using worldgen

The software does not currently accept any flags or parameters. It will generate a config file when it runs for the first time (or if the config file has been deleted).

Generating the map may take longer than expected. Large maps (dimensions larger than 513x513) can take several minutes.

## Config File

The config file can be found in the program directory as

    config.ini

The options are as follows-

======Parameters=====

size_x: Integer. The x dimension of the map. Must be a power of two, plus 1.

size_y: Integer. The y dimension of the map. Must be a power of two, plus 1.

depth: The depth of the ocean, a float between 0 and 1.

variance:
=======Climate=======

moisture_pickup: Float. The rate of moisture pickup from trade winds.

moisture_drop: Float. The rate of precipitation dropped on land from trade winds.

winds: Integer. How rapidly the trade winds cross the map.

=======Controls======

scroll: Integer. The left/right motion when a key is pressed while viewing the map.