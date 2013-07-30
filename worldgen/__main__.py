import sys
import math
import time

import pygame
import numpy as np

import climate
from config import Config
import dsprocess
import worldmaps
import views
import scaling

def main():
    t = time.time()

    config_file = Config('config.txt')

    x = int(config_file['size_x'])
    y = int(config_file['size_y'])
    size = (x, y)
    scroll = int(config_file['scroll'])
    worldmap = worldmaps.Worldmap(size)
    worldmap = dsprocess.process(worldmap)

    climate.build_climate(worldmap)
    scaling.scale(worldmap, ['precipitation'])

    pygame.init() 
    window = pygame.display.set_mode(size)
    altview = views.PrecipitationView(window, worldmap)
    altview.render()
    pygame.display.flip()

    print "Ran in %r seconds." % (time.time() - t)

    while True:
        for event in pygame.event.get(): 
            if event.type == pygame.QUIT: 
                sys.exit(0)
            elif event.type == pygame.MOUSEBUTTONDOWN:
                pos = event.pos
                print pos
                print "Elevation: %f" % worldmap.get(pos, 'elevation')
                print "Precipitation: %r" % worldmap.get(pos, 'precipitation')
                if worldmap.get(pos, 'ocean'):
                    print "Ocean"
                else:
                    print "Land"
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_UP:
                    depth += float(config_file['ocean_change'])  
                elif event.key == pygame.K_DOWN:
                    depth -= float(config_file['ocean_change']) 
                elif event.key == pygame.K_RIGHT:
                    worldmap = np.roll(worldmap, scroll, axis=0)
                elif event.key == pygame.K_LEFT:
                    worldmap = np.roll(worldmap, -1 * scroll, axis=0)
                altview = views.PrecipitationView(window, worldmap)
                altview.render()
                pygame.display.flip()  

if __name__ == '__main__':
    main()