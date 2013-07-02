worldgen
========

A world generator

Goals:
* Isolate the model, view, and control so that different views of the model can show off the new dictionary values.
* Rework scaling to use all values 0.0-1.0 rather than just max = 1.0
* Prepare the algorithm for spherical projection by seeding identical 1D midpoint-displacement lines on the far left and right edges before running the Diamond-Square algorithm. For the top and bottom, seed each element with an identical value (simple implementation compared to the alternative).
* Add a variable to control the smoothness of the map, so that I can also add a function to variably smooth some areas more than others.
