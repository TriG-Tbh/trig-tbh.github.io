import pygame
import sys
pygame.init()
clo_obj=pygame.time.Clock()

path = r"[REDACTED]"

movie=pygame.movie.Movie("movie_sample.mpg")
sur_obj=pygame.display.set_mode(movie.get_size())
mov_scre=pygame.Surface(movie.get_size()).convert()
movie.set_display(mov_scre)
movie.play()
while True:
    for eve in pygame.event.get():
        if eve==pygame.QUIT:
            movie.stop()
            pygame.quit()
            sys.exit()
    sur_obj.blit(mov_scre,(0,0))
    pygame.display.update()
    clo_obj.tick(60)