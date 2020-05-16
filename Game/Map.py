import pygame
import pytmx
from .Physics import ObstacleRect, ObstacleSlope, ObstacleOneWay


class Map:
    def __init__(self, filename):
        self.tmx = pytmx.load_pygame(filename, pixelalpha=True)
        self.width = self.tmx.width * self.tmx.tilewidth
        self.height = self.tmx.height * self.tmx.tileheight

        self.mob_spawns = []
        self.ladders = []
        self.collidables = []
        self.coins = []

        self.surface = pygame.Surface((self.width, self.height), pygame.SRCALPHA)

    def render(self, surface):
        for layer in self.tmx.visible_layers:
            if isinstance(layer, pytmx.TiledTileLayer):
                for x, y, gid in layer:
                    tile = self.tmx.get_tile_image_by_gid(gid)
                    if tile:
                        r = tile.get_rect()
                        surface.blit(tile, (x * self.tmx.tilewidth, (y + 1) * self.tmx.tileheight - r.height))

    def load_obstacles(self):
        for obj in self.tmx.objects:
            if obj.name == 'spawn':
                self.spawn_point = (obj.x, obj.y)
            elif obj.name == 'mob_spawn':
                self.mob_spawns.append((obj.x, obj.y))
            elif obj.name == 'goal':
                self.goal = pygame.Rect(obj.x, obj.y, obj.width, obj.height)
            elif obj.name == 'ladder':
                self.ladders.append(pygame.Rect(obj.x, obj.y, obj.width, obj.height))
            elif obj.name == 'oneway':
                self.collidables.append(ObstacleOneWay(obj.x, obj.y, obj.width, obj.height))
            elif obj.name == 'slope':
                p = sorted(list(obj.points))
                if p[0][0] == p[1][0]:      # left
                    x, y, w, h = p[0][0], p[0][1], p[2][0]-p[0][0], p[2][1]-p[0][1]
                    self.collidables.append(ObstacleSlope(x, y, w, h, 'left'))
                else:                       # right
                    x, y, w, h = p[0][0], p[1][1], p[1][0]-p[0][0], p[0][1] - p[1][1]
                    self.collidables.append(ObstacleSlope(x, y, w, h, 'right'))
            elif obj.name == "coin":
                self.coins.append((obj.x, obj.y))
            elif obj.name == "text":
                pass
            else:
                self.collidables.append(ObstacleRect(obj.x, obj.y, obj.width, obj.height))

    def make_map(self):
        self.mob_spawns = []
        self.render(self.surface)
        self.load_obstacles()
        return self.surface.convert_alpha()
