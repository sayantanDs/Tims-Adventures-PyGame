import pygame
import math


class ParallaxLayer:
    def __init__(self, texture, parallax_multiplier, camera, map_width, map_height):
        self.parallax_multiplier = parallax_multiplier
        self.texture = texture
        self._scaled_texture = self._resize(texture, parallax_multiplier, camera, map_width, map_height)

    def _resize(self, texture, parallax_multiplier, camera, map_width, map_height):
        w, h = texture.get_rect().size
        c_w, c_h = camera.camera_rect.size

        scaled_h = (map_height - c_h) * parallax_multiplier + c_h
        scaled_w = w * scaled_h / h

        texture = pygame.transform.smoothscale(texture, (int(scaled_w), int(scaled_h)))
        if scaled_w < map_width:
            n = int(math.ceil(map_width / scaled_w))
            texture = self._repeat(texture, n)

        return texture

    def _repeat(self, image, n):
        r = image.get_rect()
        img = pygame.Surface((r.width * n, r.height), pygame.SRCALPHA)
        img.blits([(image, (r.width * i, 0)) for i in range(n)])
        return img

    def render(self, surface, camera):
        surface.blit(self._scaled_texture, camera.get_relative_pos(0, 0, self.parallax_multiplier))



