# fps testing

import os, sys
os.environ['PYGAME_HIDE_SUPPORT_PROMPT'] = "hide"

import pygame, math
pygame.init()

width = 500
height = 500
fps = 60

window = pygame.display.set_mode((width, height))
pygame.display.set_caption(os.path.basename(__file__))
pygame.mouse.set_visible(False)
clock = pygame.time.Clock()

def process(): # process events
    clock.tick(fps)
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            sys.exit()

