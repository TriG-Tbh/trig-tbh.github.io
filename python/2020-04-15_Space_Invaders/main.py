import pygame
import os
import time
import random
import settings
pygame.font.init()


def get_asset(name):
    basepath = os.path.dirname(os.path.realpath(__file__))
    return os.path.join(os.path.join(basepath, "assets"), name)


WIN = pygame.display.set_mode((settings.WIDTH, settings.HEIGHT))
pygame.display.set_caption("Space Invaders")

# Load images
RED_SPACE_SHIP = pygame.image.load(get_asset("pixel_ship_red_small.png"))
GREEN_SPACE_SHIP = pygame.image.load(get_asset("pixel_ship_green_small.png"))
BLUE_SPACE_SHIP = pygame.image.load(get_asset("pixel_ship_blue_small.png"))

# Player ship
YELLOW_SPACE_SHIP = pygame.image.load(get_asset("pixel_ship_yellow.png"))

# Lasers
RED_LASER = pygame.image.load(get_asset("pixel_laser_red.png"))
GREEN_LASER = pygame.image.load(get_asset("pixel_laser_green.png"))
BLUE_LASER = pygame.image.load(get_asset("pixel_laser_blue.png"))
YELLOW_LASER = pygame.image.load(get_asset("pixel_laser_yellow.png"))

# Background
BG = pygame.transform.scale(pygame.image.load(
    get_asset("background-black.png")), (settings.WIDTH, settings.HEIGHT))


class Laser:
    def __init__(self, x, y, img):
        self.x = x
        self.y = y
        self.img = img
        self.mask = pygame.mask.from_surface(self.img)

    def draw(self, window):
        window.blit(self.img, (self.x, self.y))

    def move(self, vel):
        self.y += vel

    def get_height(self):
        return self.img.get_height()

    def off_screen(self, height):
        return not(self.y <= height and self.y >= -self.get_height())

    def collision(self, obj):
        return collide(obj, self)


def collide(obj1, obj2):
    offset_x = obj2.x - obj1.x
    offset_y = obj2.y - obj1.y
    return obj1.mask.overlap(obj2.mask, (offset_x, offset_y)) is not None


class Ship:

    def __init__(self, x, y, health=100, cooldownlength=30):
        self.x = x
        self.y = y
        self.health = health
        self.ship_img = None
        self.laser_img = None
        self.lasers = []
        self.cool_down_counter = 0
        self.cooldownlength = cooldownlength

    def draw(self, window):
        window.blit(self.ship_img, (self.x, self.y))
        for laser in self.lasers:
            laser.draw(window)

    def move_lasers(self, vel, obj):
        self.cooldown()
        for laser in self.lasers:
            laser.move(vel)
            if laser.off_screen(settings.HEIGHT):
                self.lasers.remove(laser)
            elif laser.collision(obj):
                obj.health -= 10
                self.lasers.remove(laser)

    def get_width(self):
        return self.ship_img.get_width()

    def get_height(self):
        return self.ship_img.get_height()

    def cooldown(self):
        if self.cool_down_counter >= self.cooldownlength:
            self.cool_down_counter = 0
        elif self.cool_down_counter > 0:
            self.cool_down_counter += 1

    def shoot(self):
        if self.cool_down_counter == 0:
            laser = Laser(self.x, self.y, self.laser_img)
            self.lasers.append(laser)
            self.cool_down_counter = 1


class Player(Ship):
    def __init__(self, x, y, health=100):
        super().__init__(x, y, health, cooldownlength=15)
        self.ship_img = YELLOW_SPACE_SHIP
        self.laser_img = YELLOW_LASER
        self.mask = pygame.mask.from_surface(self.ship_img)
        self.max_health = health

    def move_lasers(self, vel, objs):
        self.cooldown()
        for laser in self.lasers:
            laser.move(vel)
            if laser.off_screen(settings.HEIGHT):
                self.lasers.remove(laser)
            else:
                for obj in objs:
                    if laser.collision(obj):
                        objs.remove(obj)
                        self.lasers.remove(laser)

    def draw(self, window):
        super().draw(window)
        self.healthbar(window)

    def healthbar(self, window):
        pygame.draw.rect(window, (255, 0, 0), (self.x, self.y +
                                               self.ship_img.get_height() + 10, self.ship_img.get_width(), 10))
        pygame.draw.rect(window, (0, 255, 0), (self.x, self.y +
                                               self.ship_img.get_height() + 10, self.ship_img.get_width() * (self.health / self.max_health), 10))


