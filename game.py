import pygame
from graphics import Graphics
from unit import Character
from physics import Point
from event import Event

class Game():
    def __init__(self):
        self.graphics = Graphics()
        self.character = Character(Point(400, 300))
        self.graphics.register(self.character)
        self.event = Event()
        self.event.register(self.character.handler)

    def process_input(self):
        self.event.process_input()

    def update(self):
        self.character.update()
    
    def render(self):
        self.graphics.render()

def main():
    game = Game()
    while game.event.is_running:
        game.process_input()
        game.update()
        game.render()

if __name__ == '__main__':
    main()