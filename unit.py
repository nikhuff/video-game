import pygame as pg
import os
import random
import dialogue
import audio
from settings import *

speech = dialogue.Dialogue()
Sprite_list = dialogue.Sprites()
# text = pg.Surface((1, 1))
text = [""]

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
        self.is_talking = False
        self.can_interact = True
        self.time_elapsed = 0

    def get_keys(self):
        self.dx, self.dy = 0, 0
        keys = pg.key.get_pressed()
        if self.is_talking and self.can_interact:
            if keys[pg.K_z]:
                self.is_talking = False
        else:
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

    def check_collision(self, dt):
        npc = pg.sprite.spritecollideany(self, self.game.npcs)
        if pg.sprite.spritecollideany(self, self.game.walls):
            self.x -= self.dx * dt
            self.y -= self.dy * dt
            self.rect.center = (self.x, self.y)
        if npc:
            self.x -= self.dx * dt
            self.y -= self.dy * dt
            self.rect.center = (self.x, self.y)
            keys = pg.key.get_pressed()
            if keys[pg.K_z]:
                if self.can_interact:
                    npc.interact()
                    self.is_talking = True
                    self.can_interact = False
            npc.x -= npc.dx * dt
            npc.y -= npc.dy * dt
            npc.dx = 0
            npc.dy = 0

    def get_direction(self):
        if self.dx > 0:
            self.current_frame = self.images_right
        elif self.dx < 0:
            self.current_frame = self.images_left
        elif self.dy > 0:
            self.current_frame = self.images_down
        elif self.dy < 0:
            self.current_frame = self.images_up

    def update(self, dt):
        self.get_keys()
        self.get_mouse()
        self.x += self.dx * dt
        self.y += self.dy * dt
        self.rect.center = (self.x, self.y)
        self.check_collision(dt)
        self.get_direction()

        if self.dx == 0 and self.dy == 0:
            self.frame = 0
        else:
            self.frame = (self.frame + self.draw_speed) % 4

        self.image = self.current_frame[int(self.frame)]

        if not self.can_interact:
            self.time_elapsed += 1
            if self.time_elapsed > 10:
                self.can_interact = True
                self.time_elapsed = 0


class NPC(pg.sprite.Sprite):
    # player sprite
    def __init__(self, game, x, y, text):
        self.text = text
        self.groups = game.all_sprites, game.npcs
        pg.sprite.Sprite.__init__(self, self.groups)
        self.screen = pg.display.set_mode((1024, 768))
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
        self.count = 0
        self.hello = pg.font.SysFont(None, 45, False, False, None)

    # function to call to generate dialogue returns a sentence for NPC to say
    def generate_dialogue(self):
        self.dialogue = speech.random_sentence()

    def check_collision(self, dt):
        if pg.sprite.spritecollideany(self, self.game.walls):
            self.dx *= -1
            self.dy *= -1
            self.rect.center = (self.x, self.y)

    def interact(self):
        audio.NPC_Interact.play()
        global text
        self.generate_dialogue()
        # text = self.hello.render(self.dialogue, 1, (255, 153, 18), None)
        text[0] = self.dialogue
        print(self.dialogue)

    def bot_move(self):
        self.dx = 0
        self.dy = 0
        movement = 50
        direction = random.randint(0,8)
        if direction == 0:
            self.dx -= movement
        if direction == 1:
            self.dx += movement
        if direction == 2:
            self.dy -= movement
        if direction == 3:
            self.dx += movement
        if direction >= 4:
            self.dx = 0
            self.dy = 0

    def get_direction(self):
        if self.dx > 0:
            self.current_frame = self.images_right
        elif self.dx < 0:
            self.current_frame = self.images_left
        elif self.dy > 0:
            self.current_frame = self.images_down
        elif self.dy < 0:
            self.current_frame = self.images_up

    def update(self, dt):
        self.count += 1
        if self.count == 1:
            self.bot_move()
        self.x += self.dx * dt
        self.y += self.dy * dt
        self.rect.center = (self.x, self.y)
        self.check_collision(dt)
        self.get_direction()
        if self.count == 80:
            self.count = 0

        if self.dx == 0 and self.dy == 0:
            self.frame = 0
        else:
            self.frame = (self.frame + self.draw_speed) % 4

        self.image = self.current_frame[int(self.frame)]


class Villain (pg.sprite.Sprite):
    # player sprite
    def __init__(self, game, x, y, text):
        self.text = text
        self.groups = game.all_sprites, game.npcs
        pg.sprite.Sprite.__init__(self, self.groups)
        self.screen = pg.display.set_mode((1024, 768))
        self.game = game
        self.ss = Spritesheet(os.path.join(characters_folder, "villain.png"))
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
        self.count = 0
        self.hello = pg.font.SysFont(None, 45, False, False, None)

    # function to call to generate dialogue returns a sentence for NPC to say
    def generate_dialogue(self):
        self.dialogue = speech.villain_speech()

    def check_collision(self, dt):
        if pg.sprite.spritecollideany(self, self.game.walls):
            self.dx *= -1
            self.dy *= -1
            self.rect.center = (self.x, self.y)

    def interact(self):
        audio.NPC_Interact.play()
        global text
        self.generate_dialogue()
        # text = self.hello.render(self.dialogue, 1, (255, 153, 18), None)
        text[0] = self.dialogue
        print(self.dialogue)

    def bot_move(self):
        self.dx = 0
        self.dy = 0
        movement = 50
        direction = random.randint(0, 4)
        if direction == 0:
            self.current_frame = self.images_right
        if direction == 1:
            self.current_frame = self.images_left
        if direction == 2:
            self.current_frame = self.images_down
        if direction == 3:
            self.current_frame = self.images_up
        if direction >= 4:
            self.dx = 0
            self.dy = 0

    def get_direction(self):
        if self.dx > 0:
            self.current_frame = self.images_right
        elif self.dx < 0:
            self.current_frame = self.images_left
        elif self.dy > 0:
            self.current_frame = self.images_down
        elif self.dy < 0:
            self.current_frame = self.images_up

    def update(self, dt):
        self.count += 1
        if self.count == 1:
            self.bot_move()
        self.x += self.dx * dt
        self.y += self.dy * dt
        self.rect.center = (self.x, self.y)
        self.check_collision(dt)
        self.get_direction()
        if self.count == 100:
            self.count = 0

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


