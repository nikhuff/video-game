import physics


class Unit():
    def __init__(self, point):
        self.point = point
        self.velocity = Velocity()
    
    def update(self):
        self.point.x += self.velocity.dx
        self.point.y += self.velocity.dy

class Character(Unit):
    def __init__(self, point):
        super(Character, self).__init__(point)

    def render(self):
        pass


if __name__ == '__main__':
    unit = Unit(Point(0,0))