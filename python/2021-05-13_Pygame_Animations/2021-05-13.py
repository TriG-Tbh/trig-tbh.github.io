import os, sys
os.environ['PYGAME_HIDE_SUPPORT_PROMPT'] = "hide"

import pygame, math
pygame.init()

def smooth1(d, f): # linear
    return [(d/f) * (x + 1) for x in range(f)]

width = 500
height = 500
fps = 60
h = math.sqrt(50**2 + 100**2)

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

center = (width / 2, height / 2)

points = [
    (center[0], center[1] - 100),
    (center[0] + 100, center[1] - 50),
    (center[0] + 100, center[1] - 50 + h),
    (center[0], center[1] + 100),
    (center[0] - 100, center[1] - 50 + h),
    (center[0] - 100, center[1] - 50),
    center,
    (center[0] + h/2, center[1])
]

copy = points.copy()
doublecopy = points.copy()

def draw1(frame):
    if frame < 59:
        pygame.draw.polygon(window, (250, 100, 100), [points[5], points[6], points[3], points[4]])
    pygame.draw.polygon(window, (250, 0, 0), [points[0], points[1], points[6], points[5]])
    pygame.draw.polygon(window, (150 + smooth1(50, 60)[frame], 0, 0), [points[1], points[2], points[3], points[6]])


def draw2(frame):
    pygame.draw.polygon(window, (25 + smooth1(125, 60)[frame], 0, 0), [points[0], points[1], points[2], points[7]])
    pygame.draw.polygon(window, (250, 0, 0), [points[0], points[1], points[6], points[5]])
    pygame.draw.polygon(window, (200 + smooth1(50, 60)[frame], smooth1(100, 60)[frame], smooth1(100, 60)[frame]), [points[1], points[2], points[3], points[6]])
    

rot1 = [
    (smooth1(h / 2, 60), smooth1(-h/2 + 100, 60)),
    (smooth1(-100 + h/2, 60), smooth1(50, 60)),
    (smooth1(-100 + h/2, 60), smooth1(-h + 50 + h, 60)),
    (smooth1(-h/2, 60), smooth1(h - 100, 60)),
    (smooth1(100 - h/2, 60), smooth1(-h + 50, 60)),
    (smooth1(100 - h/2, 60), smooth1(50 - h/2, 60)),
    (smooth1(-h/2, 60), smooth1(0, 60)),
    (smooth1(0, 60), smooth1(0, 60))
]


rot2 = [
    (smooth1(-h/2 + 100, 60), smooth1(h/2 - 50, 60)),
    (smooth1(-h/2, 60), smooth1(0, 60)),
    (smooth1(-h/2, 60), smooth1(-h + 100, 60)),
    (smooth1(h/2 - 100, 60), smooth1(-50, 60)),
    (smooth1(0, 60), smooth1(0, 60)),
    (smooth1(h/2, 60), smooth1(h/2 - 100, 60)),
    (smooth1(h/2 - 100, 60), smooth1(-50, 60)),
    (smooth1(-h/2 + 100, 60), smooth1(-50 + h, 60))
]

for _ in range(8):
    for i in range(60):
        process()
        for r in range(len(rot1)):
            points[r] = (copy[r][0] + rot1[r][0][i], copy[r][1] + rot1[r][1][i])

        window.fill((0, 0, 0))
        draw1(i)
        pygame.display.update()

    copy = points.copy()
    for i in range(60):
        process()
        for r in range(len(rot2)):
            points[r] = (copy[r][0] + rot2[r][0][i], copy[r][1] + rot2[r][1][i])

        window.fill((0, 0, 0))
        draw2(i)
        pygame.display.update()
    points = doublecopy.copy()
    copy = points.copy()