import os

import pygame.sprite
import GameObjects
import Direction


class Bullet(pygame.sprite.Sprite):
    def __init__(self, x, y, direction):
        pygame.sprite.Sprite.__init__(self)

        self.move_x = 0
        self.move_y = 0
        self.previous_x, self.previous_y = 0, 0
        self.direction = direction

        self.collision_type = 2

        image = pygame.image.load(os.path.join('sprites/Bullet', f'bullet-{direction.name}.png')).convert()

        self.size = image.get_size()
        if self.direction == Direction.Direction.right or self.direction == Direction.Direction.left:
            self.image = pygame.transform.scale(image, (15, 10))
        else:
            self.image = pygame.transform.scale(image, (10, 15))
        self.rect = self.image.get_rect()
        self.rect.x = x
        self.rect.y = y

        GameObjects.GameObjects.instance.add_bullet(self)
