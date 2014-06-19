import numpy as np
import pygame


class LayerView(object):
    def __init__(self, surface, layer):
        self.layer = layer
        self.surface = surface

    def render(self):
        """Renders a pxarray based on 'key' of Worldmap."""
        pixel_array = pygame.PixelArray(self.surface)
        self.paint(pixel_array)
        del pixel_array

    def paint(self, pxarray):
        pass


class RedGreenView(LayerView):
    def __init__(self, surface, layer):
        LayerView.__init__(self, surface, layer)

    def paint(self, pixel_array):
        """Returns a pxarray based on 'elevation' of Worldmap."""
        for (x, y), v in np.ndenumerate(self.layer):
            g = v * 255
            r = (255 - g) / 2
            b = g / 4
            pixel_array[x, y] = (r, g, b)