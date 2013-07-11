import sys
import math
import time

import pygame

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

    wm = worldmaps.Worldmap(size)
    wm = dsprocess.process(wm)
    depth = 0.6

    pygame.init() 
    window = pygame.display.set_mode(size)
    altview = views.ElevationView_wOcean(window, wm, depth)
    altview.render()
    pygame.display.flip()

    print "Ran in %r seconds." % (time.time() - t)

    while True:
        for event in pygame.event.get(): 
            if event.type == pygame.QUIT: 
                sys.exit(0) 
            elif event.type == pygame.KEYDOWN:
                if event.key == 273: #up key
                    depth += 0.05
                    altview = views.ElevationView_wOcean(window, wm, depth)
                    altview.render()
                    pygame.display.flip()    
                elif event.key == 274: #down key
                    depth -= 0.05
                    altview = views.ElevationView_wOcean(window, wm, depth)
                    altview.render()
                    pygame.display.flip()

if __name__ == '__main__':
    main()