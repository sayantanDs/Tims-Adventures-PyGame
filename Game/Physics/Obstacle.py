import pygame
from .Collidable import Collidable
from .. import settings


class ObstacleRect(Collidable):
    def __init__(self, x, y, width, height):
        Collidable.__init__(self, x, y, width, height)

    def render(self, surface, camera):
        if settings.DEBUG_DRAW:
            pygame.draw.rect(surface, settings.DEBUG_DRAW_COLOR,
                             pygame.Rect(camera.get_relative_pos(self.rect.x, self.rect.y),
                                         (self.rect.width, self.rect.height)), 1)


class ObstacleSlope(Collidable):
    def __init__(self, x, y, width, height, direction='right'):
        Collidable.__init__(self, x, y, width, height)
        self.direction = direction
        self.slope = height / width
        if direction == 'left':
            self.slope *= -1

    def get_overlap_x(self, rect: pygame.Rect) -> (int, int):
        # if not self.rect.colliderect(rect):
        return 0, None

    def get_overlap_y(self, rect: pygame.Rect) -> (int, int):
        if not self.rect.colliderect(rect):
            return 0, None

        if self.slope > 0:
            if rect.right >= self.rect.right:  # top of slope condition
                return rect.bottom - self.rect.top, 'bottom'
            # calculating x wrt bottom left
            x = rect.right - self.rect.x

        else:
            if rect.left <= self.rect.left:  # top of slope condition
                return rect.bottom - self.rect.top, 'bottom'
            # calculating x wrt bottom left
            x = rect.left - self.rect.right

        y = self.rect.bottom - self.slope * x

        if y - rect.bottom > 0:
            return 0, None
        return rect.bottom - y, 'bottom'

    def render(self, surface, camera):

        r = camera.get_relative_rect(self.rect)
        if self.slope > 0:
            pt3 = r.topright
        else:
            pt3 = r.topleft
        if settings.DEBUG_DRAW:
            pygame.draw.polygon(surface, settings.DEBUG_DRAW_COLOR, [r.bottomleft, r.bottomright, pt3], 1)


class ObstacleOneWay(Collidable):
    def __init__(self, x, y, width, height):
        Collidable.__init__(self, x, y, width, height)

    def get_overlap_x(self, rect: pygame.Rect):
        return 0, None

    def get_overlap_y(self, rect: pygame.Rect):
        if not self.rect.colliderect(rect):
            return 0, None

        # only bottom collision
        if rect.y < self.rect.y < rect.bottom < self.rect.bottom:
            return rect.bottom - self.rect.y, 'bottom'
        else:
            return 0, None

    def render(self, surface, camera):
        if settings.DEBUG_DRAW:
            pygame.draw.rect(surface, settings.DEBUG_DRAW_COLOR,
                            pygame.Rect(camera.get_relative_pos(self.rect.x, self.rect.y),
                                                                (self.rect.width, self.rect.height)), 1)
