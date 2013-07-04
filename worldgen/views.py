import pygame
import worldmaps
import numpy as np

class MapView(object):
    def __init__(self, surface, worldmap, key):
        self.wm = worldmap
        self.surface = surface
        self.key = key
    
    def render(self):
        '''
        Renders a pxarray based on 'key' of Worldmap.
        '''
        print "Rendering Altitude"
        pxarray = pygame.PixelArray(self.surface)
        self.paint(pxarray)
        del pxarray

    def paint(self, pxarray):
        pass

class AltitudeView(MapView):
    def __init__(self, surface, worldmap):
        MapView.__init__(surface, worldmap, key='altitude')

    def paint(self, pxarray):
        '''
        Returns a pxarray based on 'altitude' of Worldmap.
        '''
        for (x, y), loc in np.ndenumerate(self.wm):
            g = loc[self.key]*255
            r = (255 - g) / 2
            b = g / 2
            pxarray[x, y] = (r, g, b)

class AltitudeView_wOcean(MapView):
    def __init__(self, surface, worldmap, depth):
        MapView.__init__(self, surface, worldmap, key='altitude')
        self.depth = depth

    def paint(self, pxarray):
        '''
        Returns a pxarray based on 'altitude' of Worldmap.
        '''
        for (x, y), loc in np.ndenumerate(self.wm):
            r,g,b = 0,0,0
            v = loc[self.key]
            if v < self.depth:
                b = v*255
            else:
                g = v*255
                r = (255 - g) / 2
                b = g / 2
            pxarray[x, y] = (r, g, b)
    
