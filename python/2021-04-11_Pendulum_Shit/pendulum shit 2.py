# once again
# pendulum shit because im bored on a saturday

import os
os.environ['PYGAME_HIDE_SUPPORT_PROMPT'] = "hide"

import math
import sys
import colorsys
import pygame
pygame.init()

size = 500 # window size in pixels
fps = 60.0 # frames per second to draw the screen at
pendulums = []

frame = 0
run = False
origin = (size / 2, 50)
clock = pygame.time.Clock()
radius = 10
speed = 0.5

def get_degree(a, b, c):
    pass

def hsv2rgb(h,s,v):
    return tuple(round(i * 255) for i in colorsys.hsv_to_rgb(h,s,v))

def lighten(color):
    new = []
    for c in color:
        c = min(255, c + 100)
        new.append(c)
    return tuple(new)

class Pendulum2:
    def __init__(self, position, cycles, color):
        self.position = position
        self.cycles = cycles
        self.color = color

        diffx = position[0] - origin[0]
        diffy = position[1] - origin[1]
        x = diffx
        y = diffy
        
        #print(diffx, diffy)

        self.length = math.sqrt(diffx**2 + diffy**2)
        z = self.length
        self.start = -(math.degrees(math.atan2(diffy, diffx)) - 90)
        #print(self.start)

        self.diffx = diffx
        self.diffy = diffy
        #input()




window = pygame.display.set_mode((size, size))
pygame.display.set_caption("pendulum stuff 2")

number = 50
for i in range(number):
    pendulums.append(Pendulum2((size / 4, (origin[1] + 10) + (i * 5)), number - (0.25 * (number - i + 1)), hsv2rgb((number - i)/number, 1, 1)))

copy = pendulums.copy()


for p in pendulums:
    target = (int(origin[0] + p.diffx), int(origin[1] + p.diffy))
    #pygame.draw.line(window, lighten(p.color), origin, target, 3)
    pygame.draw.circle(window, p.color, target, radius)


pygame.display.update()

#input()
while True:
    clock.tick(fps)
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            sys.exit()
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_ESCAPE:
                pygame.quit(); sys.exit()
            if event.key == pygame.K_SPACE:
                run = not run
            if event.key == pygame.K_DELETE:
                frame = 0
                pendulums = copy.copy()
            if event.key == 262:
                frame += 10
            if event.key == 260:
                frame -= 10
    window.fill((0, 0, 0))
    if run:
        frame += 1


    for p in pendulums:
        angle = p.start
        diff = (math.cos(math.radians((math.pi * frame * speed) * (p.cycles / 30))))
        angle = (-angle * diff) + 90
        adjacent_orig = math.cos(math.radians(angle)) * 50
        opposite_orig = math.sin(math.radians(angle)) * 50
        

        orig = (int(origin[0] + adjacent_orig), int(origin[1] + opposite_orig))

        adjacent = math.cos(math.radians(angle)) * p.length
        opposite = math.sin(math.radians(angle)) * p.length
        target = (int(origin[0] + adjacent), int(origin[1] + opposite))
        #pygame.draw.line(window, lighten(p.color), orig, target, 1) 
        pygame.draw.circle(window, p.color, target, radius)

    pygame.display.update()