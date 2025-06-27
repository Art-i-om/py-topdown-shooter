import pygame
from settings import *


class Player:
    def __init__(self, game):
        self.game = game
        self.x, self.y = PLAYER_POS
        self.angle = 0
        self.rect = pygame.Rect(0, 0, PLAYER_SIZE, PLAYER_SIZE)
        self.max_health = MAX_PLAYER_HEALTH
        self.health = self.max_health
        self.freeze_damage = False
        self.freeze_damage_timer = 0
        self.damage_cooldown = 500
        self.last_damage_time = 0

    def draw(self):
        pygame.draw.rect(self.game.screen, GREEN, self.rect)

    def movement(self):
        dx, dy = 0, 0
        speed = PLAYER_SPEED * self.game.delta_time
        keys = pygame.key.get_pressed()
        if keys[pygame.K_w]:
            dy += -speed
        if keys[pygame.K_s]:
            dy += speed
        if keys[pygame.K_a]:
            dx += -speed
        if keys[pygame.K_d]:
            dx += speed

        self.check_wall_collision(dx, dy)
        self.rect.center = (self.x, self.y)

    def check_wall(self, x, y):
        grid_x = int(x // 100)
        grid_y = int(y // 100)
        return (grid_x, grid_y) not in self.game.map.world_map

    def check_wall_collision(self, dx, dy):
        scale = PLAYER_SIZE / (self.game.delta_time + 0.0001)
        if self.check_wall(self.x + dx * scale, self.y):
            self.x += dx
        if self.check_wall(self.x, self.y + dy * scale):
            self.y += dy

    def take_damage(self, damage):
        current_time = pygame.time.get_ticks()
        if current_time - self.last_damage_time >= self.damage_cooldown:
            self.health -= damage
            self.last_damage_time = current_time
            if self.health <= 0:
                self.health = 0
                self.die()

    def die(self):
        self.game.game_over.run()

    def update(self):
        self.movement()

    @property
    def pos(self):
        return self.x, self.y

    @property
    def map_pos(self):
        return int(self.x), int(self.y)