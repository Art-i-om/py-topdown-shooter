import pygame
from UI.button import RectButton
from settings import HALF_WIDTH, HALF_HEIGHT


class GameOver:
    def __init__(self, game):
        self.game = game
        self.font = pygame.font.Font(None, 128)
        self.text = self.font.render("Game Over", True, (255, 0, 0))
        self.reset_button = RectButton(
            pos=(HALF_WIDTH - 100, HALF_HEIGHT - 100),
            size=(200, 50),
            text="Restart",
            bg_color=(50, 50, 50),
            hover_color=(100, 100, 100),
            text_color=(255, 255, 255)
        )
        self.quit_button = RectButton(
            pos=(HALF_WIDTH - 100, HALF_HEIGHT),
            size=(200, 50),
            text="Quit",
            bg_color=(50, 50, 50),
            hover_color=(100, 100, 100),
            text_color=(255, 255, 255)
        )

    def draw_to_surface(self):
        self.game.display.fill((0, 0, 0))
        self.game.display.blit(self.text, (HALF_WIDTH - self.text.get_width() // 2, self.text.get_height() * 2))
        self.reset_button.draw(self.game.display)
        self.quit_button.draw(self.game.display)

    def update(self):
        pass

    def check_events(self, event):
        if self.quit_button.is_clicked(event):
            pygame.quit()
            exit()
        if self.reset_button.is_clicked(event):
            self.game.restart_game()
