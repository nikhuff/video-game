
import pygame as pg
import sys
import random
from os import path

from settings import *
from graphics import *
from unit import *
from dialogue import multiLineSurface
import audio


class Game(object):
    def __init__(self, states, start_state):
        self.done = False
        self.screen = pg.display.set_mode((WIDTH, HEIGHT))
        self.clock = pg.time.Clock()
        self.dt = self.clock.tick(FPS) / 1000
        self.states = states
        self.state_name = start_state
        self.state = self.states[self.state_name]
        self.music = audio.title.play(-1)

    def event_loop(self):
        for event in pg.event.get():
            self.state.get_event(event)

    def flip_state(self):
        current_state = self.state_name
        next_state = self.state.next_state
        self.state.done = False
        self.state_name = next_state
        persistent = self.state.persist
        self.state = self.states[self.state_name]
        self.state.startup(persistent)
        self.music.stop()
        if self.state_name == "PROLOGUE":
            self.music = audio.prologue.play(-1)
        if self.state_name == "GAMEPLAY":
            self.music = audio.city.play(-1)
        if self.state_name == "BATTLE":
            self.music = audio.battle.play(-1)
        if self.state_name == "GAMEOVER":
            self.music = audio.prologue.play(-1)

    def update(self, dt):
        if self.state.quit:
            self.done = True
        elif self.state.done:
            self.flip_state()
        self.state.update(dt)

    def draw(self):
        self.state.draw(self.screen)

    def run(self):
        while not self.done:
            dt = self.clock.tick(FPS) / 1000
            self.event_loop()
            self.update(dt)
            self.draw()
            pg.display.update()


class GameState(object):
    def __init__(self):
        self.done = False
        self.quit = False
        self.next_state = None
        self.screen_rect = pg.display.get_surface().get_rect()
        self.persist = {}
        self.font = pg.font.Font(None, 24)

    def startup(self, persistent):
        self.persist = persistent

    def get_event(self, event):
        pass

    def update(self, dt):
        pass

    def draw(self, surface):
        pass


class TitleScreen(GameState):
    def __init__(self):
        super(TitleScreen, self).__init__()
        self.title = pg.image.load('./assets/Text/Title.png')
        self.title_rect = self.title.get_rect(center=(WIDTH / 2, (HEIGHT / 2)-100))
        self.persist["screen_color"] = "black"
        self.next_state = "GAMEPLAY"
        self.options = ["New Game", "Load", "Quit"]
        self.index = 0
        self.selected = self.options[self.index]

    def get_event(self, event):
        if event.type == pg.QUIT:
            self.quit = True

        keys = pg.key.get_pressed()
        if keys[pg.K_UP]:
            audio.menu_move.play()
            self.index = (self.index - 1) % 3
            self.selected = self.options[self.index]
        elif keys[pg.K_DOWN]:
            audio.menu_move.play()
            self.index = (self.index + 1) % 3
            self.selected = self.options[self.index]
        elif keys[pg.K_z]:
            audio.menu_select.play()
            if self.selected == "New Game":
                self.next_state = "PROLOGUE"
                self.done = True
            if self.selected == "Load":
                self.next_state = "GAMEPLAY"
                self.done = True
            elif self.selected == "Quit":
                self.quit = True

    def draw(self, surface):
        surface.fill(pg.Color("black"))
        surface.blit(self.title, self.title_rect)
        for index, option in enumerate(self.options):
            line = self.font.render(option, True, pg.Color("dodgerblue"))
            line_rect = line.get_rect(center=(WIDTH / 2, HEIGHT / 2 + 50 + 20 * (index + 1)))
            surface.blit(line, line_rect)
        option_rect = pg.Rect(WIDTH / 2 - 55, HEIGHT / 2 + 45 + 20 * (self.index + 1), 10, 10)
        pg.draw.rect(surface, pg.Color("darkgreen"), option_rect)


