# as the name implies
# its pendulum shit because im bored on a saturday

import os
os.environ['PYGAME_HIDE_SUPPORT_PROMPT'] = "hide"

import math
import sys
import colorsys
import pygame
pygame.init()

def hsv2rgb(h,s,v):
    return tuple(round(i * 255) for i in colorsys.hsv_to_rgb(h,s,v))

# global variables
friction = 0
gravity = 9.41 # pendulum gravity
size = 500 # window size in pixels
fps = 60.0 # frames per second to draw the screen at

window = pygame.display.set_mode((size, size))
pygame.display.set_caption("pendulum stuff")

class Pendulum: # class to store pendulum data
    def __init__(self, start, mass, length, color):
        self.start = start # starting angle of the pendulum
        self.mass = mass # pendulum mass
        self.length = length # length of the pendulum
        self.color = color # color for drawing the pendulum

class Pendulum2:
    def __init__(self, cycles, color):
        pass


pendulums = []


frame = 0
run = False
origin = (size / 2, 50)
clock = pygame.time.Clock()
radius = 10
speed = 1

def lighten(color):
    new = []
    for c in color:
        c = min(255, c + 75)
        new.append(c)
    return tuple(new)

number = 30
for i in range(number):
    negative = -1 if i % 2 == 0 else 1
    pendulums.append(Pendulum(-45 - (i), 1, 100 + (i * 5), hsv2rgb(1 / number * i, 1, 1)))
    #pendulums.append(Pendulum(45, 1, 100, (255, 0, 0)))

copy = pendulums.copy()

for p in pendulums:
    angle = -p.start + 90
    adjacent = math.cos(math.radians(angle)) * p.length
    opposite = math.sin(math.radians(angle)) * p.length
    target = (int(origin[0] + adjacent), int(origin[1] + opposite))
    #pygame.draw.line(window, lighten(p.color), origin, target, 3)
    pygame.draw.circle(window, p.color, target, radius)

pygame.display.update()

while True:
    clock.tick(fps)
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            sys.exit()
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_SPACE:
                run = not run
            if event.key == pygame.K_DELETE:
                frame = 0
                pendulums = copy.copy()
    window.fill((0, 0, 0))
    if run:
        frame += 1
        
    for p in pendulums:
        if friction > 0 and frame > 0:
            angle = math.cos((gravity * (frame * speed * p.mass / 2)) / p.length) / (frame/60 * friction) * p.start
            if run:
                print(math.cos((gravity * (frame * speed * p.mass / 2)) / p.length) / (frame/60 * friction) * p.start)
        else:
            angle = math.cos((gravity * (frame * speed * p.mass / 2)) / p.length) * p.start # angle adjustment
        
        angle = -angle + 90
    
        adjacent_orig = math.cos(math.radians(angle)) * 50
        opposite_orig = math.sin(math.radians(angle)) * 50

        orig = (int(origin[0] + adjacent_orig), int(origin[1] + opposite_orig))

        adjacent = math.cos(math.radians(angle)) * p.length
        opposite = math.sin(math.radians(angle)) * p.length
        target = (int(origin[0] + adjacent), int(origin[1] + opposite))
        #pygame.draw.line(window, lighten(p.color), orig, target, 5) 
        pygame.draw.circle(window, p.color, target, radius)

    pygame.display.update()