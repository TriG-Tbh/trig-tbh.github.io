# but this time
# its circles

import os
os.environ['PYGAME_HIDE_SUPPORT_PROMPT'] = "hide"

import math
import sys
import colorsys
import pygame
pygame.init()

size = 500 # window size in pixels
fps = 60.0 # frames per second to draw the screen at
circles = []

#frame = 3600 * 2.85
frame = 0
run = False
origin = (size / 2, size / 2)
clock = pygame.time.Clock()
radius = 10
speed = 1
trailcount = 0

def hsv2rgb(h,s,v):
    return tuple(round(i * 255) for i in colorsys.hsv_to_rgb(h,s,v))

def lighten(color):
    new = []
    for c in color:
        c = min(255, c + 100)
        new.append(c)
    return tuple(new)

class Circle:
    def __init__(self, color, distance, revolutions):
        self.hsv = color
        self.color = hsv2rgb(*color)
        self.distance = distance
        self.r = revolutions / fps


window = pygame.display.set_mode((size, size))
pygame.display.set_caption("circle stuff 1")
pygame.mouse.set_visible(False)

number = 75
for i in range(number):
    circles.append(Circle(((number - i)/number, 1, 1), (i + 1) * 3, i))


#circles = [Circle(hsv2rgb(1, 1, 1), 150, 1)]

for c in circles:
    target = (int(size / 2), int(size / 2 - c.distance))
    pygame.draw.circle(window, c.color, target, radius)

pygame.display.update()

copy = circles.copy()

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
                circles = copy.copy()
            if event.key == 262:
                frame += 10
            if event.key == 260:
                frame -= 10
    window.fill((0, 0, 0))
    if run and frame < (fps * 60 * 6):
        frame += 1
    for c in circles:
        for i in range(min(frame, trailcount)):
            angle = ((c.r * (frame - i - 1) * speed) % 360)
            final = 90 - angle

            xdiff = int(c.distance * math.sin(math.radians(angle)))
            ydiff = -int(c.distance * math.sin(math.radians(final)))

            #print(angle)

            target = (int(size / 2) + xdiff, int(size / 2) + ydiff)
            #pygame.draw.line(window, lighten(p.color), orig, target, 1) 
            pygame.draw.circle(window, hsv2rgb(c.hsv[0], c.hsv[1], c.hsv[2] - (i/trailcount)), target, 3)
    for c in circles:
        angle = ((c.r * frame * speed) % 360)
        final = 90 - angle

        xdiff = int(c.distance * math.sin(math.radians(angle)))
        ydiff = -int(c.distance * math.sin(math.radians(final)))

        #print(angle)

        target = (int(size / 2) + xdiff, int(size / 2) + ydiff)
        #pygame.draw.line(window, lighten(p.color), orig, target, 1) 
        pygame.draw.circle(window, c.color, target, radius)

        
    
    pygame.display.flip()