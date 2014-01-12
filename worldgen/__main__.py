import sys
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
    worldmap = worldmaps.world_map(size)
    worldmap = dsprocess.process(worldmap)

    #climate.build_climate(worldmap)
    #scaling.scale(worldmap, ['precipitation'])

    pygame.init() 
    window = pygame.display.set_mode(size)
    layer = np.copy(worldmap['smoothness'])
    altview = views.RedGreenView(window, layer)
    #altview = views.PrecipitationView(window, worldmap)
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
                print "Elevation: %f" % worldmap[pos[0], pos[1]]['elevation']
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_UP:
                    depth += float(config_file['ocean_change'])  
                elif event.key == pygame.K_DOWN:
                    depth -= float(config_file['ocean_change']) 
                elif event.key == pygame.K_RIGHT:
                    layer = np.roll(layer, scroll, axis=0)
                elif event.key == pygame.K_LEFT:
                    layer = np.roll(layer, -1 * scroll, axis=0)
                altview = views.RedGreenView(window, layer)
                altview.render()
                pygame.display.flip()  

if __name__ == '__main__':
    main()