# grid
import os, sys
os.environ['PYGAME_HIDE_SUPPORT_PROMPT'] = "hide"

import pygame, math
pygame.init()

def smooth1(d, f): # linear
    return [(d/f) * (x + 1) for x in range(f)]

width = 500
height = 500
fps = 60

distance = 20
def realsin(deg):
    return math.sin(math.radians(deg))

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

lines = (height // 2) // distance - 1

dl = distance
dr = distance
dt = distance
db = distance

def draw_lines(dl, dr, dt, db, color):
    pygame.draw.line(window, color, (width // 2 + dt // 2, 0), (width // 2 + db // 2, height))
    for d in range(lines):
        d += 1
        pygame.draw.line(window, color, (width // 2 + dt // 2 + (dt * d), 0), (width // 2 + db // 2 + (db * d), height))
    
    pygame.draw.line(window, color, (width // 2 - dt // 2, 0), (width // 2 - db // 2, height))
    for d in range(lines):
        d += 1
        pygame.draw.line(window, color, (width // 2 - dt // 2 - (dt * d), 0), (width // 2 - db // 2 - (db * d), height))

    pygame.draw.line(window, color, (0, height // 2 + dl // 2), (width, height // 2 + dr // 2))
    for d in range(lines):
        d += 1
        pygame.draw.line(window, color, (0, height // 2 + dl // 2 + (dl * d)), (width, height // 2 + dr // 2 + (dr * d)))
    
    pygame.draw.line(window, color, (0, height // 2 - dl // 2), (width, height // 2 - dr // 2))
    for d in range(lines):
        d += 1
        pygame.draw.line(window, color, (0, height // 2 - dl // 2 - (dl * d)), (width, height // 2 - dr // 2 - (dr * d)))

while True:
    for i in range(fps * 2):
        change = math.sin(math.radians((i - (fps // 4)) * 3)) / 2 + 0.5
        change2 = math.cos(math.radians((i - (fps // 4)) * 3)) / 2 + 0.5

        dt = distance + (distance * change)
        db = distance + (distance * change2)
        dl = distance + (distance * change)
        dr = distance + (distance * change)

        
        


        #print(i / 30)
        #print(dt)

        process()
        window.fill((0, 0, 0))
        
        
        draw_lines(dl, dr, dt, db, (255, 0, 0))
        #draw_lines(dr, dl, dt, db, (255, 0, 255))
        #draw_lines(dl, dr, dt, db, (0, 0, 255))
        

        pygame.display.update()