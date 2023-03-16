import pygame.sprite


class SpriteObject(pygame.sprite.Sprite):
    def __init__(self):
        # 调用父类(Sprite)的构造方法
        super().__init__() # 这儿不用使用self不然后面墙有问题！

        # 表示有效
        self.alive = True