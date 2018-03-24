import pygame as pg
import os
from settings import *

# set up assets
game_folder = os.path.dirname(__file__)
assets_folder = os.path.join(game_folder, "assets")

class Spritesheet(object):
    def __init__(self, filename):
        self.sheet = pg.image.load(filename).convert()

    # Load a specific image from a specific rectangle
    def image_at(self, rectangle, colorkey = None):
        rect = pg.Rect(rectangle)
        image = pg.Surface(rect.size).convert()
        image.blit(self.sheet, (0, 0), rect)
        if colorkey is not None:
            if colorkey is -1:
                colorkey = image.get_at((0,0))
            image.set_colorkey(colorkey, pg.RLEACCEL)
        return image

    # Load a whole bunch of images and return them as a list
    def images_at(self, rects, colorkey = None):
        return [self.image_at(rect, colorkey) for rect in rects]

class City:
    def __init__(self):
        self.ss = Spritesheet(os.path.join(assets_folder, "city.png"))
        self.sidewalk = self.ss.image_at(SIDEWALK_MID)

class Player(pg.sprite.Sprite):
    # player sprite
    def __init__(self, game, x, y):
        self.groups = game.all_sprites
        pg.sprite.Sprite.__init__(self, self.groups)
        self.game = game
        self.ss = Spritesheet(os.path.join(assets_folder, "./characters/ranger.png"))
        self.images_up = self.ss.images_at(UP, WHITE)
        self.images_right = self.ss.images_at(RIGHT, WHITE)
        self.images_down = self.ss.images_at(DOWN, WHITE)
        self.images_left = self.ss.images_at(LEFT, WHITE)
        self.current_frame = self.images_down
        self.image = self.current_frame[0]
        self.frame = 0
        self.draw_speed = .3
        self.rect = self.image.get_rect()
        self.x = x * TILESIZE
        self.y = y * TILESIZE
        self.dx = 0
        self.dy = 0

    def get_keys(self):
        self.dx, self.dy = 0, 0
        keys = pg.key.get_pressed()
        if keys[pg.K_LEFT] or keys[pg.K_a]:
            self.dx = -PLAYER_SPEED
        elif keys[pg.K_RIGHT] or keys[pg.K_d]:
            self.dx = PLAYER_SPEED
        elif keys[pg.K_UP] or keys[pg.K_w]:
            self.dy = -PLAYER_SPEED
        elif keys[pg.K_DOWN] or keys[pg.K_s]:
            self.dy = PLAYER_SPEED

    def check_collision(self):
        if pg.sprite.spritecollideany(self, self.game.walls):
            self.x -= self.dx * self.game.dt
            self.y -= self.dy * self.game.dt
            self.rect.center = (self.x, self.y)

    def get_direction(self):
        if self.dx > 0:
            self.current_frame = self.images_right
        elif self.dx < 0:
            self.current_frame = self.images_left
        elif self.dy > 0:
            self.current_frame = self.images_down
        elif self.dy < 0:
            self.current_frame = self.images_up

    def update(self):
        self.get_keys()
        self.x += self.dx * self.game.dt
        self.y += self.dy * self.game.dt
        self.rect.center = (self.x, self.y)
        self.check_collision()
        self.get_direction()

        if self.dx == 0 and self.dy == 0:
            self.frame = 0
        else:
            self.frame = (self.frame + self.draw_speed) % 4

        self.image = self.current_frame[int(self.frame)]

class Wall(pg.sprite.Sprite):
    def __init__(self, game, x, y):
        self.groups = game.all_sprites, game.walls
        pg.sprite.Sprite.__init__(self, self.groups)
        self.game = game
        self.image = pg.Surface((TILESIZE, TILESIZE))
        self.image.fill(GREEN)
        self.rect = self.image.get_rect()
        self.x = x
        self.y = y
        self.rect.x = x * TILESIZE
        self.rect.y = y * TILESIZE

class Sidewalk(pg.sprite.Sprite):
    def __init__(self, game, x, y):
        self.groups = game.all_sprites
        pg.sprite.Sprite.__init__(self)
        self.rect = self.image.get_rect()
        self.x = x
        self.y = y
        self.rect.x = x * TILESIZE
        self.rect.y = y * TILESIZE
