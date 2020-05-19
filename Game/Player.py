import pygame
import os
from .Physics import RigidBody
from .Animation import Animation, AnimatedSprite
from .UI import Font
from . import settings


class Player(RigidBody, pygame.sprite.Sprite):
    class State:
        idle = 0
        walking = 1
        running = 2
        jumping = 3
        falling = 4
        ledge_grabbing = 5
        climbing = 6
        climbing_static = 7

    textures = None
    sounds = None

    @staticmethod
    def _load_resources():
        player_folder = os.path.join(settings.img_folder, 'Jungle Asset Pack', 'character_edited')
        if Player.textures is None:
            print("loading player textures")
            Player.textures = {
                'player-idle': pygame.image.load(os.path.join(player_folder, 'idle outline big.png')).convert_alpha(),
                'player-run': pygame.image.load(os.path.join(player_folder, 'run outline big.png')).convert_alpha(),
                'player-jump': pygame.image.load(os.path.join(player_folder, 'jump outline big.png')).convert_alpha(),
                'player-fall': pygame.image.load(os.path.join(player_folder, 'mid air outline.png')).convert_alpha(),
                'player-ledge': pygame.image.load(os.path.join(player_folder, 'ledge grab outline big.png')).convert_alpha(),
                'player-climb': pygame.image.load(os.path.join(player_folder, 'climb outline big.png')).convert_alpha(),
            }
        if Player.sounds is None:
            Player.sounds = {
                'jump': pygame.mixer.Sound(os.path.join(settings.music_folder, 'jump.wav')),
                'hurt': pygame.mixer.Sound(os.path.join(settings.music_folder, 'Sound_1.wav')),
            }
            Player.sounds['jump'].set_volume(0.25)
            Player.sounds['hurt'].set_volume(0.3)

    def __init__(self, spawn_point, groups):
        self._load_resources()

        self.state = self.State.idle
        self.animation = Animation()
        self.animation.add(self.State.idle, Player.textures['player-idle'], 12, 8, 'right', offset=(-4, -3))
        self.animation.add(self.State.walking, Player.textures['player-run'], 8, 10, 'right', offset=(-4, -3))
        self.animation.add(self.State.jumping, Player.textures['player-jump'], 1, 1, 'right', offset=(-4, -3))
        self.animation.add(self.State.falling, Player.textures['player-fall'], 2, 6, 'right', offset=(-4, -3))
        self.animation.add(self.State.ledge_grabbing, Player.textures['player-ledge'], 6, 8, 'right', loop=False, offset=(-2, -10))
        self.animation.add(self.State.climbing, Player.textures['player-climb'], 2, 6, 'right', offset=(-4, -3))
        self.animation.add(self.State.climbing_static, Player.textures['player-climb'], 2, 6, 'right', loop=False, offset=(-4, -3))

        self._layer = 2
        RigidBody.__init__(self, *spawn_point, 24, 50)

        self.pushable = False
        pygame.sprite.Sprite.__init__(self, groups)

        self.jump_speed = settings.PLAYER_JUMP_SPEED
        self.walk_speed = settings.PLAYER_WALK_SPEED
        self.climb_speed = settings.PLAYER_WALK_SPEED*2//3
        self.can_jump = True
        self.facing = self.animation.sprites[self.state].default_facing

        self.coins = 0
        self._max_health = 5
        self.health = self._max_health
        self._invincible_timer = 0
        self._invincible_time = 3

        self.ledge_grabbing = False
        self._ledge_grab_checker = None  # will be made later
        self._ledge_ground_checker = None  # will be made later

        self.climbing = False

    def set_pos(self, pos):
        self.rect.topleft = pos

    def _get_input(self):
        self.v_x = 0
        if self.climbing:
            self.v_y = 0
        keys = pygame.key.get_pressed()
        if keys[pygame.K_SPACE]:
            self.jump()
        if keys[pygame.K_UP] or keys[pygame.K_w]:
            if self.climbing:
                self.v_y = -self.climb_speed
        elif keys[pygame.K_DOWN] or keys[pygame.K_s]:
            if self.climbing:
                self.v_y = +self.climb_speed
            elif self.ledge_grabbing:
                self.ledge_grabbing = False
                self.v_y = 0

        if (keys[pygame.K_LEFT] or keys[pygame.K_a]) and not self.ledge_grabbing:
            self.v_x += -1
        elif (keys[pygame.K_RIGHT] or keys[pygame.K_d]) and not self.ledge_grabbing:
            self.v_x += 1

        if self.v_x < 0 and self.facing != 'left':
            self.facing = 'left'
        if self.v_x > 0 and self.facing != 'right':
            self.facing = 'right'

        self.v_x *= self.walk_speed

    def jump(self):
        if self.can_jump:
            Player.sounds['jump'].play()
            self.v_y = -self.jump_speed
            self.can_jump = False
            self.ledge_grabbing = False
            self.climbing = False

    def do_physics(self, delta_time, map):
        colliding = RigidBody.do_physics(self, delta_time, map.collidables, no_gravity=(self.ledge_grabbing or self.climbing))
        if colliding['bottom']:
            self.can_jump = True

        self._ledge_grab(colliding, map.collidables)
        self._ladder_climb(map.ladders)

        return colliding

    def _ladder_climb(self, ladders):
        keys = pygame.key.get_pressed()
        key_pressed = keys[pygame.K_UP] or keys[pygame.K_w] or keys[pygame.K_DOWN] or keys[pygame.K_s]
        on_ladder = False
        for ladder in ladders:
            if self.rect.colliderect(ladder) and ladder.left <= self.rect.centerx <= ladder.right:
                on_ladder = True
                break

        if not self.climbing:
            if on_ladder and key_pressed:
                self.climbing = True
                self.can_jump = True
                self.ledge_grabbing = False
        elif self.climbing and not on_ladder:
            self.climbing = False

    def _ledge_grab(self, colliding, collidables):
        x = (self.rect.left - 3) if self.facing == 'left' else (self.rect.right + 3)
        self._ledge_grab_checker = (x, self.rect.top - 8)
        self._ledge_ground_checker = (x, self.rect.top + 8)
        if not (self.ledge_grabbing or self.climbing):
            if colliding[self.facing] and (not self._obstacle_check(self._ledge_grab_checker, collidables)) and \
                    self._obstacle_check(self._ledge_ground_checker, collidables):
                self.ledge_grabbing = True
                self.can_jump = True
                self.v_y = 0
        elif self.ledge_grabbing:
            if not self._obstacle_check(self._ledge_ground_checker, collidables):
                self.ledge_grabbing = False
                self.v_y = 0

    def _obstacle_check(self, pt, collidables):
        for obs in collidables:
            if obs.rect.collidepoint(pt):
                return True
        return False

    def _change_states(self):
        if self.climbing:
            if abs(self.v_y) != 0:
                self.state = self.State.climbing
            else:
                self.state = self.State.climbing_static
        elif self.ledge_grabbing:
            self.state = self.State.ledge_grabbing
        elif self.v_y < 0:
            self.state = self.State.jumping
        elif self.v_y > 100:
            self.state = self.State.falling
            self.can_jump = False
        else:
            if abs(self.v_x) > 0 and self.state != self.State.walking:
                self.state = self.State.walking
            elif abs(self.v_x) == 0 and self.state != self.State.idle:
                self.state = self.State.idle

    def _mob_collision(self, mob_group):
        mobs = pygame.sprite.spritecollide(self, mob_group, False)
        for mob in mobs:
            if mob.state != mob.State.dying:
                # mob stomp
                if (self.v_y >= 0) and (self.rect.bottom <= (mob.rect.top + mob.rect.height//2)):
                    mob.kill()
                    self.can_jump = True
                    self.jump()
                elif self._invincible_timer == 0:
                    self.hurt()

    def hurt(self, health_points=1):
        if self._invincible_timer == 0:
            self.health -= health_points
            self.sounds["hurt"].play()
            print("Player health reduced to", self.health)
            self._invincible_timer = self._invincible_time

    def _coin_collision(self, coin_group):
        coins = pygame.sprite.spritecollide(self, coin_group, False)
        for coin in coins:
            coin.pickup()
            self.coins += 1

    def _spikes_collision(self, spikes_list):
        for spikes in spikes_list:
            if self.rect.colliderect(spikes):
                self.hurt()

    def update(self, delta_time, map, mob_group, coin_group):
        if self._invincible_timer > 0:
            self._invincible_timer -= delta_time
            if self._invincible_timer < 0:
                self._invincible_timer = 0
        self._mob_collision(mob_group)
        self._coin_collision(coin_group)
        self._spikes_collision(map.spikes)

        self._get_input()
        self.do_physics(delta_time, map)
        self._change_states()
        self.animation.play(self.state, delta_time)

    def render(self, surface, camera):
        self.animation.render(surface, camera.get_relative_rect(self.rect), self.facing, self._invincible_timer)

        RigidBody.render(self, surface, camera)

        if settings.DEBUG_DRAW:
            Font.put_text(surface, ['idle', 'walk', 'run', 'jump', 'fall', 'ledge', 'climb', 'climb-s'][self.state],
                          camera.get_relative_pos(self.rect.left, self.rect.top - 32), (0, 255, 255))

            if self._ledge_grab_checker is not None and self._ledge_ground_checker is not None:
                pygame.draw.circle(surface, (255, 255, 0), camera.get_relative_pos(*self._ledge_grab_checker), 3)
                pygame.draw.circle(surface, (0, 255, 255), camera.get_relative_pos(*self._ledge_ground_checker), 3)


