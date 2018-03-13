class Game:
    def __init__(self):
        pass

    def process_input(self):
        pass

    def update(self):
        pass
    
    def render(self):
        pass

    def game(self):
        while True:
            self.process_input()
            self.update()
            self.render()