import pygame

background = None
assets = {}
renderables = []

width = 800
height = 600

class Graphics():
    def __init__(self):
        global width, height, screen, background
        pygame.display.init()
        screen = pygame.display.set_mode((width, height))
        background = self.load("./assets/800x600.png")

    def register(self, renderable):
        global renderables
        if renderable not in renderables:
            renderables.append(renderable)

    def remove(self, renderable):
        global renderables
        if renderable in renderables:
            renderables.remove(renderable)

    def render(self):
        global screen, background, renderables, width, height

        screen.fill((0, 0, 0))

        if background:
            screen.blit(background, (0, 0, width, height))

        for r in renderables:
            r.render(screen)

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