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

        # Trail system
        self.trail = []
        self.max_trail_length = 15
        self.trail_update_counter = 0
        self.trail_update_frequency = 2  # Update trail every N frames

    def draw(self):
        pygame.draw.rect(self.game.display, BLUE, self.rect)
        self.draw_trail()

    def draw_trail(self):
        for segment in self.trail:
            pygame.draw.rect(self.game.display, BLUE, segment)

    def update(self):
        if not self.alive:
            return
        self.move_to_mouse()
        self.check_enemy_collision()
        self.update_trail()

    def update_trail(self):
        if self.trail_update_counter >= self.trail_update_frequency:
            if len(self.trail) > self.max_trail_length:
                self.trail.pop(0)
            self.trail.append(self.rect.copy())
            self.trail_update_counter = 0
        self.trail_update_counter += 1

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
