import pygame
import os
from .. import settings


class Font:
    _font_normal = None
    _font_small = None
    _font_big = None
    _font_huge = None
    antialiasing = True

    @staticmethod
    def init():
        Font._font_normal = pygame.font.Font(os.path.join(settings.font_folder,
                                                         'MADEGoodTimeGroteskPERSONALUSE.otf'), 24)
        Font._font_small = pygame.font.Font(os.path.join(settings.font_folder, 'tecnico_bold.ttf'), 14)
        Font._font_big = pygame.font.Font(os.path.join(settings.font_folder,
                                                          'MADEGoodTimeGroteskPERSONALUSE.otf'), 40)
        Font._font_huge = pygame.font.Font(os.path.join(settings.font_folder,
                                                       'MADEGoodTimeGroteskPERSONALUSE.otf'), 60)

    @staticmethod
    def get_render(text, color=(255, 255, 255), size='normal'):
        if size == 'small':
            f = Font._font_small.render(text, Font.antialiasing, color)
        elif size == 'normal':
            f = Font._font_normal.render(text, Font.antialiasing, color)
        elif size == 'big':
            f = Font._font_big.render(text, Font.antialiasing, color)
        elif size == 'huge':
            f = Font._font_huge.render(text, Font.antialiasing, color)
        return f

    @staticmethod
    def put_text(surface, text, pos, color=(255, 255, 255), size='normal'):
        f = Font.get_render(text, color, size)
        surface.blit(f, pos)
