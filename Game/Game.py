import pygame
from . import settings
from .utils import *
from .Levels import Levels
from .Menu import StartMenu, PauseMenu, SettingsMenu, EndMenu
from .UI import Mouse, Font


class Game:
    def __init__(self):
        # os.environ['SDL_VIDEO_WINDOW_POS'] = "%d,%d" % (20, 50)
        pygame.init()

        icon = pygame.image.load('Resources/tim_icon.ico')
        pygame.display.set_icon(icon)

        self.display_flags = pygame.HWSURFACE | pygame.DOUBLEBUF
        self.fullscreen_flag = pygame.FULLSCREEN
        self.fullscreen = False
        self._scale_screen = False

        self.display = pygame.display.set_mode((settings.FINAL_WIDTH, settings.FINAL_HEIGHT), self.display_flags)
        self.screen = pygame.Surface((settings.SCREEN_WIDTH, settings.SCREEN_HEIGHT))

        self.screen_rect = self.screen.get_rect()
        pygame.display.set_caption(settings.WIN_TITLE)

        self.exit_game = False
        Font.init()
        Mouse.init()

        self._scenes = {
            "level_manager": [Levels, (self.goto_scene,)],
            "pause_menu": [PauseMenu, (self.goto_scene,)],
            "start_menu": [StartMenu, (self.goto_scene,)],
            "settings_menu": [SettingsMenu, (self.goto_scene, self.update_display_config)],
            "end_menu": [EndMenu, (self.goto_scene,)],
        }
        self._scene = None
        self._scene_stack = []
        self.goto_scene("start_menu")

        pygame.mixer.music.load(os.path.join(settings.music_folder, 'Road to Dazir.ogg'))
        pygame.mixer.music.set_volume(1)
        pygame.mixer.music.play(-1)

        self.clock = pygame.time.Clock()

    def goto_scene(self, scene_name, *other_args):
        if scene_name == "quit":
            self.exit_game = True
        elif scene_name == "previous":
            self.goto_previous_scene()
        elif scene_name == "start_menu" and len(self._scene_stack) > 0:
            self._scene_stack = self._scene_stack[:1]
            print("[GameScene Manager]  Returning to", self._scene_stack[-1])
            self._scene = self._scene_stack[-1]
        elif scene_name in self._scenes:
            self._scene_stack.append(self._scenes[scene_name][0](*self._scenes[scene_name][1], *other_args))
            print("[GameScene Manager]  Going to", self._scene_stack[-1])
            self._scene = self._scene_stack[-1]

    def goto_previous_scene(self):
        if len(self._scene_stack) > 1:
            print("[GameScene Manager]  Returning to", self._scene_stack[-2])
            self._scene = self._scene_stack[-2]
            self._scene_stack.pop()

    def update_display_config(self, fullscreen, height=settings.FINAL_HEIGHT):
        needs_update = False
        if settings.FULLSCREEN != fullscreen:
            settings.FULLSCREEN = fullscreen
            height = 720 if fullscreen else 480
            needs_update = True
        if settings.FINAL_HEIGHT != height:
            settings.FINAL_HEIGHT = height
            settings.FINAL_WIDTH = int(settings.FINAL_HEIGHT * 16 / 9)
            needs_update = True

        if needs_update:
            if settings.FULLSCREEN:
                pygame.display.set_mode((settings.FINAL_WIDTH, settings.FINAL_HEIGHT),
                                        self.display_flags | pygame.FULLSCREEN)
            else:
                pygame.display.set_mode((settings.FINAL_WIDTH, settings.FINAL_HEIGHT),
                                        self.display_flags)

    def render(self):
        self._scene.render(self.screen)

        # render fps
        if settings.SHOW_FPS:
            Font.put_text(self.screen, str(int(self.clock.get_fps())), (settings.SCREEN_WIDTH-50, 16), (251, 255, 196))

        self.display.blit(pygame.transform.scale(self.screen, self.display.get_rect().size), (0, 0))
        Mouse.render(self.display)

        pygame.display.flip()

    def run(self):
        while not self.exit_game:

            self.render()

            # event handling
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    self.exit_game = True
                elif event.type == pygame.KEYDOWN and event.key == pygame.K_t:
                    settings.DEBUG_DRAW = not settings.DEBUG_DRAW
                elif event.type == pygame.KEYDOWN and event.key == pygame.K_f:
                    if isinstance(self._scene, Levels):
                        self.goto_scene("pause_menu")
                    self.update_display_config(not settings.FULLSCREEN)
                else:
                    self._scene.handle_events(event)

            self.clock.tick(settings.FPS)
            delta_time = self.clock.get_time() / 1000
            self._scene.update(delta_time)

    def quit(self):
        pygame.quit()