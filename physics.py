from graphics import height, width

class Velocity():
    def __init__(self):
        self.dx = 0
        self.dy = 0

    def get_speed(self):
        return abs(self.dx + self.dy)

class Point():
    def __init__(self, x, y):
        self.x = x
        self.y = y

    def setx(self, x, unit_width):
        self.x = x
        if self.x < 0:
            self.x = 0
        elif self.x > width - unit_width:
            self.x = width - unit_width

    def sety(self, y, unit_height):
        self.y = y
        if self.y < 0:
            self.y = 0
        elif self.y > height - unit_height:
            self.y = height - unit_height
        