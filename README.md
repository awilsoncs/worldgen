worldgen
========

A world generator, designed for worldbuilders and DMs who want information beyond maps.

## Using worldgen
To use worldgen, enter

    python worldgen [x] [y]

while in the project folder, where x and y are one plus any power of two (33, 65, 129, 513). The program should output a map after several seconds. On slower computers, maps larger than 513x513 can take a minute or more.

Also, the up and down keys will re-render the map higher and lower oceans, respectively.

## Minor Goals 0.1:

- [ ] Cleanup code for readability, using numpy methods where possible.

- [ ] Refactoring overhaul (lots of DRY problems)

- [ ] Update docstrings to reflect current operation.

## Major Goals for 0.1:

- [ ] Add a variable to control the smoothness of the map, so that I can also add a function to variably smooth some areas more than others.

- [ ] Add bitmap output for Views

- [ ] Add keyboard control to __main__.py
