import pygame
from enemy import *
from settings import *


class ObjectRenderer:
    def __init__(self, game):
        self.game = game
        self.screen = game.screen
        self.player = game.player
        self.map = game.map

        add_enemy = self.add_enemy

        add_enemy(Kamikaze(game, pos=(HALF_WIDTH + 400, HALF_HEIGHT)))
        add_enemy(Kamikaze(game, pos=(HALF_WIDTH - 400, HALF_HEIGHT)))

    def draw(self):
        self.draw_map()
        self.draw_player()
        self.draw_bullet()
        self.draw_enemies()

    def draw_player(self):
        self.game.player.draw()

    def draw_bullet(self):
        if self.game.bullet and self.game.bullet.alive:
            self.game.bullet.draw()

    def draw_enemies(self):
        for enemy in self.game.enemies:
            enemy.draw()

    def add_enemy(self, enemy: Enemy):
        self.game.enemies.append(enemy)

    def draw_map(self):
        [pygame.draw.rect(self.game.screen, 'darkgrey', (pos[0] * 100, pos[1] * 100, 100, 100))
         for pos in self.map.world_map]