class Prologue(GameState):
    def __init__(self):
        super(Prologue, self).__init__()
        self.prologue = [
            "Grandpa: It's been 2 weeks since Jordan disappeared.",
            "Grandpa: He went to prove his Professor is innocent,",
            "Grandpa: Using our family's unique ability... SPIRIT WEAVING.",
            "Grandpa: I fear something happened to him in the city...",
            "Grandpa: Please grandson, go find your cousin.",
            "Grandpa: use SPIRIT WEAVING if you must.",
            "..."
        ]
        self.font = pg.font.Font(None, 44)
        self.textbox = pg.image.load('textbox.png')
        self.line = 0
        self.text = self.font.render(self.prologue[0], True, pg.Color("darkgreen"))
        self.title_rect = self.text.get_rect(center=(WIDTH / 2, HEIGHT / 2))
        self.persist["screen_color"] = "black"
        self.next_state = "GAMEPLAY"

    def get_event(self, event):
        if event.type == pg.QUIT:
            self.quit = True
        keys = pg.key.get_pressed()
        if keys[pg.K_z]:
            if self.line < 6:
                if self.line < 5:
                    audio.NPC_Interact.play()
                self.line += 1
                self.text = self.font.render(self.prologue[self.line], True, pg.Color("darkgreen"))
            if self.line == 5:
                audio.prologue.fadeout(3000)
            if self.line >= 6:
                audio.game_start.play()
                self.next_state = "GAMEPLAY"
                self.done = True

    def draw(self, surface):
        surface.fill(pg.Color("black"))

        surface.blit(self.text, self.title_rect)
        pg.display.flip()


class Gameplay(GameState):
    def __init__(self):
        super(Gameplay, self).__init__()
        self.textbox = pg.image.load('textbox.png')
        self.blank_textbox = pg.image.load('textbox.png')
        self.text = text
        self.map = TiledMap(path.join(map_folder, 'city.tmx'))
        self.map_img = self.map.make_map()
        self.map_rect = self.map_img.get_rect()
        self.all_sprites = pg.sprite.Group()
        self.walls = pg.sprite.Group()
        self.npcs = pg.sprite.Group()
        for tile_object in self.map.tmxdata.objects:
            if tile_object.name == 'player':
                self.player = Player(self, tile_object.x, tile_object.y)
            if tile_object.name == 'building':
                Obstacle(self, tile_object.x, tile_object.y,
                         tile_object.width, tile_object.height)
            if tile_object.name == 'npc':
                NPC(self, tile_object.x, tile_object.y, self.text)
            if tile_object.name == 'villain':
                Villain(self, tile_object.x, tile_object.y, self.text)
        self.camera = Camera(self.map.width, self.map.height)
        self.draw_debug = False
        self.hello = pg.font.SysFont(None, 45, False, False, None)

    def startup(self, persistent):
        self.persist = persistent

    def get_event(self, event):
        if event.type == pg.QUIT:
            self.quit = True
        elif event.type == pg.KEYUP:
            if event.key == pg.K_x:
                self.next_state = "TITLE"
                self.done = True
            elif event.key == pg.K_f:
                self.next_state = "BATTLE"
                self.done = True

    def update(self, dt):
        self.all_sprites.update(dt)
        self.camera.update(self.player)

    def draw(self, surface):
        # self.screen.fill(DARKGREY)
        surface.blit(self.map_img, self.camera.apply_rect(self.map_rect))
        for sprite in self.all_sprites:
            surface.blit(sprite.image, self.camera.apply(sprite))
            if self.draw_debug:
                pg.draw.rect(surface, GREEN, self.camera.apply_rect(sprite.rect), 1)
        if self.draw_debug:
            for wall in self.walls:
                pg.draw.rect(surface, GREEN, self.camera.apply_rect(wall.rect), 1)

        if self.player.is_talking:
            dest = (62, 462)
            self.text = multiLineSurface(text[0], self.hello, self.textbox, self.blank_textbox, (255, 255, 255))
            surface.blit(self.text, dest)
            # surface.blit(self.textbox, dest)
            # dest = (92,492)
            # self.text_box.render()
        pg.display.flip()


