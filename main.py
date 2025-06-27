import pygame
from settings import *
from player import *
from map import *
from bullet import *
from enemy import *
from UI.game_over import *
from object_renderer import *
import sys


class Game:
    def __init__(self):
        pygame.init()
        self.screen = pygame.display.set_mode(RES)
        self.clock = pygame.time.Clock()
        self.delta_time = 1
        self.player = None
        self.map = None
        self.bullet = None
        self.game_over = None
        self.object_renderer = None
        self.enemies = []
        self.running = True
        self.new_game()

    def new_game(self):
        self.player = Player(self)
        self.map = Map(self)
        self.game_over = GameOver(self)
        self.object_renderer = ObjectRenderer(self)

    def update(self):
        self.player.update()
        if self.bullet and self.bullet.alive:
            self.bullet.update()
        else:
            self.bullet = None
        for enemy in self.enemies:
            enemy.update()
        self.delta_time = self.clock.tick(FPS)
        pygame.display.set_caption(f'{self.clock.get_fps() :.1f}')

    def draw(self):
        self.screen.fill((0, 0, 0))
        self.object_renderer.draw()
        pygame.display.flip()

    def check_events(self):
        for event in pygame.event.get():
            if event.type == pygame.QUIT or (event.type == pygame.KEYDOWN and event.key == pygame.K_ESCAPE):
                pygame.quit()
                sys.exit()
            if event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
                if not self.bullet:
                    self.bullet = Bullet(self)
            if event.type == pygame.MOUSEBUTTONUP and event.button == 1:
                self.bullet = None

    def run(self):
        while self.running:
            self.check_events()
            self.update()
            self.draw()


if __name__ == '__main__':
    while True:
        game = Game()
        game.run()
