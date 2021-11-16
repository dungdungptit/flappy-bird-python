import pygame
shuriken = pygame.image.load('images/shur.png')

class Naruto():
    def __init__(self, x, y, width, height):
	    self.x = x
	    self.y = y
	    self.width = width
	    self.height = height 

    # vẽ naruto ra màn hình
    def draw(self, screen):
        screen.blit(pygame.image.load('images/NL1.png'), (self.x, self.y))

class Shuriken():
    def __init__(self,x,y,width,height,facing):
        self.x = x
        self.y = y
        self.width = width
        self.height = height
        self.hitbox = (self.x,self.y,40,40)

    def draw(self,win):
        win.blit(shuriken,(self.x,self.y))
        self.hitbox = (self.x,self.y,40,40)
    
    # setup tốc độ phi tiêu
    def auto_throw(self):
        self.x -= 15
        