class Battle(GameState):
    def __init__(self):
        super(Battle, self).__init__()
        self.textboxy = pg.image.load('textbox.png')
        self.playerTurn = True

        self.villain = pg.image.load('villain.png')
        self.villainHealth = 100
        self.villainAttack = 20
        self.villainWillToFight = 100



        self.playerHealth = 100
        self.playerAttack = 15

        self.choices = [
            "What will you do?",
            "Attack",
            "Talk",
            "Run",
        ]
        self.choices2 = [
            "What will you do?",
            "Attack",
            "Talk",
            "Run",
        ]
        self.talks1 =[
            "Villain: I am doing this to better the city",
            "But what about Sally?",
            "But what about Sarah?",
            "But what about Susan?"
        ]
        self.talks2 =[
            "Villain: I hate children!!!",
            "But what about Jimbo?",
            "But what about Sarah?",
            "But what about Susan?"
        ]
        self.talks3 =[
            "Villain: I pooped my pants",
            "But what about Jeffrica?",
            "But what about Sarah?",
            "But what about Susan?"
        ]
        self.index = 0
        self.count = 0
        self.rand = 0
        self.choice = 1
        self.dest = 0, 0
        self.dest2 = 450, 450
        self.hello = pg.font.SysFont(None, 45, False, False, None)
        self.selected = self.choices[self.index + 1]

        self.villainHpText = self.hello.render("HP- " + str(self.villainHealth), 1, (255, 0, 0), None)
        self.playerHpText = self.hello.render(str(self.playerHealth), 1, (255, 153, 18), None)
        self.villainWillText = self.hello.render("Will to Fight- " + str(self.villainWillToFight), 1, (0, 0, 255), None)

        self.text = self.hello.render(self.choices[0], 1, (255, 153, 18), None)
        self.text2 = self.hello.render(self.choices[1], 1, (255, 153, 18), None)
        self.text3 = self.hello.render(self.choices[2], 1, (255, 153, 18), None)
        self.text4 = self.hello.render(self.choices[3], 1, (255, 153, 18), None)


        self.attChoice = 0

    def startup(self, persistent):
        self.persist = persistent
        self.choice = 1

    def get_event(self, event):
        keys = pg.key.get_pressed()
        self.playerTurn = True
        if keys[pg.K_UP]:
            audio.menu_move.play()
            self.index = ((self.index - 1) % 3)
            self.selected = self.choices[self.index + 1]
        elif keys[pg.K_DOWN]:
            audio.menu_move.play()
            self.index = ((self.index + 1) % 3)
            self.selected = self.choices[self.index + 1]
        elif keys[pg.K_z]:
            if self.selected == "Attack":
                audio.punch.play()
                self.villainHealth -= self.playerAttack
                self.villainHpText = self.hello.render("HP- " + str(self.villainHealth), 1, (255, 0, 0), None)
                self.playerTurn = False
            if self.selected == "Talk":
                self.choices = self.talks1[:]
                self.playerHealth += 15
            if self.selected == "But what about Sally?":
                self.choices = self.talks2
                self.villainWillToFight -= 35
                self.villainWillText =  self.hello.render("Will to Fight- " + str(self.villainWillToFight), 1, (0, 0, 255), None)
                self.playerTurn = False

            if self.selected != "But what about Sally?":
                self.villainWillText =  self.hello.render("Will to Fight- " + str(self.villainWillToFight), 1, (0, 0, 255), None)
                self.playerTurn = False
            if self.selected == "But what about Jimbo?":
                self.choices = self.talks3
                self.villainWillToFight -= 35
                self.villainWillText = self.hello.render("Will to Fight- " + str(self.villainWillToFight), 1,
                                                         (0, 0, 255), None)
                self.playerTurn = False

            if self.selected != "But what about Jimbo?":
                self.villainWillText = self.hello.render("Will to Fight- " + str(self.villainWillToFight), 1,
                                                         (0, 0, 255), None)
                self.playerTurn = False

            if self.selected == "But what about Jeffrica?":
                self.choices = self.talks3
                self.villainWillToFight -= 35
                self.villainWillText = self.hello.render("Will to Fight- " + str(self.villainWillToFight), 1,
                                                         (0, 0, 255), None)
                self.playerTurn = False

            if self.selected != "But what about Jeffrica?":
                self.villainWillText = self.hello.render("Will to Fight- " + str(self.villainWillToFight), 1,
                                                         (0, 0, 255), None)
                self.playerTurn = False


            elif self.selected == "Run":
                self.rand = random.randrange(1, 3)
                if self.rand == 1:
                    self.choices[0] = "You are a pansy and tried to run away....you failed"
                    self.playerTurn = False
                else:
                    self.choices[0] = "you manage to run fast enough to escape"
                    if keys[pg.K_z]:
                        self.choices = self.choices2[:]
                        self.next_state = "GAMEPLAY"
                        self.done = True


        if self.playerTurn == False:
            self.playerHealth -= 15
            self.playerHpText = self.hello.render(str(self.playerHealth), 1, (255, 153, 18),None)

        if self.villainHealth <= 0:
            self.next_state = "GAMEPLAY"
            self.done = True

        if self.villainWillToFight <= 0:
            self.next_state = "GAMEPLAY"
            self.done = True

        if self.playerHealth <= 0:
            self.next_state = "GAMEOVER"
            self.done = True



