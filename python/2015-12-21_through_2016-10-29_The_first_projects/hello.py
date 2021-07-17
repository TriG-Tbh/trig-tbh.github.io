import pygame
pygame.init()
window = pygame.display.set_mode((500, 400))
while True:
	pygame.draw.circle(window,(255,255,0),(250,200),20,0)
	pygame.display.update()							
