import pygame as pg
import os
import dialogue
from settings import *

speech = dialogue.Dialogue()
Sprite_list = dialogue.Sprites()

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

class Player(pg.sprite.Sprite):
    # player sprite
    def __init__(self, game, x, y):
        self.groups = game.all_sprites
        pg.sprite.Sprite.__init__(self, self.groups)
        self.game = game
        self.ss = Spritesheet(os.path.join(characters_folder, "main_character.png"))
        self.images_up = self.ss.images_at(UP, SS)
        self.images_right = self.ss.images_at(RIGHT, SS)
        self.images_down = self.ss.images_at(DOWN, SS)
        self.images_left = self.ss.images_at(LEFT, SS)
        self.current_frame = self.images_down
        self.image = self.current_frame[0]
        self.frame = 0
        self.draw_speed = .3
        self.rect = self.image.get_rect()
        self.x = x
        self.y = y
        self.dx = 0
        self.dy = 0

    def get_keys(self):
        self.dx, self.dy = 0, 0
        keys = pg.key.get_pressed()
        if keys[pg.K_LEFT]:
            self.dx = -PLAYER_SPEED
        elif keys[pg.K_RIGHT]:
            self.dx = PLAYER_SPEED
        elif keys[pg.K_UP]:
            self.dy = -PLAYER_SPEED
        elif keys[pg.K_DOWN]:
            self.dy = PLAYER_SPEED
        elif keys[pg.K_a]:
            print("Welcome to punch town, population...You!")
        elif keys[pg.K_s]:
            print("Sup my homie?")
        elif keys[pg.K_d]:
            print("Fly, you fools!")

    def get_mouse(self):
        if pg.mouse.get_pressed()[0] == True:
            x,y = pg.mouse.get_pos()
            if x > 195 and x < 310 and y > 645 and y < 685:
                print("Welcome to punch town, population...You!")
            elif x > 395 and x < 510 and y > 645 and y < 685:
                print("Sup my homie?")
            elif x > 600 and x < 715 and y > 645 and y < 685:
                print("Fly, you fools!")

    def check_collision(self):
        npc = pg.sprite.spritecollideany(self, self.game.npcs)
        if pg.sprite.spritecollideany(self, self.game.walls):
            self.x -= self.dx * self.game.dt
            self.y -= self.dy * self.game.dt
            self.rect.center = (self.x, self.y)
        if npc:
            self.x -= self.dx * self.game.dt
            self.y -= self.dy * self.game.dt
            self.rect.center = (self.x, self.y)
            keys = pg.key.get_pressed()
            if keys[pg.K_z]:
                npc.interact()

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
        self.get_mouse()
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

class NPC(pg.sprite.Sprite):
    # player sprite
    def __init__(self, game, x, y):
        self.groups = game.all_sprites, game.npcs
        pg.sprite.Sprite.__init__(self, self.groups)
        self.game = game
        self.ss = Spritesheet(os.path.join(characters_folder, Sprite_list.random_sprite()))
        self.images_up = self.ss.images_at(UP, SS)
        self.images_right = self.ss.images_at(RIGHT, SS)
        self.images_down = self.ss.images_at(DOWN, SS)
        self.images_left = self.ss.images_at(LEFT, SS)
        self.current_frame = self.images_down
        self.image = self.current_frame[0]
        self.frame = 0
        self.draw_speed = .3
        self.rect = self.image.get_rect()
        self.x = x
        self.y = y
        self.dx = 0
        self.dy = 0
        self.dialogue = "I AM ERROR"


    #function to call to generate dialogue returns a sentence for NPC to say
    def generate_dialogue(self):
        return self.dialogue

    def check_collision(self):
        if pg.sprite.spritecollideany(self, self.game.walls):
            self.x -= self.dx * self.game.dt
            self.y -= self.dy * self.game.dt
            self.rect.center = (self.x, self.y)

    def interact(self):
        self.dialogue = speech.random_sentence()
        return self.dialogue

    def bot_move(self):
        pass

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
        self.bot_move()
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

class Obstacle(pg.sprite.Sprite):
    def __init__(self, game, x, y, w, h):
        self.groups = game.walls
        pg.sprite.Sprite.__init__(self, self.groups)
        self.game = game
        self.rect = pg.Rect(x, y, w, h)
        self.x = x
        self.y = y
        self.rect.x = x
        self.rect.y = y