#MICAH"S HARD WORK
        if event.type == pg.QUIT:
            self.quit = True
        elif event.type == pg.KEYDOWN:
            keys = pg.key.get_pressed()
            if keys[pg.K_a]:
                self.choice = 2

                if event.type == pg.KEYDOWN:
                    keys2 = pg.key.get_pressed()

                    if keys2[pg.K_q]:
                        self.attChoice = 1

                    elif keys2[pg.K_w]:

                        self.attChoice = 2
                        self.villainHealth -= self.playerAttack
                        self.villainHpText = self.hello.render(str(self.villainHealth), 1, (255, 153, 18), None)

                    elif keys2[pg.K_e]:
                        self.attChoice = 3
                        self.villainHealth -= self.playerAttack
                        self.villainHpText = self.hello.render(str(self.villainHealth), 1, (255, 153, 18), None)

            elif keys[pg.K_s]:
                self.choice = 3

                if event.type == pg.KEYDOWN:
                    keys2 = pg.key.get_pressed()

                    if keys2[pg.K_q]:
                        self.attChoice = 1
                        print("You done insult me!")

                    elif keys2[pg.K_w]:

                        self.attChoice = 2
                        print("You done compliment me!")

                    elif keys2[pg.K_e]:
                        self.attChoice = 3
                        print("You done meh meh me!")

            elif keys[pg.K_d]:
                self.choice = 4
                self.rand = random.randrange(1, 3)


    def update(self, dt):
        if self.choice == 1:
           self.text = self.hello.render(self.choices[0], 1, (255, 153, 18), None)
           self.text2 = self.hello.render(self.choices[1], 1, (255, 153, 18), None)
           self.text3 = self.hello.render(self.choices[2], 1, (255, 153, 18), None)
           self.text4 = self.hello.render(self.choices[3], 1, (255, 153, 18), None)
        elif self.choice == 2:
           self.text = self.hello.render("Punch", 1, (255, 153, 18), None)
           self.text2 = self.hello.render("Kick", 1, (255, 153, 18), None)
           self.text3 = self.hello.render("Headbutt", 1, (255, 153, 18), None)
        elif self.choice == 3:
            self.text = self.hello.render("Insult", 1, (255, 153, 18), None)
            self.text2 = self.hello.render("Compliment", 1, (255, 153, 18), None)
            self.text3 = self.hello.render("Meh meh meh", 1, (255, 153, 18), None)
        elif self.choice == 4:

            if self.rand == 1:
                self.text = self.hello.render("You are a pansy and tried to run away....you failed", 1, (255, 153, 18),
                                              None)
            else:
                self.text = self.hello.render(
                    "with human feces lubricating your pants, you manage to run fast enough to escape", 1,
                    (255, 153, 18), None)

            if self.rand == 1:
                self.text = self.hello.render("You are a pansy and tried to run away....you failed", 1, (255, 153, 18), None)
            else:
                self.text = self.hello.render("with human feces lubricating your pants, you manage to run fast enough to escape", 1, (255, 153, 18), None)


                self.next_state = "GAMEPLAY"
                self.done = True

        if self.villainHealth <= 0 or self.villainWillToFight <= 0:
            self.next_state = "GAMEPLAY"
            self.done = True

    def draw(self, surface):
        self.count += 1

        surface.blit(self.villain, (0, 0))

        self.dest = (6,491)
        surface.blit(self.playerHpText, self.dest, area=None, special_flags=0)

        self.dest = (0, 0)
        surface.blit(self.villainHpText, self.dest, area=None, special_flags=0)

        self.dest = (150, 0)
        surface.blit(self.villainWillText, self.dest, area=None, special_flags=0)

        self.dest = 62, 462
        surface.blit(self.textboxy, self.dest, area=None, special_flags=0)
        self.dest = 92, 492
        surface.blit(self.text, self.dest)

        if self.rand != 1:
            self.dest = 102, 522
            surface.blit(self.text2, self.dest)

        if self.rand != 1:
            self.dest = 102, 552
            surface.blit(self.text3, self.dest)

        if self.rand != 1:
            self.dest = 102, 582
            surface.blit(self.text4, self.dest)
        # self.text_box.render()

        option_rect = pg.Rect(82, 532 + 30 * self.index, 10, 10)
        pg.draw.rect(surface, pg.Color("orange"), option_rect)
        pg.display.flip()



        if self.count % 22 == 0:
            surface.blit(self.villain, (0, 7))
            self.dest = 62, 462
            surface.blit(self.textboxy, self.dest, area=None, special_flags=0)
            self.dest = 92, 492
            surface.blit(self.text, self.dest)

            self.dest = (6, 491)
            surface.blit(self.playerHpText, self.dest, area=None, special_flags=0)

            self.dest = (0, 0)
            surface.blit(self.villainHpText, self.dest, area=None, special_flags=0)

            self.dest = (150, 0)
            surface.blit(self.villainWillText, self.dest, area=None, special_flags=0)

            if self.rand != 1:
                self.dest = 102, 522
                surface.blit(self.text2, self.dest)

            if self.rand != 1:
                self.dest = 102, 552
                surface.blit(self.text3, self.dest)

            if self.rand != 1:
                self.dest = 102, 582
                surface.blit(self.text4, self.dest)
            # self.text_box.render()
            pg.display.flip()
        option_rect = pg.Rect(82, 532 + 30 * self.index, 10, 10)
        pg.draw.rect(surface, pg.Color("orange"), option_rect)


