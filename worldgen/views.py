import pygame
import worldmaps

class AltitudeView(object):
    def __init__(self, surface, worldmap):
        self.wm = worldmap
        self.surface = surface

    def render(self):
        '''
        Returns a greyscale pxarray based on input array.
        '''
        print "Rendering Altitude"
        surface = self.surface
        wm = self.wm
        key = 'altitude'
        pxarray = pygame.PixelArray(surface)
        for x in range(wm.shape[0]):
            for y in range(wm.shape[1]):
                g = wm.get((x, y), key)*255
                r = (255 - g) / 2
                b = g / 2
                pxarray[x, y] = (r, g, b)
        del pxarray  

class AltitudeView_wOcean(object):
    def __init__(self, surface, worldmap):
        self.wm = worldmap
        self.surface = surface

    def render(self):
        '''
        Returns a greyscale pxarray based on input array.
        '''
        print "Rendering Altitude with Oceans"
        surface = self.surface
        wm = self.wm
        key = 'altitude'
        pxarray = pygame.PixelArray(surface)
        for x in range(wm.shape[0]):
            for y in range(wm.shape[1]):
                r,g,b = 0,0,0
                v = wm.get((x, y), key)
                if v < 0.8:
                    b = v*255
                else:
                    g = v*255
                    r = (255 - g) / 2
                    b = g / 2
                pxarray[x, y] = (r, g, b)
        del pxarray 
    
    
