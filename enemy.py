import pygame
import heapq
import math
from settings import *


class Enemy:
    def __init__(self, game, max_health=100, damage=25, pos=(0, 0)):
        self.game = game
        self.x, self.y = pos
        self.speed = ENEMY_SPEED
        self.rect = pygame.Rect(0, 0, ENEMY_SIZE, ENEMY_SIZE)
        self.max_health = max_health
        self.health = self.max_health
        self.damage = damage
        self.path = []
        self.path_index = 0
        self.recalculate_timer = 0
        self.recalculate_interval = 10  # Recalculate path every 10 frames

    def draw(self):
        pygame.draw.rect(self.game.screen, RED, self.rect)

    def update(self):
        self.move_with_pathfinding()
        self.check_player_collision()

    def check_wall(self, x, y):
        grid_x = int(x // 100)
        grid_y = int(y // 100)
        return (grid_x, grid_y) not in self.game.map.world_map

    def get_grid_pos(self, x, y):
        return int(x // 100), int(y // 100)

    def get_world_pos(self, grid_x, grid_y):
        return grid_x * 100 + 50, grid_y * 100 + 50

    def heuristic(self, pos1, pos2):
        return abs(pos1[0] - pos2[0]) + abs(pos1[1] - pos2[1])

    def get_neighbors(self, pos):
        x, y = pos
        neighbors = []
        for dx, dy in [(0, 1), (0, -1), (1, 0), (-1, 0)]:
            new_x, new_y = x + dx, y + dy
            if (new_x, new_y) not in self.game.map.world_map:
                neighbors.append((new_x, new_y))
        return neighbors

    def find_path(self, start_pos, end_pos):
        start_grid = self.get_grid_pos(start_pos[0], start_pos[1])
        end_grid = self.get_grid_pos(end_pos[0], end_pos[1])

        open_set = []
        heapq.heappush(open_set, (0, start_grid))
        came_from = {}
        g_score = {start_grid: 0}
        f_score = {start_grid: self.heuristic(start_grid, end_grid)}

        while open_set:
            current = heapq.heappop(open_set)[1]

            if current == end_grid:
                path = []
                while current in came_from:
                    world_pos = self.get_world_pos(current[0], current[1])
                    path.append(world_pos)
                    current = came_from[current]
                path.reverse()
                return path

            for neighbor in self.get_neighbors(current):
                tentative_g_score = g_score[current] + 1

                if neighbor not in g_score or tentative_g_score < g_score[neighbor]:
                    came_from[neighbor] = current
                    g_score[neighbor] = tentative_g_score
                    f_score[neighbor] = tentative_g_score + self.heuristic(neighbor, end_grid)
                    heapq.heappush(open_set, (f_score[neighbor], neighbor))

        return []

    def move_with_pathfinding(self):
        self.recalculate_timer += 1
        if self.recalculate_timer >= self.recalculate_interval or not self.path:
            player_pos = self.game.player.pos
            self.path = self.find_path((self.x, self.y), player_pos)
            self.path_index = 0
            self.recalculate_timer = 0

        if self.path and self.path_index < len(self.path):
            target_x, target_y = self.path[self.path_index]

            dx = target_x - self.x
            dy = target_y - self.y
            distance = math.sqrt(dx * dx + dy * dy)

            if distance < 20:
                self.path_index += 1
            else:
                if distance > 0:
                    dx /= distance
                    dy /= distance

                speed = self.speed * self.game.delta_time

                self.x += dx * speed
                self.y += dy * speed
        else:
            self.move_to_player_direct()

        self.rect.center = (self.x, self.y)

    def move_to_player_direct(self):
        player_x, player_y = self.game.player.pos
        dx = player_x - self.x
        dy = player_y - self.y
        distance = math.sqrt(dx * dx + dy * dy)

        if distance > 1:
            dx /= distance
            dy /= distance

        speed = self.speed * self.game.delta_time
        dx *= speed
        dy *= speed

        self.check_wall_collision(dx, dy)

    def check_wall_collision(self, dx, dy):
        scale = ENEMY_SIZE / (self.game.delta_time + 0.0001)
        if self.check_wall(self.x + dx * scale, self.y):
            self.x += dx
        if self.check_wall(self.x, self.y + dy * scale):
            self.y += dy

    def check_player_collision(self):
        player_rect = self.game.player.rect
        if self.rect.colliderect(player_rect):
            self.game.player.take_damage(self.damage)

    def take_damage(self, damage):
        self.health -= damage
        if self.health <= 0:
            self.die()

    def die(self):
        self.game.enemies.remove(self)


class Kamikaze(Enemy):
    def __init__(self, game, max_health=MAX_ENEMY_HEALTH, damage=ENEMY_DAMAGE, pos=(0, 0)):
        super().__init__(game, max_health, damage, pos)