class Enemy(Ship):

    COLOR_MAP = {
        "red": (RED_SPACE_SHIP, RED_LASER),
        "green": (GREEN_SPACE_SHIP, GREEN_LASER),
        "blue": (BLUE_SPACE_SHIP, BLUE_LASER)
    }

    def __init__(self, x, y, color, health=100):
        super().__init__(x, y, health)
        self.ship_img, self.laser_img = self.COLOR_MAP[color]
        self.mask = pygame.mask.from_surface(self.ship_img)
        self.velx = random.randint(-3, 3)

    def move(self, vely):
        self.x += self.velx
        self.y += vely
        if self.x + self.get_width() < 0:
            self.x = settings.WIDTH
        if self.x > settings.WIDTH:
            self.x = -self.get_width()
        if self.y > settings.HEIGHT:
            self.y = -self.get_height()

    def shoot(self):
        if self.cool_down_counter == 0:
            laser = Laser(self.x-15, self.y, self.laser_img)
            self.lasers.append(laser)
            self.cool_down_counter = 1


def main():
    run = True
    clock = pygame.time.Clock()
    level = 0
    player = Player(300, 630)

    enemies = []
    wave_length = 5

    lost = False
    lost_count = 0

    main_font = pygame.font.SysFont("comicsans", 50)
    lost_font = pygame.font.SysFont("comicsans", 70)

    def redraw_window():
        WIN.blit(BG, (0, 0))

        # Draw text
        lives_label = main_font.render(
            f"Lives: {settings.LIVES}", 1, (255, 255, 255))
        level_label = main_font.render(
            f"Level: {level}", 1, (255, 255, 255))
        enemy_label = main_font.render(
            f"Enemies: {len(enemies)}", 1, (255, 255, 255)
        )

        for enemy in enemies:
            enemy.draw(WIN)

        player.draw(WIN)

        WIN.blit(lives_label, (10, 10))
        WIN.blit(level_label, (settings.WIDTH -
                               level_label.get_width() - 10, 10))
        WIN.blit(enemy_label, (settings.WIDTH -
                               enemy_label.get_width() - 10, 60))

        if lost:
            lost_label = lost_font.render("GAME OVER", 1, (255, 255, 255))
            WIN.blit(lost_label, (settings.WIDTH/2 - lost_label.get_width() /
                                  2, settings.HEIGHT/2 - lost_label.get_height()/2))

        pygame.display.update()

    while run:
        clock.tick(settings.FPS)

        redraw_window()

        if player.health <= 0:
            player.health = 100
            settings.LIVES -= 1

        if settings.LIVES <= 0:
            lost = True
            lost_count += 1

        if lost:
            if lost_count > settings.FPS * 5:
                run = False
            else:
                continue

        if len(enemies) == 0:
            level += 1
            wave_length += 5
            for _ in range(wave_length):
                enemy = Enemy(random.randrange(
                    50, settings.WIDTH-100), random.randrange(-1500, -100), random.choice(["red", "green", "blue"]))
                enemies.append(enemy)

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                run = False

        keys = pygame.key.get_pressed()
        if keys[pygame.K_ESCAPE]:
            run = False
        if keys[pygame.K_a] and (player.x - settings.PLAYER_VEL > 0):
            player.x -= settings.PLAYER_VEL
        if keys[pygame.K_d] and (player.x + settings.PLAYER_VEL + player.get_width() < settings.WIDTH):
            player.x += settings.PLAYER_VEL
        if keys[pygame.K_w] and (player.y - settings.PLAYER_VEL > 0):
            player.y -= settings.PLAYER_VEL
        if keys[pygame.K_s] and (player.y + settings.PLAYER_VEL + player.get_height() + 10 < settings.HEIGHT):
            player.y += settings.PLAYER_VEL
        if keys[pygame.K_SPACE]:
            player.shoot()

        for enemy in enemies[:]:
            enemy.move(settings.ENEMY_VEL)
            enemy.move_lasers(settings.LASER_VEL, player)

            if random.randrange(0, 120) == 1:
                enemy.shoot()

            if collide(enemy, player):
                player.health -= 10
                enemies.remove(enemy)

        player.move_lasers(-settings.LASER_VEL * 2, enemies)


if __name__ == "__main__":
    main()
