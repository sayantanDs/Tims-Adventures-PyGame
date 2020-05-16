from .Mouse import Mouse
import pygame
from .Font import Font


class Button:
    def __init__(self, pos, size, text, callback, bttn_color=(48, 59, 77), text_color=(255,255,255)):
        self.rect = pygame.Rect(pos, size)
        self._color = bttn_color
        # k = 20
        # self._color_hover = ((bttn_color[0]+k)%256, (bttn_color[1]+k)%256, (bttn_color[2]+k)%256)
        self._color_hover = 87, 149, 230
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
            self._mouse_in_rect = True
        else:
            self._mouse_in_rect = False
        if self._mouse_in_rect and event.type == pygame.MOUSEBUTTONUP and event.button == 1:
            self._callback()