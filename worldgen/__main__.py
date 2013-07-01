## Packaged modules
import sys
import math
import time

## Local modules
import algorithm

## Pygame
import pygame
pygame.init() 
t = time.time()
## Generation functions

script, size = sys.argv[0], int(sys.argv[1])

if size <= 0:
    print "ERROR: Invalid size: %d" % size
    print "\tSetting size to 257"
    size = 257
if math.log(size-1, 2) % 1 != 0.0:
    print "ERROR: Invalid size: %d" % size
    print "\tMust be (2^n)+1"
    sys.exit(0)

## Run the code
window = pygame.display.set_mode((size, size))
a = algorithm.process(window, size)
px = algorithm.build_pxarray(window, a)
pygame.display.flip()
print "Ran in %r seconds." % (time.time() - t)
del px
## Boilerplate
while True:
    for event in pygame.event.get(): 
        if event.type == pygame.QUIT: 
            sys.exit(0) 
        else: 
            print event 
