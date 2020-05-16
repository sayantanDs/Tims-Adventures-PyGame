import pygame
import sys
import os
from . import settings
from .Map import Map
from .ParallaxBg import make_parallax_bg
from .Player import Player
from .Camera import Camera
from .Mob import Mob
from .utils import *
from .Levels import Levels
from .Menu import StartMenu, PauseMenu, SettingsMenu
from .UI import Mouse, Font


class Game:
    def __init__(self):
        # os.environ['SDL_VIDEO_WINDOW_POS'] = "%d,%d" % (20, 50)
        pygame.init()

        self.display_flags = pygame.HWSURFACE | pygame.DOUBLEBUF
        self.fullscreen_flag = pygame.FULLSCREEN
        self.fullscreen = False
        self._scale_screen = False
        if settings.SCREEN_WIDTH != settings.FINAL_WIDTH:
            self.display = pygame.display.set_mode((settings.FINAL_WIDTH, settings.FINAL_HEIGHT), self.display_flags)
            self.screen = pygame.Surface((settings.SCREEN_WIDTH, settings.SCREEN_HEIGHT))
            self._scale_screen = True
        else:
            self.screen = pygame.display.set_mode((settings.SCREEN_WIDTH, settings.SCREEN_HEIGHT), self.display_flags)

        self.screen_rect = self.screen.get_rect()
        pygame.display.set_caption(settings.WIN_TITLE)

        self.exit_game = False
        Font.init()
        Mouse.init()

        self._scenes = {
            "level_manager": Levels(self._switch_scene),
            "pause_menu": PauseMenu(self._switch_scene),
            "start_menu": StartMenu(self._switch_scene),
            "settings_menu": SettingsMenu(self._switch_scene)
        }
        self._scene = self._scenes["start_menu"]
        self._prev_scene = self._scene

        pygame.mixer.music.load(os.path.join(settings.music_folder, 'Road to Dazir.ogg'))
        pygame.mixer.music.set_volume(0.5)
        pygame.mixer.music.play(-1)

        self.clock = pygame.time.Clock()

    def _switch_scene(self, scene_name):
        if scene_name == "quit":
            self.exit_game = True
        elif scene_name == "previous":
            self._scene = self._prev_scene
        elif scene_name in self._scenes:
            self._prev_scene = self._scene
            self._scene = self._scenes[scene_name]

    def render(self):
        self._scene.render(self.screen)

        # render fps
        Font.put_text(self.screen, str(int(self.clock.get_fps())), (settings.SCREEN_WIDTH-50, 16), (251, 255, 196))

        if self._scale_screen:
            self.display.blit(pygame.transform.scale(self.screen, self.display.get_rect().size), (0, 0))
            Mouse.render(self.display)
        else:
            Mouse.render(self.screen)

        pygame.display.flip()

    def run(self):
        while not self.exit_game:

            self.render()

            # event handling
            for event in pygame.event.get():
                if event.type == pygame.QUIT or (event.type == pygame.KEYDOWN and event.key == pygame.K_ESCAPE):
                    self.exit_game = True
                elif event.type == pygame.KEYDOWN and event.key == pygame.K_t:
                    settings.DEBUG_DRAW = not settings.DEBUG_DRAW
                elif event.type == pygame.KEYDOWN and event.key == pygame.K_f:
                    self.fullscreen = not self.fullscreen
                    if self.fullscreen:
                        pygame.display.set_mode((settings.FINAL_WIDTH, settings.FINAL_HEIGHT),
                                                self.display_flags | pygame.FULLSCREEN)
                    else:
                        pygame.display.set_mode((settings.FINAL_WIDTH, settings.FINAL_HEIGHT),
                                                self.display_flags)
                else:
                    self._scene.handle_events(event)

            self.clock.tick(settings.FPS)
            delta_time = self.clock.get_time() / 1000
            self._scene.update(delta_time)

    def quit(self):
        pygame.quit()