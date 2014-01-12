import numpy as np
import pygame



class MapView(object):
    def __init__(self, surface, layer):
        self.layer = layer
        self.surface = surface

    def render(self):
        """Renders a pxarray based on 'key' of Worldmap."""
        pxarray = pygame.PixelArray(self.surface)
        self.paint(pxarray)
        del pxarray

    def paint(self, pxarray):
        pass


class RedGreenView(MapView):
    def __init__(self, surface, layer):
        MapView.__init__(self, surface, layer)

    def paint(self, pxarray):
        """Returns a pxarray based on 'elevation' of Worldmap."""
        for (x, y), v in np.ndenumerate(self.layer):
            g = v * 255
            r = (255 - g) / 2
            b = g / 4
            pxarray[x, y] = (r, g, b)