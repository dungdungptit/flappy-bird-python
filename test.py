from os import pipe
import pygame
import sys
import random
from settings import*
from enemy import*

pygame.init()
screen = pygame.display.set_mode((width, heigth))
phitieu = Shuriken(300, 400, 40, 40, -1)
clock = pygame.time.Clock()

while True:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            sys.exit()
    screen.fill((30, 30, 30))
    phitieu.auto_throw()
    if phitieu.x <0 or phitieu.y < 0: phitieu.x = 1270
    phitieu.draw(screen)

    pygame.display.update()
    clock.tick(60)