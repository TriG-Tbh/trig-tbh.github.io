# smoothing tests

import os, sys
os.environ['PYGAME_HIDE_SUPPORT_PROMPT'] = "hide"

import pygame, math, colorsys
pygame.init()

def smooth1(d, f): # linear
    return [(d/f) * (x + 1) for x in range(f)]

def smooth2(d, f): # quadratic
    return [(d/(f ** 2)) * ((x + 1) ** 2) for x in range(f)]

def smooth3(d, f): # quadratic (reversed)
    return [-(d/(f ** 2)) * (((x + 1) - f) ** 2) + d for x in range(f)]

def smooth4(d, f): # elliptic
    ranges = [x + 1 for x in range(f)]
    return [(d * math.sqrt(x * ((2 * f) - x)) ) / f for x in ranges]

def smooth5(d, f): # elliptic (reversed)
    ranges = [x + 1 for x in range(f)]
    return [-(d * math.sqrt(f ** 2 - x ** 2)) / f + d for x in ranges]

def smooth6(d, f): # sin
    return [d * math.sin((math.pi * (x + 1)) / (2 * f)) for x in range(f)]

def smooth7(d, f): # cos
    return [-d * math.cos((math.pi * (x + 1)) / (2 * f)) + d for x in range(f)]

def hsv2rgb(h,s,v):
    return tuple(round(i * 255) for i in colorsys.hsv_to_rgb(h,s,v))

def setup(d, f):
    return [smooth1(d, f),
    smooth2(d, f),
    smooth3(d, f),
    smooth5(d, f),
    smooth4(d, f),
    smooth7(d, f),
    smooth6(d, f)]

def draw_circles(ranges, frame):
    hue = 0
    for s in ranges:
        pygame.draw.circle(window, hsv2rgb(hue / len(ranges), 1, 1), (round(s[frame]) + (width // 4), 65 * (hue + 1)), 10)
        hue += 1

def draw_circles2(ranges, frame):
    hue = 0
    for s in ranges:
        pygame.draw.circle(window, hsv2rgb(hue / len(ranges), 1, 1), (round(s[frame]) + (width * 3 // 4), 65 * (hue + 1)), 10)
        hue += 1

lines = ["Linear", "Quadratic", "Quadratic (reverse)", "Elliptic", "Elliptic (reverse)", "Cosine", "Sine"]
font = pygame.font.SysFont("Calibri", 30)
color = (255, 255, 255)
text = [font.render(l, False, color) for l in lines]


def put_text():
    tpos = 0
    for t in text:
        pos = (width // 2 - t.get_width() // 2, 65 * tpos + 20)
        tpos += 1

        window.blit(t, pos)

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

setup1 = setup(width // 2, 120)
setup2 = setup(-width // 2, 120)

for _ in range(4):
    for i in range(120):
        process()
        window.fill((0, 0, 0))
        draw_circles(setup1, i)
        put_text()
        pygame.display.update()
    for i in range(120):
        process()
        window.fill((0, 0, 0))
        draw_circles2(setup2, i)
        put_text()
        pygame.display.update()
