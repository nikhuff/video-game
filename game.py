import pygame as pg
import sys
from os import path

from settings import *
from graphics import *
from unit import *
import audio


class Game(object):
    """
    A single instance of this class is responsible for 
    managing which individual game state is active
    and keeping it updated. It also handles many of
    pygame's nuts and bolts (managing the event 
    queue, framerate, updating the display, etc.). 
    and its run method serves as the "game loop".
    """
    def __init__(self, states, start_state):
        """
        Initialize the Game object.
        
        screen: the pygame display surface
        states: a dict mapping state-names to GameState objects
        start_state: name of the first active game state 
        """
        self.done = False
        self.screen = pg.display.set_mode((WIDTH, HEIGHT))
        self.clock = pg.time.Clock()
        self.dt = self.clock.tick(FPS) / 1000        
        self.states = states
        self.state_name = start_state
        self.state = self.states[self.state_name]
        
    def event_loop(self):
        """Events are passed for handling to the current state."""
        for event in pg.event.get():
            self.state.get_event(event)
            
    def flip_state(self):
        """Switch to the next game state."""
        current_state = self.state_name
        next_state = self.state.next_state
        self.state.done = False
        self.state_name = next_state
        persistent = self.state.persist
        self.state = self.states[self.state_name]
        self.state.startup(persistent)
    
    def update(self, dt):
        """
        Check for state flip and update active state.
        
        dt: milliseconds since last frame
        """
        if self.state.quit:
            self.done = True
        elif self.state.done:
            self.flip_state()    
        self.state.update(dt)
        
    def draw(self):
        """Pass display surface to active state for drawing."""
        self.state.draw(self.screen)
        
    def run(self):
        """
        Pretty much the entirety of the game's runtime will be
        spent inside this while loop.
        """ 
        while not self.done:
            dt = self.clock.tick(FPS) / 1000
            self.event_loop()
            self.update(dt)
            self.draw()
            pg.display.update()
            
            
class GameState(object):
    """
    Parent class for individual game states to inherit from. 
    """
    def __init__(self):
        self.done = False
        self.quit = False
        self.next_state = None
        self.screen_rect = pg.display.get_surface().get_rect()
        self.persist = {}
        self.font = pg.font.Font(None, 24)
        
    def startup(self, persistent):
        """
        Called when a state resumes being active.
        Allows information to be passed between states.
        
        persistent: a dict passed from state to state
        """
        self.persist = persistent        
        
    def get_event(self, event):
        """
        Handle a single event passed by the Game object.
        """
        pass
        
    
    def update(self, dt):
        """
        Update the state. Called by the Game object once
        per frame. 
        
        dt: time since last frame
        """
        pass
        
    def draw(self, surface):
        """
        Draw everything to the screen.
        """
        pass
        
        
class TitleScreen(GameState):
    def __init__(self):
        super(TitleScreen, self).__init__()
        self.title = self.font.render("Spirit Weaver", True, pg.Color("dodgerblue"))
        self.title_rect = self.title.get_rect(center=(WIDTH/2, HEIGHT/2))
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
            self.index = (self.index - 1) % 3
            self.selected = self.options[self.index]            
        elif keys[pg.K_DOWN]:
            self.index = (self.index + 1) % 3
            self.selected = self.options[self.index]
        elif keys[pg.K_z]:
            if self.selected == "New Game":
                self.next_state = "GAMEPLAY"
                self.done = True
            elif self.selected == "Quit":
                self.quit = True

    
    def draw(self, surface):
        surface.fill(pg.Color("black"))
        surface.blit(self.title, self.title_rect)
        for index, option in enumerate(self.options):
            line = self.font.render(option, True, pg.Color("dodgerblue"))
            line_rect = line.get_rect(center=(WIDTH/2, HEIGHT/2 + 50 + 20 * (index + 1)))
            surface.blit(line, line_rect)
        option_rect = pg.Rect(WIDTH/2 - 55, HEIGHT/2 + 45 + 20 * (self.index + 1), 10, 10)
        pg.draw.rect(surface, pg.Color("darkgreen"), option_rect)
    
    
class Gameplay(GameState):
    def __init__(self):
        super(Gameplay, self).__init__()
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
                NPC(self, tile_object.x, tile_object.y)
        self.camera = Camera(self.map.width, self.map.height)
        self.draw_debug = False
        
    def startup(self, persistent):
        self.persist = persistent

        
    def get_event(self, event):
        if event.type == pg.QUIT:
            self.quit = True
        elif event.type == pg.KEYUP:
            if event.key == pg.K_x:
                self.next_state = "TITLE"
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
        # self.text_box.render()
        pg.display.flip()
        
    
if __name__ == "__main__":
    pg.init()
    pg.mixer.init()    
    states = {"TITLE": TitleScreen(),
              "GAMEPLAY": Gameplay(),
              "BATTLE": None}
    game = Game(states, "TITLE")
    game.run()
    pg.quit()
    sys.exit()