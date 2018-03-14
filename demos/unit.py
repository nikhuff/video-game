import pygame

import graphics


class unit(object):
	def __init__(self, x, y):
			self.x = x
			self.y = y
			self.frame = 0.0
			
class George(unit):
	def __init__(self, x, y):
		super(George, self).__init__(x, y)
		self.spritesheet = graphics.load("george.png")
		self.mapping = {
			"down" : [(0, 48 * i, 48 ,48) for i in range(4)],
			"left" : [(48, 48 * i, 48 ,48) for i in range(4)],
			"up"   : [(96, 48 * i, 48 ,48) for i in range(4)],
			"right": [(144, 48 * i, 48 ,48) for i in range(4)]
		}
		self.facing = "down"


		self.speed = 0
		
	def update(self):
		self.frame = (self.frame + self.speed) % 4

	def render(self, surface):
		surface.blit(self.spritesheet,
		             (self.x, self.y, 48,48),
		             self.mapping[self.facing][int(self.frame)])
					 
	def handler(self, event):
		self.speed = 0
		if event.type == pygame.KEYDOWN:
			self.speed = 0.2
			if event.key == pygame.K_UP:
				self.y -= 1
				if self.y < 0:
					self.y = 0
				self.facing = "up"
			elif event.key == pygame.K_DOWN:
				self.y += 1
				if self.y > (599 - 48):
					self.y = 599 - 48
				self.facing = "down"
			elif event.key == pygame.K_LEFT:
				self.x -= 1
				if self.x < 0:
					self.x = 0
				self.facing = "left"
			elif event.key == pygame.K_RIGHT:
				self.x += 1
				if self.x > (799 - 48):
					self.x = 799 - 48
				self.facing = "right"
