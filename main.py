import moderngl
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
        self.screen = pygame.display.set_mode(RES, pygame.OPENGL | pygame.DOUBLEBUF)
        self.ctx = moderngl.create_context()
        self.display = pygame.Surface(self.screen.get_size())
        self.clock = pygame.time.Clock()
        self.delta_time = 1
        self.player = None
        self.map = None
        self.bullet = None
        self.game_over = None
        self.object_renderer = None
        self.enemies = []
        self.running = True
        self.game_state = "playing"
        self.new_game()

    def new_game(self):
        self.player = Player(self)
        self.map = Map(self)
        self.game_over = GameOver(self)
        self.object_renderer = ObjectRenderer(self)

    def update(self):
        if self.game_state == "playing":
            self.player.update()
            if self.bullet and self.bullet.alive:
                self.bullet.update()
            else:
                self.bullet = None
            for enemy in self.enemies:
                enemy.update()
        elif self.game_state == "game_over":
            self.game_over.update()

        self.delta_time = self.clock.tick(FPS)
        pygame.display.set_caption(f'{self.clock.get_fps() :.1f}')

    def draw(self):
        self.display.fill((0, 0, 0))
        if self.game_state == "playing":
            self.object_renderer.draw_game_state()
        elif self.game_state == "game_over":
            self.object_renderer.draw_game_over_state()

    def check_events(self):
        for event in pygame.event.get():
            if event.type == pygame.QUIT or (event.type == pygame.KEYDOWN and event.key == pygame.K_ESCAPE):
                pygame.quit()
                sys.exit()

            if self.game_state == "playing":
                if event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
                    if not self.bullet:
                        self.bullet = Bullet(self)
                if event.type == pygame.MOUSEBUTTONUP and event.button == 1:
                    self.bullet = None
            elif self.game_state == "game_over":
                self.game_over.check_events(event)

    def trigger_game_over(self):
        self.game_state = "game_over"

    def restart_game(self):
        self.game_state = "playing"
        self.new_game()

    def run(self):
        while self.running:
            self.check_events()
            self.update()
            self.draw()


if __name__ == '__main__':
    while True:
        game = Game()
        game.run()
