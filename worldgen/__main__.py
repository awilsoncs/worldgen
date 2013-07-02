## Packaged modules
import sys
import math
import time

## Local modules
import algorithm
import worldmaps
import views

## Pygame
import pygame
pygame.init() 
t = time.time()

## Input handling
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

## Run the code
window = pygame.display.set_mode(size)
wm = worldmaps.Worldmap(size)
wm = algorithm.process(wm)
depth = 0.7
altview = views.AltitudeView_wOcean(window, wm, depth)
altview.render()
pygame.display.flip()

print "Ran in %r seconds." % (time.time() - t)
## Boilerplate
while True:
    for event in pygame.event.get(): 
        if event.type == pygame.QUIT: 
            sys.exit(0) 
        elif event.type == pygame.KEYDOWN:
            if event.key == 273: #up key
                depth += 0.1
                altview = views.AltitudeView_wOcean(window, wm, depth)
                altview.render()
                pygame.display.flip()    
            elif event.key == 274: #down key
                depth -= 0.1
                altview = views.AltitudeView_wOcean(window, wm, depth)
                altview.render()
                pygame.display.flip()
            
            
            
            
            
            
