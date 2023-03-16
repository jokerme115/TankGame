import sys

import pygame.mixer

from Panel import Panel
from Tank import *
from Bullet import *
from setting import *
from Wall import *

class TankGame:
    def __init__(self):
        # 这儿之所以把部分成员变量分开，是为了之后的重启游戏！
        self.window = None
        self.playerBGM = None       # 添加背景音乐
        self.fireBGM = None         # 开火声音
        self.init()


    def init(self):
        self.computerTankCount = TOTAL_COMPUTER_TANK
        self.playerLife = PLAYER_LIFE

        self.playerTank = None  # 玩家坦克数量
        self.computerTankList = []  # 电脑坦克
        self.playerBullets = []  # 玩家子弹
        self.computerBullets = []  # 电脑子弹
        self.explosionList = []  # 爆炸效果

        self.Panel = None  # 面板
        self.wallList = []  # 墙

    # 初始化坦克的位置
    def initPlayerTank(self):
        self.playerTank = Tank(400, 500)
        # 此处有一个bug不能在这里播放音乐！

    # 显示坦克
    def displayPlayerTank(self):
        if self.playerTank and self.playerTank.alive:
            self.playerTank.display(self.window)
            if self.playerTank and not self.playerTank.stop:
                self.playerTank.move()
            self.playerTank.checkCollide(self.computerTankList)
            self.playerTank.checkCollide(self.wallList)
        elif self.playerTank:
            self.playerTank = None
            self.playerLife -= 1
            self.Panel.setPlayer(self.playerLife)

    # 显示玩家子弹
    def displayPlayerBullet(self):
        for bullet in self.playerBullets[:]:
            if bullet.alive:
                bullet.display(self.window)
                bullet.move()
                bullet.checkWallCollide(self.wallList)
                elist = bullet.checkTankCollide(self.computerTankList)
                if len(elist) > 0:
                    self.explosionList.extend(elist)
            else:
                self.playerBullets.remove(bullet)

    # 显示电脑坦克
    def displayComputerTank(self):
        for tank in self.computerTankList:
            if tank.alive:
                tank.display(self.window)
                tank.randMove()
                bullet = tank.shot()
                if bullet:
                    self.computerBullets.append(bullet)
                tank.checkCollide([self.playerTank])
                tank.checkCollide(self.computerTankList)
                tank.checkCollide(self.wallList)
            else:
                self.computerTankList.remove(tank)
                self.Panel.cutDown(1)
                self.computerTankCount -= 1
                if COMPUTER_TANK <= self.computerTankCount:
                    self.initComputerTanks(1)

    # 显示电脑子弹
    def displayComputerBullet(self):
        for bullet in self.computerBullets[:]:
            if bullet.alive:
                bullet.display(self.window)
                bullet.move()
                bullet.checkWallCollide(self.wallList)
                elist = bullet.checkTankCollide([self.playerTank])
                if len(elist) > 0:
                    self.explosionList.extend(elist)
            else:
                self.computerBullets.remove(bullet)

    # 初始化坦克位置
    def initComputerTanks(self, n):
        # 这样初始化有一个不好的地方，很多的坦克会重叠在一起

        # for i in range(n):
        #     left = random.randint(0, 600)
        #     top = random.randint(0, 200)
        #     e = EnemyTank(left, top)
        #     self.computerTankList.append(e)

        cont = 0
        while cont < n:
            left = random.randint(0, 600)
            top = random.randint(0, 200)
            e = EnemyTank(left, top)
            if not e.checkCollideBuild(self.computerTankList): # 这儿这个方法是我重新写的，原文是碰撞就停，这儿是返回一个True
                self.computerTankList.append(e)
                cont += 1

    # 显示爆炸效果
    def displayExplosion(self):
        for explosion in self.explosionList[:]:
            if explosion.frameIndex >= 0:
                explosion.display(self.window)
            else:
                self.explosionList.remove(explosion)

    # 初始化墙体
    def initWall(self):
        for i in range(1, 6): # 修改这可以修改墙的个数
            wall = Wall(130 * i , 240)
            self.wallList.append(wall)

    def displayWalls(self):
        for wall in self.wallList[:]:
            if wall.alive:
                wall.display(self.window)
            else:
                self.wallList.remove(wall)

    # 程序结束的操作
    def gameover(self):
        if (self.playerTank is None and self.playerLife == 0) or (len(self.computerTankList) == 0 and self.computerTankCount == 0):
            if self.resetGame():
                self.init()
                self.Panel = Panel()
                self.initComputerTanks(COMPUTER_TANK if self.computerTankCount > COMPUTER_TANK else self.computerTankCount)
                self.initWall()
                self.initPlayerTank()
                return False
            return True
        return False

    # 进入结束画面
    def resetGame(self):
        if self.playerLife == 0:
            over_image = pygame.image.load("res/image/gameover.gif")
        else:
            over_image = pygame.image.load("res/image/youwin.gif")
        over_image_rect = over_image.get_rect()
        over_image_rect.left = SCREEN_SIZE[0] / 2 - over_image_rect.width / 2
        over_image_rect.top = SCREEN_SIZE[1] / 2 - over_image_rect.height  # 字体显示
        font = pygame.font.SysFont(' SimHei ', 25)
        text1_render = font.render(' Press <R> to restart the game. ', True, (85, 65,0))
        text2_render = font.render(' Press <Esc> to quit the game. ', True,(85, 65, 0))
        text1_rect = text1_render.get_rect()
        text2_rect = text2_render.get_rect()
        text1_rect.left, text1_rect.top = (SCREEN_SIZE[0] / 2 - text1_rect.width / 2, over_image_rect.top + over_image_rect.height)
        text2_rect.left, text2_rect.top = (SCREEN_SIZE[0] / 2 - text2_rect.width / 2, text1_rect.top + 30)

        while True:
            self.window.fill(BG_COLOR)
            self.window.blits(((over_image, over_image_rect), (text1_render, text1_rect), (text2_render, text2_rect)))

        # 获取事件
            eventList = pygame.event.get()
            for event in eventList:
                if event.type == pygame.QUIT:
                    self.exit()
                if event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_ESCAPE:
                        return False
                    elif event.key == pygame.K_r:
                        return True
            pygame.display.update()

    # 主进程
    def eventProcess(self):
        events = pygame.event.get()

        for event in events:
            if event.type == pygame.QUIT:
                self.exit()
            if event.type == pygame.KEYDOWN:
                if self.playerTank:
                    if event.key in (pygame.K_LEFT, pygame.K_RIGHT, pygame.K_UP, pygame.K_DOWN):
                        self.playerTank.stop = False
                    if event.key == pygame.K_DOWN:
                        self.playerTank.direction = 'Down'
                    elif event.key == pygame.K_UP:
                        self.playerTank.direction = 'Up'
                    elif event.key == pygame.K_LEFT:
                        self.playerTank.direction = 'Left'
                    elif event.key == pygame.K_RIGHT:
                        self.playerTank.direction = 'Right'
                    elif event.key == pygame.K_SPACE:
                        if len(self.playerBullets) < PLAYER_SHOT_LIMIT or PLAYER_SHOT_LIMIT < 0:
                            self.playerBullets.append(self.playerTank.shot())
                            self.fireBGM.play()
                elif event.key == pygame.K_r:
                    if self.playerTank is None and self.playerLife > 0:
                        self.initPlayerTank()
            if event.type == pygame.KEYUP:
                if self.playerTank and event.key in (pygame.K_LEFT, pygame.K_RIGHT, pygame.K_UP, pygame.K_DOWN):
                    self.playerTank.stop = True

    # 程序主程序
    def run(self):
        pygame.init()
        pygame.mixer.init()

        self.playerBGM = pygame.mixer.Sound(START_MUSIC)
        self.fireBGM = pygame.mixer.Sound(FIRE_MUSIC)

        # 设置窗口大小
        self.window = pygame.display.set_mode((SCREEN_SIZE[0] + PANELWIDTH, SCREEN_SIZE[1]))
        self.Panel = Panel()                    # 创建面板对象
        self.initPlayerTank()                   # 新增一个坦克
        pygame.display.set_caption("TankGame")  # 设置标题
        self.initWall()

        self.initComputerTanks(COMPUTER_TANK if self.computerTankCount > COMPUTER_TANK\
                               else self.computerTankCount)
        clock = pygame.time.Clock()
        self.playerBGM.play()

        while True:

            # 窗口填色
            self.window.fill(BG_COLOR)
            self.displayWalls()
            self.displayPlayerTank()
            self.displayComputerTank()
            self.displayExplosion()
            self.displayPlayerBullet()
            self.displayComputerBullet()
            self.eventProcess()
            self.Panel.display(self.window)
            if self.gameover():
                break
            # 获取事件, 判断是否退出

            pygame.display.update()
            clock.tick(FPS)

    @staticmethod
    def exit():
        pygame.quit()  # 卸载所有模块
        sys.exit()  # 终止程序

if __name__ == '__main__':
    TankGame().run()
