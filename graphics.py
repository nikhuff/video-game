import pygame

VIEW_RESOLUTION = width, height = [200, 200]
SCREEN_RESOLUTION = 900, 900

screen = pygame.display.set_mode(SCREEN_RESOLUTION)
assets = {}
renderables = []

import pygame as pg
import pytmx
from settings import *

class Map:
    def __init__(self, filename):
        self.data = []
        with open(filename, 'rt') as f:
            for line in f:
                self.data.append(line.strip())

        self.tilewidth = len(self.data[0])
        self.tileheight = len(self.data)
        self.width = self.tilewidth * TILESIZE
        self.height = self.tileheight * TILESIZE

class TiledMap:
    def __init__(self, filename):
        tm = pytmx.load_pygame(filename, pixelalpha=True)
        self.width = tm.width * tm.tilewidth
        self.height = tm.height * tm.tileheight
        self.tmxdata = tm
    
    def render(self, surface):
        ti = self.tmxdata.get_tile_image_by_gid
        for layer in self.tmxdata.visible_layers:
            if isinstance(layer, pytmx.TiledTileLayer):
                for x, y, gid, in layer:
                    tile = ti(gid)
                    if tile:
                        surface.blit(tile, (x * (self.tmxdata.tilewidth),
                                            y * (self.tmxdata.tileheight)))

    def make_map(self):
        temp_surface = pg.Surface((self.width, self.height))
        self.render(temp_surface)
        return temp_surface

class Camera:
    def __init__(self, width, height):
        self.camera = pg.Rect(0, 0, width, height)
        self.width = width
        self.height = height

    def apply(self, entity):
        return entity.rect.move(self.camera.topleft)

    def apply_rect(self, rect):
        return rect.move(self.camera.topleft)

    def update(self, target):
        x = -target.rect.center[0] + int(WIDTH / 2)
        y = -target.rect.center[1] + int(HEIGHT / 2)

        x = min(0, x)
        y = min(0, y)
        x = max(-(self.width - WIDTH), x)
        y = max(-(self.height - HEIGHT), y)
        self.camera = pg.Rect(x, y, self.width, self.height)
class Graphics():
    def __init__(self):
        global screen, native_screen
        pygame.display.init()
        screen = pygame.display.set_mode(SCREEN_RESOLUTION)
        native_screen = pygame.Surface(VIEW_RESOLUTION)
        
        # screen = self.load("./assets/environment/800x600.png")
        # native_screen = self.load("./assets/environment/800x600.png")

    def register(self, renderable):
        global renderables
        if renderable not in renderables:
            renderables.append(renderable)

    def remove(self, renderable):
        global renderables
        if renderable in renderables:
            renderables.remove(renderable)

    def render(self):
        global screen, native_screen, renderables, width, height

        pygame.font.init()
        # (font-None uses the default font, size, bold, italics, background-stuff that im not really sure about)
        hello = pygame.font.SysFont(None, 45, False, False, None)
        text = hello.render("Attack", 1, (255, 153, 18), None)
        text2 = hello.render("Talk", 1, (255, 153, 18), None)
        text3 = hello.render("Run", 1, (255, 153, 18), None)
        screen.blit(text, (width - 310, 650))



        screen.fill((0, 0, 255))
        native_screen.fill((255, 0, 0))

        # if background:
        #     # screen_background = pygame.transform.scale(background, (width * 7, height * 7))
        #     native_screen.blit(background, (0, 0, width, height))

        for r in renderables:
            r.render(native_screen)

        pygame.transform.scale(native_screen, SCREEN_RESOLUTION, screen)
        native_screen.blit(screen, (0, 0, width, height))

        # Text box stuff

        rect1 = pygame.Surface((115, 40))
        rect1.fill((29, 134, 206))
        pygame.Surface.set_alpha(rect1, 250)
        dest = width - 5, 645
        screen.blit(rect1, dest, area=None, special_flags=0)
        screen.blit(text, (width + 3, 650))

        rect1 = pygame.Surface((115, 40))
        rect1.fill((29, 134, 206))
        pygame.Surface.set_alpha(rect1, 250)
        dest = width + 195, 645
        screen.blit(rect1, dest, area=None, special_flags=0)
        screen.blit(text2, (width + 222, 650))

        rect1 = pygame.Surface((115, 40))
        rect1.fill((29, 134, 206))
        pygame.Surface.set_alpha(rect1, 250)
        dest = width + 400, 645
        screen.blit(rect1, dest, area=None, special_flags=0)
        screen.blit(text3, (width + 430, 650))

        pygame.display.flip()




    @staticmethod
    def load(file):
        global assets
        if file in assets:
            return assets[file]
        else:
            image = pygame.image.load(file)
            assets[file] = image
            return image
