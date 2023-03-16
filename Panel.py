import pygame

import setting


class Panel:
    PANELWIDTH, PANELHEIGHT = setting.PANELWIDTH, setting.SCREEN_SIZE[1]
    PANELLEFT, PANELTOP = setting.SCREEN_SIZE[0], 0

    def __init__(self, playerCount = setting.PLAYER_LIFE, totalTank = setting.TOTAL_COMPUTER_TANK):
        # 控制面板的surface
        self.panel = pygame.Surface((Panel.PANELWIDTH, Panel.PANELHEIGHT), flags = pygame.HWSURFACE)

        # 填充方块
        self.panel.fill((190, 190, 190))
        self.panelPoint = (self.PANELLEFT, Panel.PANELTOP)

        # 最多显示20个坦克图标
        self.tank_icon = pygame.image.load("res/image/tank_icon.png")
        self.tankIcon_point = (self.PANELLEFT + 10, 30)

        # 玩家图标
        self.player_icon = pygame.image.load("res/image/player_icon.png")
        self.playerIcon_point = (self.PANELLEFT + 10, Panel.PANELHEIGHT - 50)
        self.icon_points = []
        self.font = pygame.font.Font("c:/Windows/Fonts/Simhei.ttf", 20)
        self.player_count = playerCount
        self.player_count_text = self.font.render(
            str(self.player_count), True, (255, 0, 0), (190, 190, 190)
        )
        self.text_position = (Panel.PANELLEFT + 35, Panel.PANELHEIGHT - 45)
        self.reset(totalTank)

    def display(self, screen):
        screen.blit(self.panel, self.panelPoint)
        for i in range(len(self.icon_points) // 2):
            screen.blit(self.tank_icon, self.icon_points[2 * i])
            screen.blit(self.tank_icon, self.icon_points[2* i + 1])
            if len(self.icon_points) > 0 and len(self.icon_points) % 2:
                screen.blit(self.tank_icon, self.icon_points[len(self.icon_points) - 1])
            screen.blit(self.player_icon, self.playerIcon_point)
            screen.blit(self.player_count_text, self.text_position)

    def reset(self, total):
        row = total // 2 + total % 2
        for i in range(row):
            self.icon_points.append((self.tankIcon_point[0], self.tankIcon_point[1] + 20 * i))
            self.icon_points.append((self.tankIcon_point[0] + 20, self.tankIcon_point[1] + 20 * i))
        if total % 2:
            self.icon_points.pop()


    def cutDown(self, n):
        for i in range(n):
            self.icon_points.pop()

    def setPlayer(self, n):
        self.player_count = n
        self.player_count_text = self.font.render(str(self.player_count), True, (255, 0, 0), (190, 190, 190))