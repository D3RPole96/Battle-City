import enum
import os
import pygame

import Bullet
import Direction
import GameSettings
import GameObjects


class Player(pygame.sprite.Sprite):
    def __init__(self):
        pygame.sprite.Sprite.__init__(self)
        self.images = []

        self.move_x = 0
        self.move_y = 0
        self.frame = 0
        self.previous_x, self.previous_y = 0, 0
        self.direction = Direction.Direction.up
        self.reload_time = 0

        self.collision_type = 1

        for i in Direction.Direction:
            img = pygame.image.load(os.path.join('sprites/Tanks', f'green-tank-{i.name}.png')).convert()
            self.images.append(img)

        self.size = self.images[0].get_size()
        self.image = pygame.transform.scale(self.images[0], (GameSettings.change_for_screen_width(50),
                                                             GameSettings.change_for_screen_height(50)))
        self.rect = self.image.get_rect()
        self.image.set_colorkey((0, 0, 0))

        GameObjects.GameObjects.instance.set_player(self)

    def control(self, x, y):
        self.move_x = x
        self.move_y = y

    def update(self):
        self.previous_x, self.previous_y = self.rect.x, self.rect.y
        self.move_player()

        self.rect.x = min(780 - self.image.get_size()[0], self.rect.x)
        self.rect.x = max(0, self.rect.x)
        self.rect.y = min(780 - self.image.get_size()[1], self.rect.y)
        self.rect.y = max(0, self.rect.y)

        self.reload_time -= 1
        self.reload_time = max(0, self.reload_time)

    def move_player(self):
        self.rect.x += self.move_x
        if self.move_x == 0:
            self.rect.y += self.move_y

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

    def undo_move(self):
        self.rect.x, self.rect.y = self.previous_x, self.previous_y

    def shoot(self):
        if self.reload_time > 0:
            return
        if self.direction == Direction.Direction.up:
            Bullet.Bullet(self.rect.x + 20, self.rect.y - 21, self.direction, True)
        if self.direction == Direction.Direction.right:
            Bullet.Bullet(self.rect.x + 51, self.rect.y + 20, self.direction, True)
        if self.direction == Direction.Direction.down:
            Bullet.Bullet(self.rect.x + 20, self.rect.y + 51, self.direction, True)
        if self.direction == Direction.Direction.left:
            Bullet.Bullet(self.rect.x - 21, self.rect.y + 20, self.direction, True)
        self.reload_time = GameSettings.GameSettings.fps * 2

    def collider_with_bullet(self, bullet):
        if bullet.is_bullet_friendly:
            return
