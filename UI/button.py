import pygame
from settings import *


class BaseButton:
    def __init__(self, pos, size, text='Write text', font=None, text_color=(255, 255, 255)):
        self.text = text
        self.pos = pos
        self.size = size
        self.font = font or pygame.font.SysFont('Arial', 40)
        self.text_color = text_color
        self.rect = pygame.Rect(self.pos, self.size)

    def draw_text(self, screen):
        if self.text:
            text_surf = self.font.render(self.text, True, self.text_color)
            text_rect = text_surf.get_rect(center=self.rect.center)
            screen.blit(text_surf, text_rect)

    def is_clicked(self, event):
        return event.type == pygame.MOUSEBUTTONDOWN and event.button == 1 and self.rect.collidepoint(pygame.mouse.get_pos())


class RectButton(BaseButton):
    def __init__(self, pos, size, text=None, font=None,
                 bg_color=(50, 50, 50), hover_color=(100, 100, 100), text_color=(255, 255, 255)):
        super().__init__(text=text, pos=pos, size=size, font=font, text_color=text_color)
        self.bg_color = bg_color
        self.hover_color = hover_color

    def draw(self, screen):
        mouse_pos = pygame.mouse.get_pos()
        color = self.hover_color if self.rect.collidepoint(mouse_pos) else self.bg_color
        pygame.draw.rect(screen, color, self.rect)
        pygame.draw.rect(screen, pygame.Color('black'), self.rect, 2)
        self.draw_text(screen)


class ImageButton(BaseButton):
    def __init__(self, pos, size, image, text=None, font=None, text_color=(255, 255, 255)):
        super().__init__(text=text, pos=pos, size=size, font=font, text_color=text_color)
        self.image = image
        self.rect = self.image.get_rect(topleft=pos)

    def draw(self, screen):
        screen.blit(self.image, self.rect)
        self.draw_text(screen)
