import pygame

class Event():
    def __init__(self):
        self.listeners = []
        self.is_running = True
        self.register(self.quit)

    def process_input(self):
        for event in pygame.event.get():
            for listener in self.listeners:
                listener(event)

    def register(self, listener):
        if listener not in self.listeners:
            self.listeners.append(listener)

    def remove(self, listener):
        if listener in self.listeners:
            self.listeners.remove(listener)

    def quit(self, event):
        if event.type == pygame.QUIT:
            self.is_running = False