class Gameover(GameState):
    def __init__(self):
        super(Gameover, self).__init__()
        self.title = pg.image.load('./assets/Text/Title.png')
        self.title_rect = self.title.get_rect(center=(WIDTH / 2, (HEIGHT / 2)-100))
        self.persist["screen_color"] = "black"
        self.next_state = "GAMEPLAY"
        self.options = ["Quit"]
        self.index = 0
        self.selected = self.options[self.index]

    def get_event(self, event):
        if event.type == pg.QUIT:
            self.quit = True

        keys = pg.key.get_pressed()
        if keys[pg.K_UP]:
            audio.menu_move.play()
            self.index = (self.index - 1) % 1
            self.selected = self.options[self.index]
        elif keys[pg.K_DOWN]:
            audio.menu_move.play()
            self.index = (self.index + 1) % 1
            self.selected = self.options[self.index]
        elif keys[pg.K_z]:
            audio.menu_select.play()
            if self.selected == "Quit":
                self.quit = True
    def draw(self, surface):
        surface.fill(pg.Color("black"))
        surface.blit(self.title, self.title_rect)
        for index, option in enumerate(self.options):
            line = self.font.render(option, True, pg.Color("dodgerblue"))
            line_rect = line.get_rect(center=(WIDTH / 2, HEIGHT / 2 + 50 + 20 * (index + 1)))
            surface.blit(line, line_rect)
        option_rect = pg.Rect(WIDTH / 2 - 55, HEIGHT / 2 + 45 + 20 * (self.index + 1), 10, 10)
        pg.draw.rect(surface, pg.Color("darkgreen"), option_rect)

if __name__ == "__main__":
    pg.init()
    pg.mixer.init()
    states = {"TITLE": TitleScreen(),
              "PROLOGUE": Prologue(),
              "GAMEPLAY": Gameplay(),
              "BATTLE": Battle(),
              "GAMEOVER": Gameover()}

    game = Game(states, "TITLE")
    game.run()
    pg.quit()
    sys.exit()
