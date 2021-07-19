import settings
import random

import os, sys
os.environ['PYGAME_HIDE_SUPPORT_PROMPT'] = '1'

import pygame
import pygame.freetype
pygame.init()
pygame.mouse.set_visible(False)

import os

basedir = os.path.dirname(os.path.realpath(__file__))

size = pygame.display.list_modes()[0]
window = pygame.display.set_mode(size, pygame.FULLSCREEN)

clock = pygame.time.Clock()

game_settings = {
    "apples": 15,
    "obstacles": 15,
    "wrap-around": False
}

font = pygame.font.Font(os.path.join(basedir, "forward.ttf"), 50)

font2 = pygame.font.Font(os.path.join(basedir, "forward.ttf"), 24)
snake = font.render("SNAKE", 0, (255, 255, 255))
ssize = font.size("SNAKE")

start = font2.render("Press space to start.", 0, settings.LIME)
stsize = font2.size("Press space to start.")

def quit_game():
    pygame.quit()
    sys.exit()


def check_events():
    for event in pygame.event.get():
        if event == pygame.QUIT:
            quit_game()
        keys = pygame.key.get_pressed()
        if keys[pygame.K_ESCAPE]:
            quit_game()
        

while True:
    clock.tick(settings.FPS)
    check_events()
    if pygame.key.get_pressed()[pygame.K_SPACE]:
        break
    window.fill((0, 0, 0))
    window.blit(snake, (size[0] / 2 - ssize[0] / 2, size[1] / 2 - ssize[1] / 2))
    window.blit(start, (size[0] / 2 - stsize[0] / 2, 50 + size[1] / 2 - stsize[1] / 2))
    pygame.display.update()

while True:

    import basic
    game = basic.Game(window, game_settings=game_settings)
    game.playing = True
    game.run()

    if game.score < game.maxscore:
        snake = font.render("GAME OVER", 0, settings.RED)
        ssize = font.size("GAME OVER")
    else:
        snake = font.render("YOU WIN!", 0, settings.LIME)
        ssize = font.size("YOU WIN!")

    start = font2.render("Score: " + str(game.score), 0, (255, 255, 255))
    stsize = font2.size("Score: " + str(game.score))

    while True:
        clock.tick(settings.FPS)
        check_events()
        if pygame.key.get_pressed()[pygame.K_SPACE]:
            break
        window.fill((0, 0, 0))
        window.blit(snake, (size[0] / 2 - ssize[0] / 2, size[1] / 2 - ssize[1] / 2))
        window.blit(start, (size[0] / 2 - stsize[0] / 2, 50 + size[1] / 2 - stsize[1] / 2))
        pygame.display.update()

quit_game()