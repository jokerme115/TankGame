import random

import pygame.image

from Bullet import *
from Bullet import Bullet
from SpriteObject import SpriteObject
from setting import *


class Tank(SpriteObject):
    def __init__(self, left, top):
        """
        坦克对象
        :param left: 左边距
        :param top:  上边距
        """
        super(SpriteObject, self).__init__()
        self.images = {
            'Up': pygame.image.load('res/image/tank_up.png'),
            'Down': pygame.image.load('res/image/tank_down.png'),
            'Left': pygame.image.load('res/image/tank_left.png'),
            'Right': pygame.image.load('res/image/tank_right.png')
        }

        # 坦克的初始方向
        self.stop = True
        self.direction = 'Up'
        # 当前显示的图片
        self.image = self.images[self.direction]
        # 获取图片当前的位置
        self.rect = self.image.get_rect()
        # 更改图片的位置
        self.rect.left = left
        self.rect.top = top
        self.lastLeft = self.rect.left
        self.lastTop = self.rect.top

    def display(self, screen):
        # 根据当前方向获取显示image
        self.image = self.images[self.direction]
        screen.blit(self.image, self.rect)

    def move(self):
        """
            此处修改了一下，因为向下和向右移动的时候会比其他情况多一个判断所以说速度会慢一点，
            但是由于两个对象用的同一个move因此在这里用了一个判断
        """
        self.lastLeft = self.rect.left
        self.lastTop = self.rect.top
        if self.direction == 'Left':
            if self.rect.left > 0:
                self.rect.left -= SPEED
        elif self.direction == 'Right':
            if self.rect.left + self.rect.width < SCREEN_SIZE[0]:
                self.rect.left += SPEED
        elif self.direction == 'Up':
            if self.rect.top > 0:
                self.rect.top -= SPEED
        elif self.direction == 'Down':
            if self.rect.top + self.rect.height < SCREEN_SIZE[1]:
                self.rect.top += SPEED


    def checkCollide(self, spriteObjectList):
        for obj in spriteObjectList:
            if obj and obj is not self and pygame.sprite.collide_rect(obj, self):
                self.halt()

    def checkCollideBuild(self, spriteObjectList):
        for obj in spriteObjectList:
            if obj and obj is not self and pygame.sprite.collide_rect(obj, self):
                return True
        return False


    def shot(self):
        return Bullet(self)

    def halt(self):
        self.rect.left = self.lastLeft
        self.rect.top = self.lastTop


class EnemyTank(Tank):
    def __init__(self, left, top):
        super().__init__(left, top)
        self.images = {
            'Up': pygame.image.load('res/image/entank_up.png'),
            'Down': pygame.image.load('res/image/entank_down.png'),
            'Left': pygame.image.load('res/image/entank_left.png'),
            'Right': pygame.image.load('res/image/entank_right.png')
        }
        # 初始方向
        self.direction = self.randDirection()
        # 初始步数
        self.step = STEP

    def randDirection(self):
        return ["Up", "Down", "Left", "Right"][random.randint(0, 3)]

    def randMove(self):
        if self.step <= 0:
            self.direction = self.randDirection()
            self.step = STEP
        else:
            self.move()
            self.step -= 1

    def shot(self):
        num = random.randint(1, 1000)
        if num < 10:
            return Bullet(self)