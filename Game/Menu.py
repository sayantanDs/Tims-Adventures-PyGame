from .GameScene import GameScene
from . import settings
import pygame
import os
from .UI import Mouse, Button, Font, CheckBox


class StartMenu(GameScene):
    bg = None

    @staticmethod
    def _load_resources():
        if StartMenu.bg is None:
            StartMenu.bg = pygame.transform.smoothscale(pygame.image.load(os.path.join(settings.img_folder, "HUD", "main_menu_bg_50.png")), (settings.SCREEN_WIDTH, settings.SCREEN_HEIGHT))

    def __init__(self, goto_scene):
        self._goto_scene = goto_scene
        GameScene.__init__(self)
        self._load_resources()

        Mouse.set_visible(True)

        # self._title = Font.get_render(settings.WIN_TITLE, size="huge")
        self._title = pygame.image.load(os.path.join(settings.img_folder, "title_text.png"))
        self._text_rect = self._title.get_rect()
        self._text_x = (settings.SCREEN_WIDTH - self._text_rect.width) // 2
        self._text_y = self._text_rect.height // 2

        y = self._text_rect.bottom + 100
        w, h = 150, 50
        self.start_bttn = Button((settings.SCREEN_WIDTH//2-75, y), (w, h), "Start", lambda: goto_scene("level_manager"))
        self.settings_bttn = Button((settings.SCREEN_WIDTH//2-75, y+75), (w, h), "Settings", lambda: goto_scene("settings_menu"))
        # self.credits_bttn = Button((settings.SCREEN_WIDTH//2-75, y+150), (w, h), "Credits", lambda: goto_scene("credits"))
        self.exit_bttn = Button((settings.SCREEN_WIDTH//2-75, y+150), (w, h), "Quit", lambda: goto_scene("quit"))

    def render(self, surface):
        surface.blit(self.bg, (0, 0))
        surface.blit(self._title, (self._text_x, self._text_y))
        self.start_bttn.render(surface)
        self.settings_bttn.render(surface)
        # self.credits_bttn.render(surface)
        self.exit_bttn.render(surface)

    def update(self, delta_time):
        pass

    def handle_events(self, event):
        self.start_bttn.handle_events(event)
        self.settings_bttn.handle_events(event)
        # self.credits_bttn.handle_events(event)
        self.exit_bttn.handle_events(event)

        if event.type == pygame.KEYDOWN and (event.key == pygame.K_p or event.key == pygame.K_ESCAPE):
            self._goto_scene("quit")


class PauseMenu(GameScene):
    def __init__(self, goto_scene):
        self._goto_scene = goto_scene
        GameScene.__init__(self)
        Mouse.set_visible(True)
        w, h = 150, 50

        self._text_surface = Font.get_render("Paused", size="big")
        self._text_rect = self._text_surface.get_rect()
        self._text_x = (settings.SCREEN_WIDTH - self._text_rect.width) // 2
        self._text_y = self._text_rect.height // 2

        self.continue_bttn = Button(((settings.SCREEN_WIDTH-w)//2, self._text_rect.bottom + 50), (w, h),
                                    "Continue", lambda: goto_scene("previous"))
        self.settings_bttn = Button(((settings.SCREEN_WIDTH - w) // 2, self._text_rect.bottom + 125), (w, h),
                                    "Settings", lambda: goto_scene("settings_menu"))
        self.start_menu_bttn = Button(((settings.SCREEN_WIDTH - w) // 2, self._text_rect.bottom + 200), (w, h), "Start Menu",
                                lambda: goto_scene("start_menu"))
        self.exit_bttn = Button(((settings.SCREEN_WIDTH - w) // 2, self._text_rect.bottom + 275), (w, h), "Quit",
                                lambda: goto_scene("quit"))

    def render(self, surface):
        surface.fill((35, 25, 40))
        surface.blit(self._text_surface, (self._text_x, self._text_y))
        self.continue_bttn.render(surface)
        self.settings_bttn.render(surface)
        self.start_menu_bttn.render(surface)
        self.exit_bttn.render(surface)

    def update(self, delta_time):
        pass

    def handle_events(self, event):
        self.continue_bttn.handle_events(event)
        self.settings_bttn.handle_events(event)
        self.start_menu_bttn.handle_events(event)
        self.exit_bttn.handle_events(event)

        if event.type == pygame.KEYDOWN and (event.key == pygame.K_p or event.key == pygame.K_ESCAPE):
            self._goto_scene("previous")


class SettingsMenu(GameScene):
    def __init__(self, goto_scene, update_display_config):
        self._goto_scene = goto_scene
        self._update_display_config = update_display_config

        GameScene.__init__(self)
        Mouse.set_visible(True)
        w, h = 150, 50

        self._text_surface = Font.get_render("Settings", size="big")
        self._text_rect = self._text_surface.get_rect()
        self._text_x = (settings.SCREEN_WIDTH - self._text_rect.width) // 2
        self._text_y = self._text_rect.height//2

        self._fullscreen_checkbox = CheckBox((50, self._text_rect.bottom+50), "Fullscreen")
        self._fullscreen_checkbox.selected = settings.FULLSCREEN
        self._scale_checkbox = CheckBox((50, self._text_rect.bottom + 100), "Scale to 1280x720")
        self._scale_checkbox.selected = (settings.FINAL_HEIGHT != settings.SCREEN_HEIGHT)
        self._fps_checkbox = CheckBox((50, self._text_rect.bottom + 150), "Show FPS")
        self._fps_checkbox.selected = settings.SHOW_FPS

        self.continue_bttn = Button((50, (settings.SCREEN_HEIGHT - h - 25)), (w, h),
                                    "Done", self._on_done)

    def _on_done(self):
        settings.SHOW_FPS = self._fps_checkbox.selected
        h = 720 if self._scale_checkbox.selected else 480
        self._update_display_config(self._fullscreen_checkbox.selected, h)
        self._goto_scene("previous")

    def render(self, surface):
        surface.fill((35, 25, 40))
        surface.blit(self._text_surface, (self._text_x, self._text_y))
        self._fullscreen_checkbox.render(surface)
        self._scale_checkbox.render(surface)
        self._fps_checkbox.render(surface)
        self.continue_bttn.render(surface)

    def update(self, delta_time):
        pass

    def handle_events(self, event):
        self._fullscreen_checkbox.handle_events(event)
        self._scale_checkbox.handle_events(event)
        self._fps_checkbox.handle_events(event)
        self.continue_bttn.handle_events(event)

        if event.type == pygame.KEYDOWN and event.key == pygame.K_ESCAPE:
            self._goto_scene("previous")


class EndMenu(GameScene):
    def __init__(self, goto_scene):
        self._goto_scene = goto_scene
        GameScene.__init__(self)
        Mouse.set_visible(True)
        w, h = 150, 50

        self._heading_text_surface = Font.get_render("Congratulations!!", size="big")
        self._heading_text_rect = self._heading_text_surface.get_rect()
        self._heading_text_x = (settings.SCREEN_WIDTH - self._heading_text_rect.width) // 2
        self._heading_text_y = self._heading_text_rect.height // 2

        self._text_surface = Font.get_render("You have completed your journey!", size="normal")
        self._text_rect = self._text_surface.get_rect()
        self._text_x = (settings.SCREEN_WIDTH - self._text_rect.width) // 2
        self._text_y = self._heading_text_rect.bottom + self._heading_text_rect.height

        self.start_menu_bttn = Button(((settings.SCREEN_WIDTH - w) // 2, self._text_rect.bottom + 200), (w, h), "Start Menu",
                                lambda: goto_scene("start_menu"))
        self.exit_bttn = Button(((settings.SCREEN_WIDTH - w) // 2, self._text_rect.bottom + 275), (w, h), "Quit",
                                lambda: goto_scene("quit"))

    def render(self, surface):
        surface.fill((35, 25, 40))
        surface.blit(self._heading_text_surface, (self._heading_text_x, self._heading_text_y))
        surface.blit(self._text_surface, (self._text_x, self._text_y))
        self.start_menu_bttn.render(surface)
        self.exit_bttn.render(surface)

    def update(self, delta_time):
        pass

    def handle_events(self, event):
        self.start_menu_bttn.handle_events(event)
        self.exit_bttn.handle_events(event)

        if event.type == pygame.KEYDOWN and (event.key == pygame.K_p or event.key == pygame.K_ESCAPE):
            self._goto_scene("start_menu")
