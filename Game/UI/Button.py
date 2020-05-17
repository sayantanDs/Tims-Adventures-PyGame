import pygame
import os
from .Font import Font
from .Mouse import Mouse
from .. import settings


class Button:
    select_sound = None
    click_sound = None

    @staticmethod
    def _load_resources():
        if Button.select_sound is None:
            Button.select_sound = pygame.mixer.Sound(os.path.join(settings.music_folder, 'zipclick.wav'))
            Button.click_sound = pygame.mixer.Sound(os.path.join(settings.music_folder, 'klick1.wav'))
            Button.click_sound.set_volume(0.5)

    def __init__(self, pos, size, text, callback, bttn_color=(48, 59, 77), text_color=(255,255,255)):
        self._load_resources()
        self.rect = pygame.Rect(pos, size)
        self._color = bttn_color
        # k = 20
        # self._color_hover = ((bttn_color[0]+k)%256, (bttn_color[1]+k)%256, (bttn_color[2]+k)%256)
        self._color_hover = (87, 149, 230)
        self._text = text
        self._text_color = text_color
        self._callback = callback
        self._mouse_in_rect = False

        self._text_surface = Font.get_render(self._text, self._text_color)
        self._text_rect = self._text_surface.get_rect()
        self._text_x = self.rect.x + (self.rect.width - self._text_rect.width)//2
        self._text_y = self.rect.y + (self.rect.height - self._text_rect.height)//2

    def render(self, surface):
        if self._mouse_in_rect:
            pygame.draw.circle(surface, self._color_hover, (self.rect.x, self.rect.centery), self.rect.height//2)
            pygame.draw.circle(surface, self._color_hover, (self.rect.right, self.rect.centery), self.rect.height//2)

            pygame.draw.rect(surface, self._color_hover, self.rect)

        else:
            pygame.draw.circle(surface, self._color, (self.rect.x, self.rect.centery), self.rect.height // 2)
            pygame.draw.circle(surface, self._color, (self.rect.right, self.rect.centery), self.rect.height // 2)
            pygame.draw.rect(surface, self._color, self.rect)

        surface.blit(self._text_surface, (self._text_x, self._text_y))

    def handle_events(self, event):
        # if self.rect.collidepoint(*pygame.mouse.get_pos()):
        if self.rect.collidepoint(*Mouse.get_pos()):
            if self._mouse_in_rect is False:
                self.select_sound.play()
                self._mouse_in_rect = True

        else:
            self._mouse_in_rect = False
        if self._mouse_in_rect and event.type == pygame.MOUSEBUTTONUP and event.button == 1:
            self.click_sound.play()
            self._callback()