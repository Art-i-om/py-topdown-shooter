import pygame
from pygame import mouse
import math
from settings import *


class Bullet:
    def __init__(self, game):
        self.game = game
        self.x, self.y = game.player.x, game.player.y
        self.speed = BULLET_SPEED
        self.rect = pygame.Rect(0, 0, BULLET_SIZE, BULLET_SIZE)
        self.dir_x, self.dir_y = 0, 0
        self.alive = True

    def draw(self):
        pygame.draw.rect(self.game.screen, BLUE, self.rect)

    def update(self):
        if not self.alive:
            return
        self.move_to_mouse()
        self.check_enemy_collision()

    def check_wall(self, x, y):
        grid_x = int(x // 100)
        grid_y = int(y // 100)
        return (grid_x, grid_y) not in self.game.map.world_map

    def check_wall_collision(self, dx, dy):
        scale = BULLET_SIZE / (self.game.delta_time + 0.0001)
        if self.check_wall(self.x + dx * scale, self.y):
            self.x += dx
        else:
            self.alive = False
        if self.check_wall(self.x, self.y + dy * scale):
            self.y += dy
        else:
            self.alive = False

    def move_to_mouse(self):
        mouse_x, mouse_y = mouse.get_pos()
        dx = mouse_x - self.x
        dy = mouse_y - self.y
        distance = math.hypot(dx, dy)
        if distance <= 5:
            self.dir_x, self.dir_y = 0, 0
        else:
            self.dir_x = dx / distance
            self.dir_y = dy / distance
        speed = self.speed * self.game.delta_time
        self.check_wall_collision(self.dir_x * speed, self.dir_y * speed)
        self.rect.center = (self.x, self.y)

    def check_enemy_collision(self):
        for enemy in self.game.enemies:
            if self.rect.colliderect(enemy.rect):
                enemy.take_damage(BULLET_DAMAGE)
                self.alive = False
