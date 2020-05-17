import pygame
import os
from .. import settings


class Font:
    _font = {}
    antialiasing = True

    @staticmethod
    def init():
        Font._font["normal"] = pygame.font.Font(os.path.join(settings.font_folder, 'libre-franklin.extrabold.otf'), 24)
        Font._font["small"] = pygame.font.Font(os.path.join(settings.font_folder, 'libre-franklin.regular.otf'), 14)
        Font._font["big"] = pygame.font.Font(os.path.join(settings.font_folder, 'libre-franklin.extrabold.otf'), 40)
        Font._font["huge"] = pygame.font.Font(os.path.join(settings.font_folder, 'libre-franklin.extrabold.otf'), 60)

    @staticmethod
    def get_render(text, color=(255, 255, 255), size='normal'):
        return Font._font[size].render(text, Font.antialiasing, color)

    @staticmethod
    def put_text(surface, text, pos, color=(255, 255, 255), size='normal'):
        f = Font.get_render(text, color, size)
        surface.blit(f, pos)
