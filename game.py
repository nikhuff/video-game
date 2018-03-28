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
        self.running = True
        self.load_data()
        self.text_box = TextBox(self.screen)

    def load_data(self):
        self.map = TiledMap(path.join(map_folder, 'city.tmx'))
        self.map_img = self.map.make_map()
        self.map_rect = self.map_img.get_rect()

    def new(self):
        self.all_sprites = pg.sprite.Group()
        self.walls = pg.sprite.Group()
        # for row, tiles in enumerate(self.map.data):
        #     for col, tile in enumerate(tiles):
        #         if tile == '1':
        #             Wall(self, col, row)
        #         if tile == 'P':
        #             self.player = Player(self, col, row)
        for tile_object in self.map.tmxdata.objects:
            if tile_object.name == 'player':
                self.player = Player(self, tile_object.x, tile_object.y)
            if tile_object.name == 'building':
                Obstacle(self, tile_object.x, tile_object.y,
                         tile_object.width, tile_object.height)
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

    def draw(self):
        # self.screen.fill(DARKGREY)
        self.screen.blit(self.map_img, self.camera.apply_rect(self.map_rect))
        for sprite in self.all_sprites:
            self.screen.blit(sprite.image, self.camera.apply(sprite))
        self.text_box.render()
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