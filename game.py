import pygame as pg
import sys
from os import path

from settings import *
from graphics import *
from unit import *
import audio

class Game:
    def __init__(self):
        pg.init()
        pg.mixer.init()
        self.screen = pg.display.set_mode((WIDTH, HEIGHT))
        pg.display.set_caption(TITLE)
        self.clock = pg.time.Clock()
        pg.key.set_repeat(500, 100)
        self.running = True

    def load_data(self):
        game_folder = path.dirname(__file__)
        self.map = Map(path.join(game_folder, 'map2.txt'))

    def new(self):
        self.load_data()
        self.all_sprites = pg.sprite.Group()
        self.walls = pg.sprite.Group()
        for row, tiles in enumerate(self.map.data):
            for col, tile in enumerate(tiles):
                if tile == '1':
                    Wall(self, col, row)
                if tile == 'P':
                    self.player = Player(self, col, row)

        self.camera = Camera(self.map.width, self.map.height)
        
    def run(self):
        self.playing = True
        while self.playing:
            self.dt = self.clock.tick(FPS) / 1000
            self.events()
            self.update()
            self.draw()
            
    def update(self):
        self.all_sprites.update()
        self.camera.update(self.player)
    
    def events(self):
        for event in pg.event.get():
            # check for closing window
            if event.type == pg.QUIT:
                self.quit()
            if event.type == pg.KEYDOWN:
                if event.key == pg.K_ESCAPE:
                    self.quit()
    
    def draw_grid(self):
        for x in range(0, WIDTH, TILESIZE):
            pg.draw.line(self.screen, LIGHTGREY, (x,0), (x,HEIGHT))
        for y in range(0, WIDTH, TILESIZE):
            pg.draw.line(self.screen, LIGHTGREY, (0,y), (WIDTH, y))

    def draw(self):
        self.screen.fill(DARKGREY)
        self.draw_grid()
        for sprite in self.all_sprites:
            self.screen.blit(sprite.image, self.camera.apply(sprite))
        pg.display.flip()
        
    def quit(self):
        if self.playing:
            self.playing = False
        self.running = False

    def show_start_screen(self):
        pass

    def show_go_screen(self):
        pass

def main():
    game = Game()
    game.show_start_screen()
    audio.city.play(-1)
    while game.running:
        game.new()
        game.run()
        game.show_go_screen()

pg.quit()

if __name__ == '__main__':
    main()