import pygame
from .. import settings
from .Collidable import Collidable
from .Obstacle import ObstacleOneWay
from ..UI import Font


class RigidBody(Collidable, pygame.sprite.Sprite):
    def __init__(self, x, y, width, height):
        Collidable.__init__(self,  x, y, width, height)

        self.v_x = 0
        self.v_y = 0
        self.mass = width*height
        self.restitution = 0.5

    @staticmethod
    def _sign(num):
        return -1 if num < 0 else 1

    def do_physics(self, delta_time, collidables, no_gravity=False):
        if not no_gravity:
            self.v_y += settings.GRAVITY * delta_time

        if abs(self.v_y) > settings.TERMINAL_V:
            self.v_y = self._sign(self.v_y)*settings.TERMINAL_V
        if abs(self.v_x) > settings.TERMINAL_V:
            self.v_x = self._sign(self.v_x)*settings.TERMINAL_V

        x_mov = int(self.v_x * delta_time)  # was moving faster in negative direction if not converted to int
        y_mov = int(self.v_y * delta_time)

        colliding = {'top': False, 'bottom': False, 'right': False, 'left': False}

        # -----------------------[ Y COLLISION ]---------------------------
        # sweep over the total movement in steps
        while y_mov:
            sign = self._sign(y_mov)
            if abs(y_mov) > settings.MAX_COLLISION_STEP_SIZE:
                y_step = sign * settings.MAX_COLLISION_STEP_SIZE
            else:
                y_step = y_mov
            y_mov -= y_step

            self.rect.y += y_step

            collision_occurred = False
            for collidable in collidables:
                if collidable is not self:
                    overlap_y, collision_dir = collidable.get_overlap_y(self.rect)
                    # if collision occurred
                    if overlap_y:
                        if isinstance(collidable, ObstacleOneWay):
                            if self.v_y < 0:
                                continue
                            elif hasattr(self, 'climbing') and self.climbing:
                                continue
                        self.rect.y -= overlap_y
                        collision_occurred = True
                        colliding[collision_dir] = True

            # if collision occurred in this sweep, no need to sweep further
            if collision_occurred:
                break

        # -----------------------[ X COLLISION ]---------------------------

        # sweep over the total movement in steps
        while x_mov:
            sign = self._sign(x_mov)
            if abs(x_mov) > settings.MAX_COLLISION_STEP_SIZE:
                x_step = sign * settings.MAX_COLLISION_STEP_SIZE
            else:
                x_step = x_mov
            x_mov -= x_step

            self.rect.x += x_step

            collision_occurred = False
            for collidable in collidables:
                if collidable is not self:
                    overlap_x, collision_dir = collidable.get_overlap_x(self.rect)
                    # if collision occurred
                    if overlap_x:
                        self.rect.x -= overlap_x
                        collision_occurred = True
                        colliding[collision_dir] = True

            # if collision occurred in this sweep, no need to sweep further
            if collision_occurred:
                break

        if colliding['left'] or colliding['right']:
            self.v_x = 0
        if colliding['top'] or colliding['bottom']:
            self.v_y = 0

        return colliding

    def render(self, surface, camera):
        if settings.DEBUG_DRAW:
            pygame.draw.rect(surface, settings.DEBUG_DRAW_COLOR,
                             pygame.Rect(camera.get_relative_pos(self.rect.x, self.rect.y),
                                         (self.rect.width, self.rect.height)), 1)

            Font.put_text(surface, "(%0.2f, %03d)"%(self.v_x, int(self.v_y)), camera.get_relative_pos(self.rect.right+5, self.rect.top - 10), (0,0,0), "small")
