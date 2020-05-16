from .GameScene import GameScene
from . import settings
import pygame
import os
from .UI import Mouse, Button, Font


class StartMenu(GameScene):
    bg = None
    @staticmethod
    def _load_resources():
        if StartMenu.bg is None:
            StartMenu.bg = pygame.transform.smoothscale(pygame.image.load(os.path.join(settings.img_folder, "HUD", "main_menu_bg_50.png")), (settings.SCREEN_WIDTH, settings.SCREEN_HEIGHT))

    def __init__(self, switch_scene):
        GameScene.__init__(self)
        self._load_resources()
        self._title = Font.get_render(settings.WIN_TITLE, size="huge")
        self._text_rect = self._title.get_rect()
        self._text_x = (settings.SCREEN_WIDTH - self._text_rect.width) // 2
        self._text_y = self._text_rect.height // 2

        y = self._text_rect.bottom + 60
        w, h = 150, 50
        self.start_bttn = Button((settings.SCREEN_WIDTH//2-75, y), (w, h), "Start", lambda: switch_scene("level_manager"))
        self.settings_bttn = Button((settings.SCREEN_WIDTH//2-75, y+75), (w, h), "Settings", lambda: switch_scene("settings_menu"))
        self.credits_bttn = Button((settings.SCREEN_WIDTH//2-75, y+150), (w, h), "Credits", lambda: switch_scene("credits"))
        self.exit_bttn = Button((settings.SCREEN_WIDTH//2-75, y+225), (w, h), "Quit", lambda: switch_scene("quit"))


    def render(self, surface):
        # surface.fill((35, 25, 40))
        surface.blit(self.bg, (0,0))
        # surface.fill((250, 250, 250), special_flags=pygame.BLEND_MULT)
        surface.blit(self._title, (self._text_x, self._text_y))
        self.start_bttn.render(surface)
        self.settings_bttn.render(surface)
        self.credits_bttn.render(surface)
        self.exit_bttn.render(surface)

    def update(self, delta_time):
        pass

    def handle_events(self, event):
        self.start_bttn.handle_events(event)
        self.settings_bttn.handle_events(event)
        self.credits_bttn.handle_events(event)
        self.exit_bttn.handle_events(event)


class PauseMenu(GameScene):
    def __init__(self, switch_scene):
        GameScene.__init__(self)
        w, h = 150, 50
        self.continue_bttn = Button(((settings.SCREEN_WIDTH-w)//2, (settings.SCREEN_HEIGHT-h)//2), (w, h),
                                    "Continue", lambda: switch_scene("level_manager"))
        self.settings_bttn = Button(((settings.SCREEN_WIDTH - w) // 2, (settings.SCREEN_HEIGHT - h) // 2 + 75), (w, h),
                                    "Settings", lambda: switch_scene("settings_menu"))

        self._text_surface = Font.get_render("Paused", size="big")
        self._text_rect = self._text_surface.get_rect()
        self._text_x = (settings.SCREEN_WIDTH - self._text_rect.width) // 2
        self._text_y = (settings.SCREEN_HEIGHT - self._text_rect.height) // 2 - h - 30

    def render(self, surface):
        surface.fill((35, 25, 40))
        surface.blit(self._text_surface, (self._text_x, self._text_y))
        self.continue_bttn.render(surface)
        self.settings_bttn.render(surface)

    def update(self, delta_time):
        pass

    def handle_events(self, event):
        self.continue_bttn.handle_events(event)
        self.settings_bttn.handle_events(event)


class SettingsMenu(GameScene):
    def __init__(self, switch_scene):
        self._switch_scene = switch_scene
        GameScene.__init__(self)
        w, h = 150, 50
        self.continue_bttn = Button(((settings.SCREEN_WIDTH-w)//2, (settings.SCREEN_HEIGHT-h)//2), (w, h),
                                    "Done", self._on_done)

        self._text_surface = Font.get_render("Settings", size="big")
        self._text_rect = self._text_surface.get_rect()
        self._text_x = (settings.SCREEN_WIDTH - self._text_rect.width) // 2
        self._text_y = self._text_rect.height//2

    def _on_done(self):
        self._switch_scene("previous")

    def render(self, surface):
        surface.fill((35, 25, 40))
        surface.blit(self._text_surface, (self._text_x, self._text_y))
        self.continue_bttn.render(surface)

    def update(self, delta_time):
        pass

    def handle_events(self, event):
        self.continue_bttn.handle_events(event)