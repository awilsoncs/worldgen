import sys
import math
import time

import pygame
import numpy as np

import climate
import dsprocess
import worldmaps
import views

def main():
    t = time.time()

    script, x, y = sys.argv[0], int(sys.argv[1]), int(sys.argv[2])
    size = (x, y)
    if x <= 0 or y <= 0:
        print "ERROR: Invalid size: %d" % size
        print "\tSetting size to 257"
        size = (257, 257)
    if math.log(x-1, 2) % 1 != 0.0 or math.log(y-1, 2) % 1 != 0.0:
        print "ERROR: Invalid size: %d" % size
        print "\tMust be (2^n)+1"
        sys.exit(0)

    worldmap = worldmaps.Worldmap(size)
    worldmap = dsprocess.process(worldmap)
    depth = 0.6
    climate.build_climate(worldmap)

    pygame.init() 
    window = pygame.display.set_mode(size)
    altview = views.ElevationView_wOcean(window, worldmap, depth)
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
                    depth += 0.005  
                elif event.key == pygame.K_DOWN:
                    depth -= 0.005
                elif event.key == pygame.K_RIGHT:
                    worldmap = np.roll(worldmap, 5, axis=0)
                elif event.key == pygame.K_LEFT:
                    worldmap = np.roll(worldmap, -5, axis=0)
                altview = views.ElevationView_wOcean(window, worldmap, depth)
                altview.render()
                pygame.display.flip()  


if __name__ == '__main__':
    main()