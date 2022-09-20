import os
import pygame

from Obstacle import Obstacle


class Brick(pygame.sprite.Sprite):
    def __init__(self):
        pygame.sprite.Sprite.__init__(self)
        self.images = []

        self.collision_type = 1

        for i in range(1, 16):
            img = pygame.image.load(os.path.join('sprites/Bricks', f'Brick{i}.png')).convert()
            self.images.append(img)
        self.size = self.images[14].get_size()
        self.image = pygame.transform.scale(self.images[14], (30, 30))
        self.rect = self.image.get_rect()