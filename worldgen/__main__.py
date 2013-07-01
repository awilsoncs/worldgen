import sys
import algorithm

import pygame
pygame.init() 

## Generation functions

script, size = sys.argv[0], int(sys.argv[1])

## Run the code
window = pygame.display.set_mode((size, size))
a = algorithm.process(window, size)
px = algorithm.build_pxarray(window, a)
pygame.display.flip()
del px
## Boilerplate
while True:
    for event in pygame.event.get(): 
        if event.type == pygame.QUIT: 
            sys.exit(0) 
        else: 
            print event 
