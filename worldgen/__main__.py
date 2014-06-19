import sys
import time

import pygame
import numpy as np

import climate
from config import Config
import dsprocess
import worldmaps
import views


def main():
    t = time.time()

    config_file = Config('config.txt')

    x = int(config_file['size_x'])
    y = int(config_file['size_y'])
    size = (x, y)
    scroll = int(config_file['scroll'])
    world_map = worldmaps.world_map(size)
    world_map = dsprocess.process(world_map)
    world_map = climate.process(world_map)

    #climate.build_climate(world_map)
    #scaling.scale(world_map, ['precipitation'])

    pygame.init() 
    window = pygame.display.set_mode(size)
    layer = np.copy(world_map['smoothness'])
    elevation_view = views.BlackWhiteView(window, layer)
    #elevation_view = views.PrecipitationView(window, world_map)
    elevation_view.render()
    pygame.display.flip()

    print "Ran in %r seconds." % (time.time() - t)

    while True:
        for event in pygame.event.get(): 
            if event.type == pygame.QUIT: 
                sys.exit(0)
            elif event.type == pygame.MOUSEBUTTONDOWN:
                pos = event.pos
                print pos
                print "Elevation: %f" % world_map[pos[0], pos[1]]['elevation']
                print "Depth: %f" % world_map[pos[0], pos[1]]['water depth']
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_RIGHT:
                    layer = np.roll(layer, scroll, axis=0)
                elif event.key == pygame.K_LEFT:
                    layer = np.roll(layer, -1 * scroll, axis=0)
                elevation_view = views.BlackWhiteView(window, layer)
                elevation_view.render()
                pygame.display.flip()  

if __name__ == '__main__': main()