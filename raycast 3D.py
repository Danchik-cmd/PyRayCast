import pygame
import sys
from math import cos, sin, pi, floor, degrees
from time import time

caption = 'Raycasting 3D'

colors = {'WHITE': (255, 255, 255),
          'BLACK': (0, 0, 0),
          'RED': (138, 14, 14),
          'GREEN': (32, 128, 51),
          'BLUE': (0, 0, 255),
          'PURPLE': (128, 30, 135),
          'OCEAN': (14, 138, 136),
          'BROWN': (186, 114, 32),
          'ORANGE': (230, 119, 16)}

# coefficient is the ratio of the number of squares in width to width
c = 40

# game map in matrix
g_map = [[2, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1],
         [2, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 2, 0, 0, 0, 1],
         [2, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 2, 0, 0, 0, 1],
         [2, 0, 0, 0, 1, 0, 0, 0, 0, 0, 0, 1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 2, 0, 0, 0, 1],
         [2, 0, 0, 0, 1, 0, 0, 0, 0, 0, 0, 3, 0, 0, 0, 0, 0, 3, 0, 0, 0, 0, 0, 1, 0, 0, 0, 2, 0, 0, 0, 1],
         [2, 0, 0, 0, 1, 1, 1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 3, 3, 0, 0, 0, 0, 0, 0, 0, 0, 0, 2, 0, 0, 0, 1],
         [2, 0, 0, 0, 0, 0, 0, 0, 2, 2, 1, 1, 1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 2, 0, 0, 0, 1],
         [4, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 2, 0, 0, 0, 3],
         [4, 0, 0, 0, 0, 0, 3, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 3],
         [4, 3, 3, 3, 0, 0, 3, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1, 1, 0, 0, 0, 0, 0, 0, 0, 3],
         [4, 0, 0, 0, 0, 0, 3, 3, 3, 3, 0, 0, 0, 0, 0, 0, 0, 0, 0, 4, 4, 4, 1, 1, 0, 0, 0, 0, 0, 0, 0, 3],
         [4, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 3],
         [4, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 3],
         [4, 0, 0, 0, 0, 0, 2, 2, 0, 0, 0, 0, 0, 0, 0, 1, 1, 1, 0, 0, 0, 0, 4, 0, 0, 0, 0, 0, 0, 0, 0, 1],
         [4, 0, 0, 0, 0, 0, 0, 2, 2, 4, 4, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 4, 4, 4, 0, 0, 0, 0, 0, 0, 1],
         [3, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 4, 0, 0, 4, 0, 0, 0, 1],
         [3, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 4, 0, 0, 4, 0, 0, 0, 1],
         [3, 3, 3, 3, 3, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 4, 1, 1, 1, 1], ]

# screen resolution
res = (1280, 720)


class Player(object):
    # ROV - range of vision
    # LOS - line of sight
    def __init__(self, x, y, angle=1, speed=2.0, rov=400, fov=pi/3, size=4, color=colors['RED']):
        self.x = x
        self.y = y
        self.angle = angle
        self.speed = speed
        self.ROV = rov
        self.FOV = fov
        self.size = size
        self.color = color

    def move(self, game_map):
        key = pygame.key.get_pressed()

        new_x = cos(self.angle) * self.speed
        new_y = sin(self.angle) * self.speed

        # working out the sliding on the wall
        if key[pygame.K_w]:
            if not game_map[floor((self.y + new_y) / c)][floor(self.x / c)] == 0 and game_map[floor(self.y / c)][floor((self.x + new_x) / c)] == 0:
                self.x += new_x
            elif not game_map[floor(self.y / c)][floor((self.x + new_x) / c)] == 0 and game_map[floor((self.y + new_y) / c)][floor(self.x / c)] == 0:
                self.y += new_y
            elif game_map[floor((self.y + new_y) / c)][floor((self.x + new_x) / c)] == 0:
                self.x += new_x
                self.y += new_y
        if key[pygame.K_s]:
            if not game_map[floor((self.y - new_y) / c)][floor(self.x / c)] == 0 and game_map[floor(self.y / c)][floor((self.x - new_x) / c)] == 0:
                self.x -= new_x
            elif not game_map[floor(self.y / c)][floor((self.x - new_x) / c)] == 0 and game_map[floor((self.y - new_y) / c)][floor(self.x / c)] == 0:
                self.y -= new_y
            elif game_map[floor((self.y - new_y) / c)][floor((self.x - new_x) / c)] == 0:
                self.x -= new_x
                self.y -= new_y
        if key[pygame.K_d]:
            self.angle += self.speed / 40
        if key[pygame.K_a]:
            self.angle -= self.speed / 40

    def draw(self, scr):
        pygame.draw.circle(scr, self.color, (int(self.x), int(self.y)), self.size)


