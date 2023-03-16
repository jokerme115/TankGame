import pygame.image

from SpriteObject import SpriteObject
from setting import *


class Wall(SpriteObject):
    def __init__(self, left, top):
        super().__init__()
        self.image = pygame.transform.scale(pygame.image.load("res/image/wall.png"), (50, 50))

        self.rect = self.image.get_rect()
        self.rect.left = left
        self.rect.top =  top

        self.alive = True
        self.life = WALL_LIFE

    def display(self, screen):
        screen.blit(self.image, self.rect)

