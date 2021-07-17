import pygame, sys, random
import pygame.locals as GAME_GLOBALS
import pygame.event as GAME_EVENTS
import pygame.time as GAME_TIME

pygame.init()
title_image = pygame.image.load('assets/title.jpg')
game_over_image = pygame.image.load('assets/game_over.jpg')
windowWidth = 400
windowHeight = 600
surface = pygame.display.set_mode((windowWidth,
windowHeight))
pygame.display.set_caption('Drop!')
leftDown = False
rightDown = False
gameStarted = False
gameEnded = False
gamePlatforms = []
platformSpeed = 3
platformDelay = 2000
lastPlatform = 0
platformsDroppedThrough = -1
dropping = False
gameBeganAt = 0
timer = 0
player = {
	'x' : windowWidth / 2,
	'y' : 0,
	'height' : 25,
	'width' : 10,
	'vy' : 5
}

