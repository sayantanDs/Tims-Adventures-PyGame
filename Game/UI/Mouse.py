import pygame
import os
from .. import settings


class Mouse:
    cursor_img = None
    _visible = True

    @staticmethod
    def init():
        # Mouse.cursor_img = pygame.image.load(os.path.join(settings.img_folder, "Light Blue.png")).convert_alpha()
        Mouse.cursor_img = pygame.image.load(os.path.join(settings.img_folder, "Cursors", "Cursor1.png")).convert_alpha()
        pygame.mouse.set_visible(False)

    @staticmethod
    def set_visible(torf):
        Mouse._visible = torf

    @staticmethod
    def is_visible():
        return Mouse._visible

    @staticmethod
    def render(surface):
        if Mouse._visible:
            # surface.blit(Mouse.cursor_img, Mouse.get_pos())
            surface.blit(Mouse.cursor_img, pygame.mouse.get_pos())

    @staticmethod
    def get_pos():
        px, py = pygame.mouse.get_pos()
        px = int(px * settings.SCREEN_WIDTH / settings.FINAL_WIDTH)
        py = int(py * settings.SCREEN_HEIGHT / settings.FINAL_HEIGHT)
        return px, py

    @staticmethod
    def set_pos(x, y):
        px = int(x * settings.FINAL_WIDTH / settings.SCREEN_WIDTH)
        py = int(y * settings.FINAL_HEIGHT / settings.SCREEN_HEIGHT)
        pygame.mouse.set_pos((px, py))