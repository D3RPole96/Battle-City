import enum
import os
import pygame

import Bullet
import Direction
import GameSettings
import GameObjects


class Tank(pygame.sprite.Sprite):
    def __init__(self, bullet_level, armor_level, speed, is_tank_player):
        pygame.sprite.Sprite.__init__(self)
        self.images = []

        self.move_x = 0
        self.move_y = 0
        self.frame = 0
        self.previous_x, self.previous_y, self.previous_move_x, self.previous_move_y = 0, 0, 0, 0
        self.direction = Direction.Direction.down
        self.reload_time = 0

        self.bullet_level = bullet_level
        self.armor_level = armor_level
        self.tank_speed = GameSettings.change_for_fps(speed)
        self.is_tank_player = is_tank_player

        self.sliding_time = GameSettings.change_for_fps(20)
        self.sliding_time_remaining = 0
        self.did_slide = False
        self.slide_x, self.slide_y = 0, 0

        self.collision_type = 1

        for i in Direction.Direction:
            img = pygame.image.load(os.path.join('sprites/Tanks', f'green-tank-{i.name}.png')).convert()
            self.images.append(img)

        tank_side_size = GameSettings.get_tank_side_size()
        self.size = self.images[0].get_size()
        self.image = pygame.transform.scale(self.images[0], (GameSettings.change_for_screen_width(tank_side_size),
                                                             GameSettings.change_for_screen_height(tank_side_size)))
        self.rect = self.image.get_rect()
        self.image.set_colorkey((0, 0, 0))

        GameObjects.GameObjects.instance.add_tank(self)

    def control(self, x, y):
        self.move_x = x
        self.move_y = y

    def set_positive_move_x(self):
        self.move_x = self.tank_speed

    def set_negative_move_x(self):
        self.move_x = -self.tank_speed

    def set_positive_move_y(self):
        self.move_y = self.tank_speed

    def set_negative_move_y(self):
        self.move_y = -self.tank_speed

    def unset_move_x(self):
        self.move_x = 0

    def unset_move_y(self):
        self.move_y = 0

    def update(self):
        if self.sliding_time_remaining == 0 \
                and GameObjects.GameObjects.instance.is_player_on_ice() \
                and self.move_x == self.move_y == 0 \
                and (self.previous_move_x != 0 or self.previous_move_y != 0) \
                and not self.did_slide:
            self.sliding_time_remaining = self.sliding_time
            self.did_slide = True
            self.slide_x = self.previous_move_x
            self.slide_y = self.previous_move_y

        if self.move_x != 0 or self.move_y != 0 or not GameObjects.GameObjects.instance.is_player_on_ice():
            self.sliding_time_remaining = 0
            self.did_slide = False


        self.previous_x, self.previous_y = self.rect.x, self.rect.y
        self.move_player()

        self.rect.x = min(780 - self.image.get_size()[0], self.rect.x)
        self.rect.x = max(0, self.rect.x)
        self.rect.y = min(780 - self.image.get_size()[1], self.rect.y)
        self.rect.y = max(0, self.rect.y)

        self.reload_time -= 1
        self.reload_time = max(0, self.reload_time)

    def move_player(self):
        if self.sliding_time_remaining != 0:
            self.rect.x += self.slide_x
            self.rect.y += self.slide_y
            self.sliding_time_remaining -= 1
            return

        self.rect.x += self.move_x
        self.previous_move_x = self.move_x
        self.previous_move_y = 0
        if self.move_x == 0:
            self.rect.y += self.move_y
            self.previous_move_y = self.move_y

        self.set_direction()

    def set_direction(self):
        if self.rect.x - self.previous_x > 0:
            self.direction = Direction.Direction.right
        if self.rect.x - self.previous_x < 0:
            self.direction = Direction.Direction.left
        if self.rect.y - self.previous_y > 0:
            self.direction = Direction.Direction.down
        if self.rect.y - self.previous_y < 0:
            self.direction = Direction.Direction.up

        self.image = pygame.transform.scale(self.images[self.direction.value], (50, 50))
        self.image.set_colorkey((0, 0, 0))

    def undo_move(self):
        self.rect.x, self.rect.y = self.previous_x, self.previous_y

    def shoot(self):
        if self.reload_time > 0:
            return
        if self.direction == Direction.Direction.up:
            Bullet.Bullet(self.rect.x + 20, self.rect.y - 11, self.direction, self.is_tank_player, self.bullet_level)
        if self.direction == Direction.Direction.right:
            Bullet.Bullet(self.rect.x + 41, self.rect.y + 20, self.direction, self.is_tank_player, self.bullet_level)
        if self.direction == Direction.Direction.down:
            Bullet.Bullet(self.rect.x + 20, self.rect.y + 41, self.direction, self.is_tank_player, self.bullet_level)
        if self.direction == Direction.Direction.left:
            Bullet.Bullet(self.rect.x - 11, self.rect.y + 20, self.direction, self.is_tank_player, self.bullet_level)
        self.reload_time = GameSettings.change_for_fps(10)

    def collider_with_bullet(self, bullet):
        if (bullet.is_bullet_friendly and not self.is_tank_player) \
                or (not bullet.is_bullet_friendly and self.is_tank_player):
            GameObjects.GameObjects.instance.dynamic_objects.remove(self)
            if not self.is_tank_player:
                GameObjects.GameObjects.instance.enemies.remove(self)
            else:
                GameObjects.GameObjects.instance.player = None
            bullet.destroy_bullet()
            self.kill()
