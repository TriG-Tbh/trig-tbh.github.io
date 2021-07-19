import pygame

from network import Network
from player import Player

width = 500
height = 500

win = pygame.display.set_mode((width, height))
pygame.display.set_caption("Client")

clientnumber = 0





def redrawwindow(win, player, player2):
    win.fill((255, 255, 255))
    player.draw(win)
    player2.draw(win)
    pygame.display.update()



def main():
    run = True
    n = Network()
    p = n.getp()
    clock = pygame.time.Clock()
    while run:
        clock.tick(60)
        p2 = n.send(p)
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                run = False
                import sys
                sys.exit(0)
        p.move()
        redrawwindow(win, p, p2)


if __name__ == "__main__":
    try:
        main()
    except:
        import sys
        sys.exit(0)
