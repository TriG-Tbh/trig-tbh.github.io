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

class Apple:
    def __init__(self, x, y):
        self.x = x
        self.y = y

class Snake:
    def __init__(self, x, y):
        self.head = Head(x, y)
        self.body = [self.head]
        self.turning = {}
        self.wraparound = []

class Head:
    def __init__(self, x, y):
        self.x = x
        self.y = y
        self.direction = (0, 0)

class Body:
    def __init__(self, x, y, direction):
        self.x = x
        self.y = y
        self.direction = direction

class Obstacle:
    def __init__(self, x, y):
        self.x = x
        self.y = y

font = pygame.font.Font(os.path.join(basedir, "forward.ttf"), 24)
score = font.render("Score:", 0, (255, 255, 255))


class Game:
    def __init__(self, window, game_settings={"apples": 1, "obstacles": 0, "wrap-around": False}):
        
        self.window = window

        w, h = pygame.display.get_surface().get_size()
        self.width = int(w / settings.PIXEL_SIZE)
        self.height = int(h / settings.PIXEL_SIZE)
        self.snake = Snake(random.randint(0, self.width - 1),  random.randint(0, self.height - 1))

        

        self.apples = []
        for _ in range(game_settings["apples"]):
            self.apples.append(Apple(random.randint(0, self.width - 1), random.randint(0, self.height - 1)))

        goahead = False
        while not goahead:
            self.apples = []
            for _ in range(game_settings["apples"]):
                self.apples.append(Apple(random.randint(0, self.width - 1), random.randint(0, self.height - 1)))
                
            if len(set([(a.x, a.y) for a in self.apples])) < game_settings["apples"]: continue
            if (self.snake.head.x, self.snake.head.y) in [(a.x, a.y) for a in self.apples]: continue
                
            
            
            goahead = True

        self.obstacles = []
        if game_settings["obstacles"] > 0:
            goahead = False
            while not goahead:
                self.obstacles = []
                for _ in range(game_settings["obstacles"]):
                    self.obstacles.append(Obstacle(random.randint(0, self.width - 1), random.randint(0, self.height - 1)))
                
                if len(set([(a.x, a.y) for a in self.obstacles])) < game_settings["obstacles"]: continue
                if (self.snake.head.x, self.snake.head.y) in [(a.x, a.y) for a in self.obstacles]: continue
                if len(set([(a.x, a.y) for a in self.obstacles]) & set([(a.x, a.y) for a in self.apples])) > 0: continue
                goahead = True
        self.size = (w, h)

        
        self.clock = pygame.time.Clock()
        self.playing = False
        self.score = 0
        self.scoretext = font.render(str(self.score), 0, settings.LIME)
        self.gs = game_settings
        self.maxscore = (w * h) - game_settings["obstacles"] - game_settings["apples"]

    def quit_game(self):
        pygame.quit()
        sys.exit()

    def check_events(self):
        for event in pygame.event.get():
            if event == pygame.QUIT:
                self.quit_game()
            keys = pygame.key.get_pressed()
            if keys[pygame.K_ESCAPE]:
                self.quit_game()
            
            if (keys[pygame.K_w] or keys[pygame.K_UP]) and self.snake.head.direction != (0, 1) and (self.snake.head.x, self.snake.head.y) not in self.snake.turning.keys():
                self.snake.head.direction = (0, -1)
                if len(self.snake.body) > 1:
                    self.snake.turning[(self.snake.head.x, self.snake.head.y)] = self.snake.head.direction
            elif (keys[pygame.K_a] or keys[pygame.K_LEFT]) and self.snake.head.direction != (1, 0) and (self.snake.head.x, self.snake.head.y) not in self.snake.turning.keys():
                self.snake.head.direction = (-1, 0)
                if len(self.snake.body) > 1:
                    self.snake.turning[(self.snake.head.x, self.snake.head.y)] = self.snake.head.direction
            elif (keys[pygame.K_s] or keys[pygame.K_DOWN]) and self.snake.head.direction != (0, -1) and (self.snake.head.x, self.snake.head.y) not in self.snake.turning.keys():
                self.snake.head.direction = (0, 1)
                if len(self.snake.body) > 1:
                    self.snake.turning[(self.snake.head.x, self.snake.head.y)] = self.snake.head.direction
            elif (keys[pygame.K_d] or keys[pygame.K_RIGHT]) and self.snake.head.direction != (-1, 0) and (self.snake.head.x, self.snake.head.y) not in self.snake.turning.keys():
                self.snake.head.direction = (1, 0)
                if len(self.snake.body) > 1:
                    self.snake.turning[(self.snake.head.x, self.snake.head.y)] = self.snake.head.direction
            
    def draw_screen(self):
        self.window.fill(settings.BLACK)

        for apple in self.apples:
            pygame.draw.rect(self.window, settings.RED, ((apple.x) * settings.PIXEL_SIZE + (settings.PIXEL_SIZE * 0.25), (apple.y) * settings.PIXEL_SIZE + (settings.PIXEL_SIZE * 0.25), settings.PIXEL_SIZE * 0.5, settings.PIXEL_SIZE * 0.5))
        
        self.update_snake()

        

        for x in range(self.width):
            xpos = settings.PIXEL_SIZE * (x) - 1
            pygame.draw.line(self.window, settings.GREY, (xpos, 0), (xpos, self.size[1]))

        for y in range(self.height):
            ypos = settings.PIXEL_SIZE * (y) - 1
            pygame.draw.line(self.window, settings.GREY, (0, ypos), (self.size[0], ypos))

        for o in self.obstacles:
            pygame.draw.rect(self.window, settings.WHITE, ((o.x) * settings.PIXEL_SIZE + (settings.PIXEL_SIZE * 0.25), (o.y) * settings.PIXEL_SIZE + (settings.PIXEL_SIZE * 0.25), settings.PIXEL_SIZE * 0.5, settings.PIXEL_SIZE * 0.5))

        self.window.blit(score, (15, 15))
        self.window.blit(self.scoretext, (125, 15))



    def update_snake(self):

        self.snake.turning = {k: v for k, v in self.snake.turning.items() if k in [(b.x, b.y) for b in self.snake.body]}

        if (self.snake.head.x, self.snake.head.y) in [(a.x, a.y) for a in self.apples]:
            lastpos = self.snake.body[-1]
            addpos = (lastpos.x - lastpos.direction[0], lastpos.y - lastpos.direction[1])
            self.snake.body.append(Body(*addpos, lastpos.direction))

            appleindex = [(a.x, a.y) for a in self.apples].index((self.snake.head.x, self.snake.head.y))

            apple = self.apples[appleindex]
            x = random.randint(0, self.width - 1)
            y = random.randint(0, self.height - 1)
            while (x, y) in [(b.x, b.y) for b in self.snake.body] or (x, y) in [(a.x, a.y) for a in self.apples] or (x, y) in [(a.x, a.y) for a in self.obstacles]:
                x = random.randint(0, self.width - 1)
                y = random.randint(0, self.height - 1)
            apple.x = x
            apple.y = y
            self.score += 1
            self.scoretext = font.render(str(self.score), 0, settings.LIME)
            



        self.snake.head.x += self.snake.head.direction[0]
        self.snake.head.y += self.snake.head.direction[1]
        
        
        for b in range(len(self.snake.body[1:])):
            bodypart = self.snake.body[1:][b]
            if (bodypart.x, bodypart.y) in self.snake.turning.keys():
                self.snake.body[b+1].direction = self.snake.turning[(bodypart.x, bodypart.y)]

        for b in range(len(self.snake.body[1:])):
            bodypart = self.snake.body[1:][b]
            self.snake.body[b+1].x += bodypart.direction[0]
            self.snake.body[b+1].y += bodypart.direction[1]
            pygame.draw.rect(self.window, settings.GREEN, (bodypart.x * settings.PIXEL_SIZE, bodypart.y * settings.PIXEL_SIZE, settings.PIXEL_SIZE, settings.PIXEL_SIZE))

        
        pygame.draw.rect(self.window, settings.LIME, (self.snake.head.x * settings.PIXEL_SIZE, self.snake.head.y * settings.PIXEL_SIZE, settings.PIXEL_SIZE, settings.PIXEL_SIZE))




    def run(self):
        while self.playing:
            self.clock.tick(settings.FPS)
            self.check_events()
            if not self.gs["wrap-around"]:
                if self.snake.head.x >= self.width or self.snake.head.x < 0:
                    self.playing = False
                    break
                if self.snake.head.y >= self.height or self.snake.head.y < 0:
                    self.playing = False
                    break
            else:
                
            self.draw_screen()
            pygame.display.update()

            #print(self.snake.head.x, self.snake.head.y, self.width, self.height)

            

            if (self.snake.head.x, self.snake.head.y) in [(b.x, b.y) for b in self.snake.body[1:]]:
                self.playing = False
                break

            if (self.snake.head.x, self.snake.head.y) in [(b.x, b.y) for b in self.obstacles]:
                self.playing = False
                break

            if self.score >= self.maxscore:
                self.playing = False
                break





