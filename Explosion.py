import pygame.image
from Tank import *
from mygame import *


class Explosion:
    images = [
        pygame.image.load("res/image/explosion-1.png"),
        pygame.image.load("res/image/explosion-2.png"),
        pygame.image.load("res/image/explosion-3.png"),
        pygame.image.load("res/image/explosion-4.png"),
        pygame.image.load("res/image/explosion-5.png")
    ]

    def __init__(self, tank):
        self.frameIndex = 0 # 爆炸图片的序号，初始为0，-1代表无效
        self.image = Explosion.images[self.frameIndex]

        rect = self.image.get_rect()
        self.rect = tank.rect
        self.rect.left = tank.rect.left - (rect.width - tank.rect.width) / 2
        self.rect.top = tank.rect.top - (rect.height - tank.rect.height) / 2

    def display(self, screen):
        if self.frameIndex < len(self.images):
            screen.blit(self.image, self.rect)
            self.image = self.images[self.frameIndex]
            self.frameIndex += 1
        else:
            self.frameIndex = -1