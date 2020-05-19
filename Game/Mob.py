from .Physics import RigidBody
from .Animation import Animation
from .settings import *
from . import settings
import pygame
import random
import os
from .UI import Font


class Mob(RigidBody, pygame.sprite.Sprite):
    class State:
        idle = 0
        walking = 1
        running = 2
        jumping = 3
        falling = 4
        dying = 5

    textures = None
    death_sound = None

    @staticmethod
    def _load_textures():

        if Mob.textures is None:
            print("loading mob textures")
            Mob.textures = {
                'enemy-idle': pygame.image.load(
                    os.path.join(settings.img_folder, "Pixel Adventure",
                                 "Enemies/AngryPig/Idle (36x30) pink.png")).convert_alpha(),
                'enemy-walk': pygame.image.load(
                    os.path.join(settings.img_folder, "Pixel Adventure",
                                 "Enemies/AngryPig/Walk (36x30) pink.png")).convert_alpha(),
                'enemy-die': pygame.image.load(
                    os.path.join(settings.img_folder, "Pixel Adventure",
                                 "Enemies/AngryPig/Die (36x30).png")).convert_alpha(),
            }

        if Mob.death_sound is None:
            Mob.death_sound = pygame.mixer.Sound(os.path.join(settings.music_folder, 'Sound_2.wav'))
            Mob.death_sound.set_volume(0.3)

    def __init__(self, spawn_point, groups):
        self._load_textures()
        self.state = self.State.idle
        self.animation = Animation()
        self.animation.add(self.State.idle, Mob.textures['enemy-idle'], 9, 8, 'left', offset=(-4, -5))
        self.animation.add(self.State.walking, Mob.textures['enemy-walk'], 16, 25, 'left', offset=(-4, -5))
        self.animation.add(self.State.jumping, Mob.textures['enemy-idle'], 9, 8, 'left', offset=(-4, -5))
        self.animation.add(self.State.falling, Mob.textures['enemy-idle'], 9, 8, 'left', offset=(-4, -5))
        self.animation.add(self.State.dying, Mob.textures['enemy-die'], 7, 16, 'left', loop=False, offset=(-4, -5))

        self._layer = 1
        RigidBody.__init__(self, *spawn_point, 28, 25)
        
        self.pushable = False
        pygame.sprite.Sprite.__init__(self, groups)

        self.jump_speed = PLAYER_JUMP_SPEED
        self.walk_speed = PLAYER_WALK_SPEED * 2 / 3
        self.jumping = True

        self.facing = self.animation.sprites[self.state].default_facing
        self._ground_checker = None

    def _ground_check(self, pt, collidables):
        for obs in collidables:
            if obs.rect.collidepoint(pt):
                return True
        return False

    def _ai(self, colliding, collidables):
        x = (self.rect.left - 8) if self.facing == 'left' else (self.rect.right + 8)
        self._ground_checker = (int(x), int(self.rect.bottom + 8))
        if self.state == self.State.walking:
            if self.facing == 'left' and (colliding['left'] or not self._ground_check(self._ground_checker, collidables)):
                self.v_x = self.walk_speed
            elif self.facing == 'right' and (colliding['right'] or not self._ground_check(self._ground_checker, collidables)):
                self.v_x = -self.walk_speed

        if self.state == self.State.idle:
            if random.randint(0, 10) == 5:
                self.v_x = self.walk_speed

    def jump(self):
        if not self.jumping:
            self.v_y -= self.jump_speed
            self.jumping = True

    def do_physics(self, delta_time, collidables):
        colliding = RigidBody.do_physics(self, delta_time, collidables)
        if self.jumping and colliding['bottom']:
            self.jumping = False

        return colliding

    def _change_states(self):
        if self.state != self.State.dying:
            if self.jumping:
                if self.state != self.State.jumping:
                    self.state = self.State.jumping
            elif abs(self.v_x) > 0 and self.state != self.State.walking:
                self.state = self.State.walking
            elif abs(self.v_x) == 0 and self.state != self.State.idle:
                self.state = self.State.idle

        if self.v_x < 0 and self.facing != 'left':
            self.facing = 'left'
        if self.v_x > 0 and self.facing != 'right':
            self.facing = 'right'

    def _spikes_collision(self, spikes_list):
        for spikes in spikes_list:
            if self.rect.colliderect(spikes):
                self.kill()
                break

    def update(self, delta_time, map):
        if self.state != self.State.dying:
            colliding = self.do_physics(delta_time, map.collidables)
            self._ai(colliding, map.collidables)
            self._change_states()
            self._spikes_collision(map.spikes)
        else:
            self.kill()     # to finish animation and kill sprite

        self.animation.play(self.state, delta_time)

    def kill(self):
        if self.state != self.State.dying:
            self.state = self.State.dying
            self.death_sound.play()
            print(self, "Mob died")

        elif self.animation.is_over():
            pygame.sprite.Sprite.kill(self)
            print(self, "Mob sprite killed")

    def render(self, surface, camera):
        self.animation.render(surface, camera.get_relative_rect(self.rect), self.facing)
        RigidBody.render(self, surface, camera)

        if settings.DEBUG_DRAW:
            if self._ground_checker is not None:
                pygame.draw.circle(surface, (255, 255, 0), camera.get_relative_pos(*self._ground_checker), 3)

            Font.put_text(surface, ['idle', 'walk', 'run', 'jump', 'fall', 'dying'][self.state],
                          camera.get_relative_pos(self.rect.left, self.rect.top-32), (0, 255, 255))

