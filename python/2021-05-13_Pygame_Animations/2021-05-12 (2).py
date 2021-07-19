# circles

import os, sys
os.environ['PYGAME_HIDE_SUPPORT_PROMPT'] = "hide"

import pygame, math
pygame.init()


def smooth2(d, f): # quadratic
    return [(d/(f ** 2)) * ((x + 1) ** 2) for x in range(f)]

def smooth3(d, f): # quadratic (reversed)
    return [-(d/(f ** 2)) * (((x + 1) - f) ** 2) + d for x in range(f)]



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

enter_vals = smooth3(width // 4, 120)
exit_vals = smooth3(width // 4, 100)


while True:
    for i in range(119):
        process()
        window.fill((0, 0, 0))
        pygame.draw.circle(window, (255, 255, 255), (width // 2, height // 2), int(enter_vals[i]))
        if i >= 20:
            pygame.draw.circle(window, (0, 0, 0), (width // 2, height // 2), int(exit_vals[i - 20]) + 2)
        pygame.display.update()