import pygame

from Explosion import Explosion
from setting import *
from SpriteObject import SpriteObject
from Tank import *


class Bullet(SpriteObject):
    def __init__(self, tank):
        super(SpriteObject, self).__init__()
        images = {
            'Up': pygame.image.load('res/image/bullet-U.png'),
            'Down': pygame.image.load('res/image/bullet-D.png'),
            'Left': pygame.image.load('res/image/bullet-L.png'),
            'Right': pygame.image.load('res/image/bullet-R.png')
        }

        self.direction = tank.direction
        self.image = images[self.direction]
        self.rect = self.image.get_rect()

        if self.direction == "Up":
            self.rect.left = tank.rect.left + tank.rect.width / 2 - self.rect.width / 2
            self.rect.top = tank.rect.top - self.rect.height
        elif self.direction == "Down":
            self.rect.left = tank.rect.left + tank.rect.width / 2 - self.rect.width / 2
            self.rect.top = tank.rect.top + tank.rect.height
        elif self.direction == "Left":
            self.rect.left = tank.rect.left - self.rect.width
            self.rect.top = tank.rect.top +  + tank.rect.height / 2 - self.rect.height / 2
        elif self.direction == "Right":
            self.rect.left = tank.rect.left + tank.rect.width
            self.rect.top = tank.rect.top + tank.rect.height / 2 - self.rect.height / 2

        self.speed = SPEED * 2
        self.alive = True # 子弹是否有效

    def display(self, screen):
        screen.blit(self.image, self.rect)

    def move(self):
        if self.direction == 'Left':
            if self.rect.left >= 0:
                self.rect.left -= self.speed
        elif self.direction == 'Right':
            if self.rect.left + self.rect.width < SCREEN_SIZE[0]:
                self.rect.left += self.speed
        elif self.direction == 'Up':
            if self.rect.top >= 0:
                self.rect.top -= self.speed
        elif self.direction == 'Down':
            if self.rect.top + self.rect.height < SCREEN_SIZE[1]:
                self.rect.top += self.speed
        if self.rect.left < 0 or self.rect.top < 0 or self.rect.top + self.rect.height >= SCREEN_SIZE[1] or self.rect.left + self.rect.width >= SCREEN_SIZE[0]:
            self.alive = False

    def checkTankCollide(self, tankList):
        result = []
        for tank in tankList:
            if tank and pygame.sprite.collide_rect(tank, self):
                tank.alive = False
                self.alive = False
                result.append(Explosion(tank))
        return result

    def checkWallCollide(self, wallList):
        for wall in wallList:
            if pygame.sprite.collide_rect(wall, self):
                self.alive = False
                wall.life -= 1
                if wall.life <= 0:
                    wall.alive = False