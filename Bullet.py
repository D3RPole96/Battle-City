import os

import pygame

import GameSettings
import GameObjects
import Direction


class Bullet(pygame.sprite.Sprite):
    def __init__(self, x, y, direction, is_bullet_friendly):
        pygame.sprite.Sprite.__init__(self)

        self.bullet_speed = GameSettings.change_for_fps(4)

        self.move_x = 0
        self.move_y = 0
        self.previous_x, self.previous_y = 0, 0
        self.direction = direction

        self.collision_type = 2

        image = pygame.image.load(os.path.join('sprites/Bullet', f'bullet-{direction.name}.png')).convert()

        self.size = image.get_size()
        if self.direction == Direction.Direction.right or self.direction == Direction.Direction.left:
            self.image = pygame.transform.scale(image, (GameSettings.change_for_screen_width(15),
                                                        GameSettings.change_for_screen_height(10)))
        else:
            self.image = pygame.transform.scale(image, (GameSettings.change_for_screen_width(10),
                                                        GameSettings.change_for_screen_height(15)))

        self.image.set_colorkey((0, 0, 0))

        self.rect = self.image.get_rect()
        self.rect.x = x
        self.rect.y = y

        self.is_bullet_friendly = is_bullet_friendly

        GameObjects.GameObjects.instance.add_bullet(self)

    def move_bullet(self):
        if self.direction == Direction.Direction.up:
            self.rect.y -= self.bullet_speed
        if self.direction == Direction.Direction.right:
            self.rect.x += self.bullet_speed
        if self.direction == Direction.Direction.down:
            self.rect.y += self.bullet_speed
        if self.direction == Direction.Direction.left:
            self.rect.x -= self.bullet_speed

    def is_bullet_behind_screen(self):
        if self.rect.x < 0 - self.rect.size[0] \
                or self.rect.x > GameSettings.GameSettings.screen_width \
                or self.rect.y < 0 - self.rect.size[1] \
                or self.rect.y > GameSettings.GameSettings.screen_height:
            self.destroy_bullet()
            return True
        return False

    def destroy_bullet(self):
        GameObjects.GameObjects.instance.bullets.remove(self)
        self.kill()
