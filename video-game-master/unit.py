import pygame

from physics import *
from graphics import Graphics

class Unit():
    def __init__(self, point):
        self.point = point
        self.velocity = Velocity()
        self.frame = 0.0
        self.height = 0
        self.width = 0

    def update(self):
        self.point.setx(self.point.x + self.velocity.dx, self.width)
        self.point.sety(self.point.y + self.velocity.dy, self.height)

class Character(Unit):
    def __init__(self, point):
        super(Character, self).__init__(point)
        self.spritesheet = Graphics.load("./assets/characters/george.png")
        self.mapping = self.get_mapping()
        self.height = 33
        self.width = 24
        self.facing = "down"

    def update(self):
        super(Character, self).update()
        self.frame = (self.frame + self.velocity.get_speed()) % 4
 
    def render(self, surface):
        # make sure that character is not stuck in an animated frame if he is motionless
        if self.velocity.get_speed() == 0:
            self.frame = 0
        # render the character based on his position
        surface.blit(self.spritesheet,
                     (self.point.x, self.point.y, self.width, self.height),
                     self.mapping[self.facing][int(self.frame)])

    def get_mapping(self):
        return {
            "up": [(24 * i, 0, 24, 33) for i in [1, 2, 3, 2]],
			"right": [(24 * i, 33, 24, 33) for i in [1, 2, 3, 2]],
			"down": [(24 * i, 66, 24, 33) for i in [1, 2, 3, 2]],
			"left": [(24 * i, 99, 24, 33) for i in [1, 2, 3, 2]]
        }

    def set_direction(self):
        if self.velocity.dx > 0:
            self.facing = "right"
        elif self.velocity.dx < 0:
            self.facing = "left"
        elif self.velocity.dy > 0:
            self.facing = "down"
        elif self.velocity.dy < 0:
            self.facing = "up"

    def handler(self, event):
        self.velocity.dx, self.velocity.dy = 0, 0

        if event.type == pygame.KEYDOWN:
            if (event.key == pygame.K_UP or event.key == pygame.K_RIGHT or event.key == pygame.K_DOWN or event.key == pygame.K_LEFT):
                if event.key == pygame.K_UP:
                    self.velocity.setdy(-1)
                elif event.key == pygame.K_DOWN:
                    self.velocity.setdy(1)
                elif event.key == pygame.K_LEFT:
                    self.velocity.setdx(-1)
                elif event.key == pygame.K_RIGHT:
                    self.velocity.setdx(1)

            self.set_direction()

if __name__ == '__main__':
    unit = Unit(Point(0,0))
    char = Character(Point(0,0))
