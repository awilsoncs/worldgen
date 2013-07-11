import numpy as np
import pygame

import worldmaps

class MapView(object):
    def __init__(self, surface, worldmap):
        self.worldmap = worldmap
        self.surface = surface
    
    def render(self):
        """Renders a pxarray based on 'key' of Worldmap."""
        print "Rendering elevation"
        pxarray = pygame.PixelArray(self.surface)
        self.paint(pxarray)
        del pxarray

    def paint(self, pxarray):
        pass

class ElevationView(MapView):
    def __init__(self, surface, worldmap):
        MapView.__init__(surface, worldmap)
        self.key = 'elevation'

    def paint(self, pxarray):
        """Returns a pxarray based on 'elevation' of Worldmap."""
        for (x, y), loc in np.ndenumerate(self.worldmap):
            g = loc[self.key]*255
            r = (255 - g) / 2
            b = g / 4
            pxarray[x, y] = (r, g, b)

class ElevationView_wOcean(MapView):
    def __init__(self, surface, worldmap, depth):
        MapView.__init__(self, surface, worldmap)
        self.key = 'elevation'
        self.depth = depth

    def paint(self, pxarray):
        for (x, y), loc in np.ndenumerate(self.worldmap):
            r,g,b = 0,0,0
            v = loc[self.key]
            if v < self.depth:
                b = v*255
                g = b / 2
            else:
                v = v - self.depth
                r = v * 255
                g = 170 - r
                b = 110 * (g / 255)
            pxarray[x, y] = (r, g, b)

class ContourView(ElevationView_wOcean):
    def __init__(self, surface, worldmap, depth):
        ElevationView_wOcean.__init__(self, surface, worldmap,
            depth)

    def paint(self, pxarray):
        """Returns an elevation contour map."""
        for (x, y), loc in np.ndenumerate(self.worldmap):
            r,g,b = 0,0,0
            v = loc[self.key]
            if v < self.depth:
                r,g,b = 0, 125, 255
            elif v < self.depth + 0.05:
                r,g,b = 0, 125, 60
            elif v < self.depth + .1:
                r,g,b = 25, 100, 30
            elif v < self.depth + .15:
                r,g,b = 50, 75, 15
            elif v < self.depth + .2:
                r,g,b = 100, 50, 0
            elif v < self.depth + .25:
                r,g,b = 150, 25, 0
            elif v < self.depth + .3:
                r,g,b = 175, 25, 0
            elif v < self.depth + .35:
                r,g,b = 200, 25, 0
            elif v > self.depth + .35:
                r,g,b = 220, 25, 0
            pxarray[x, y] = (r, g, b)

class VolcanoChance(MapView):
    def __init__(self, surface, worldmap):
        MapView.__init__(self, surface, worldmap)

    def paint(self, pxarray):
        for (x, y), loc in np.ndenumerate(self.worldmap):
            r = loc['volcanism'] * 255
            g = loc['elevation'] * 255
            b = loc['smoothness'] * 255
            pxarray[x, y] = (r, g, b)