class Game(object):
    def __init__(self, width, height, _map, player):
        pygame.init()
        pygame.display.set_caption(caption)
        self.icon = pygame.image.load('assets/icon.ico')
        pygame.display.set_icon(self.icon)
        self.clock = pygame.time.Clock()
        self.font = pygame.font.Font(None, 36)
        self.frame_rate = 120
        self.FPS = 0
        self.width = width
        self.height = height
        self.quit = False
        self._map = _map
        self.player = player
        self.screen = pygame.display.set_mode((width, height))

    def handle_events(self):
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()

        key = pygame.key.get_pressed()

        if key[pygame.K_ESCAPE]:
            pygame.quit()
            sys.exit()
        if key[pygame.K_KP_PLUS]:
            self.player.speed += 0.1
        if key[pygame.K_KP_MINUS]:
            self.player.speed -= 0.1
        if key[pygame.K_F1]:
            pygame.image.save(self.screen, ('assets/raycast_' + str(time()) + '.jpeg'))

    def update(self):
        pygame.display.update()
        self.clock.tick(self.frame_rate)

    def show_info(self):
        pygame.draw.rect(self.screen, colors['ORANGE'], (0, 0, self.width, 60))
        pygame.draw.rect(self.screen, colors['WHITE'], (0, 0, self.width, 55))
        FPS = self.font.render('FPS: ' + str(int(self.FPS)), 1, (120, 0, 0))
        angle = self.font.render('Angle: ' + str(int(degrees(self.player.angle))), 1, (120, 0, 0))
        x = self.font.render('X: ' + str(int(self.player.x)), 1, (120, 0, 0))
        y = self.font.render('Y: ' + str(int(self.player.y)), 1, (120, 0, 0))
        control = self.font.render('+ -  change speed     W S A D - control', 1, (120, 0, 0))
        speed = self.font.render('speed: ' + str(int(self.player.speed // 1)) + '.' + str(int(self.player.speed % 1 * 10)), 1, (120, 0, 0))
        self.screen.blit(FPS, (10, 10))
        self.screen.blit(angle, (140, 10))
        self.screen.blit(x, (300, 10))
        self.screen.blit(y, (400, 10))
        self.screen.blit(speed, (500, 10))
        self.screen.blit(control, (750, 10))

    def draw_map(self):
        for i in range(self.height // c):
            for j in range(self.width // c):
                if not self._map[i][j] == 0:
                    pygame.draw.rect(self.screen, colors['BLACK'], (j * c, i * c, c, c))
                else:
                    pygame.draw.rect(self.screen, colors['BLACK'], (j * c, i * c, c, c), 1)

    def draw_ceil(self):
        for y in range(0, self.height // 2):
            per = 1 - y / (self.height / 2)
            color = (colors['PURPLE'][0] * per, colors['PURPLE'][1] * per, colors['PURPLE'][2] * per)
            pygame.draw.line(self.screen, color, (0, y), (self.width, y), 4)

    def draw_floor(self):
        for y in range(self.height // 2, self.height + 1, 4):
            per = (y - self.height / 2) / (self.height / 2)
            color = (colors['BROWN'][0] * per, colors['BROWN'][1] * per, colors['BROWN'][2] * per)
            pygame.draw.line(self.screen, color, (0, y), (self.width, y), 4)

    def draw_column(self, ray, x):
        ray.length *= cos(ray.vec.angle - self.player.angle)
        y1 = int(self.height / 2 * (1 - 50 / ray.length))
        y2 = int(self.height / 2 * (1 + 50 / ray.length))

        per = 1 - ray.length / self.player.ROV

        if self._map[ray.stepY][ray.stepX] == 1:
            color = (colors['WHITE'][0] * per, colors['WHITE'][1] * per, colors['WHITE'][2] * per)
            pygame.draw.line(self.screen, color, (x, y1), (x, y2), 8)
        elif self._map[ray.stepY][ray.stepX] == 2:
            color = (colors['GREEN'][0] * per, colors['GREEN'][1] * per, colors['GREEN'][2] * per)
            pygame.draw.line(self.screen, color, (x, y1), (x, y2), 8)
        elif self._map[ray.stepY][ray.stepX] == 3:
            color = (colors['RED'][0] * per, colors['RED'][1] * per, colors['RED'][2] * per)
            pygame.draw.line(self.screen, color, (x, y1), (x, y2), 8)
        elif self._map[ray.stepY][ray.stepX] == 4:
            color = (colors['OCEAN'][0] * per, colors['OCEAN'][1] * per, colors['OCEAN'][2] * per)
            pygame.draw.line(self.screen, color, (x, y1), (x, y2), 8)
        else:
            color = colors['BLACK']
            pygame.draw.line(self.screen, color, (x, y1), (x, y2), 8)

    def raycast(self):
        column = 0
        while column <= self.width:
            a = (column * self.player.FOV) / 1280 - self.player.FOV / 2
            vec = Vector(2, self.player.angle + a)
            ray = Ray(self.player.x, self.player.y, vec)
            ray.cast(self._map, self.player.ROV)
            # ray.draw(self.player, self.screen)
            self.draw_column(ray, column)
            column += 8

    def run(self):
        while not self.quit:
            start = time()
            self.handle_events()
            # self.screen.fill(colors['WHITE'])
            self.player.move(self._map)
            # self.draw_map()
            self.draw_ceil()
            self.draw_floor()
            self.raycast()
            # self.player.draw(self.screen)
            self.show_info()
            self.update()
            self.FPS = 1 / (time() - start)


# each ray has its vector along which it moves
class Vector(object):
    def __init__(self, length, angle):
        self.length = length
        self.angle = angle
        self.x = self.length * cos(self.angle)
        self.y = self.length * sin(self.angle)


class Ray(object):
    def __init__(self, x, y, vec):
        self.x = x
        self.y = y
        self.stepX = int(self.x / c)
        self.stepY = int(self.y / c)
        self.vec = vec
        self.length = 0

    def cast(self, _map, max_length):
        while _map[self.stepY][self.stepX] == 0 and self.length <= max_length - self.vec.length:
            self.x += self.vec.x
            self.y += self.vec.y

            self.length += self.vec.length

            self.stepX = int(self.x / c)
            self.stepY = int(self.y / c)

    def draw(self, player, scr):
        pygame.draw.line(scr, colors['PURPLE'], (player.x, player.y), (self.x, self.y), 2)


Danchik = Player(100, 100)
raycast = Game(res[0], res[1], g_map, Danchik)


if __name__ == "__main__":
    raycast.run()