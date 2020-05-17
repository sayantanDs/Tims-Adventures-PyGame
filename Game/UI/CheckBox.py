import pygame
import os
from .Font import Font
from .Mouse import Mouse
from .. import settings


class CheckBox:
    click_sound = None

    @staticmethod
    def _load_resources():
        if CheckBox.click_sound is None:
            CheckBox.click_sound = pygame.mixer.Sound(os.path.join(settings.music_folder, 'klick1.wav'))
            CheckBox.click_sound.set_volume(0.5)

    def __init__(self, pos, text, text_color=(255, 255, 255)):
        self._load_resources()
        self.checkbox_rect = pygame.Rect(pos, (25, 25))
        self.checkbox_inside_rect = pygame.Rect((pos[0]+5, pos[1]+5), (15, 15))
        self._color = (250, 250, 250)
        self._color_hover = (87, 149, 230)

        self._text = text
        self._text_color = text_color
        self._text_surface = Font.get_render(self._text, self._text_color)
        self._text_rect = self._text_surface.get_rect()
        self._text_x = pos[0] + 50
        self._text_y = self.checkbox_rect.centery - self._text_rect.height//2

        self.selected = False
        self._mouse_in_rect = False

    def render(self, surface):
        pygame.draw.rect(surface, self._color, self.checkbox_rect, 2)
        if self.selected:
            pygame.draw.rect(surface, self._color_hover, self.checkbox_inside_rect)

        surface.blit(self._text_surface, (self._text_x, self._text_y))

    def handle_events(self, event):
        # if self.rect.collidepoint(*pygame.mouse.get_pos()):
        if self.checkbox_rect.collidepoint(*Mouse.get_pos()):
            if self._mouse_in_rect is False:
                self._mouse_in_rect = True
        else:
            self._mouse_in_rect = False

        if self._mouse_in_rect and event.type == pygame.MOUSEBUTTONUP and event.button == 1:
            self.click_sound.play()
            self.selected = not self.selected