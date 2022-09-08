"""
Objects
"""
import os
import pygame


class Player(pygame.sprite.Sprite):
    """
    Spawn a player
    """

    def __init__(self):
        pygame.sprite.Sprite.__init__(self)
        self.images = []

        img = pygame.image.load(os.path.join('sprites', 'green-tank.png')).convert()
        self.images.append(img)
        self.size = self.images[0].get_size()
        self.image = pygame.transform.scale(self.images[0], (int(self.size[0]/4), int(self.size[1]/4)))
        self.rect = self.image.get_rect()