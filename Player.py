import os
import pygame


class Player(pygame.sprite.Sprite):
    """
    Spawn a player
    """

    def __init__(self):
        pygame.sprite.Sprite.__init__(self)
        self.images = []

        self.move_x = 0  # move along X
        self.move_y = 0  # move along Y
        self.frame = 0  # count frames

        img = pygame.image.load(os.path.join('sprites', 'green-tank.png')).convert()
        self.images.append(img)
        self.size = self.images[0].get_size()
        self.image = pygame.transform.scale(self.images[0], (int(self.size[0] / 4), int(self.size[1] / 4)))
        self.rect = self.image.get_rect()

    """
    Control player movement
    """

    def control(self, x, y):
        self.move_x += x
        self.move_y += y

    """
    Update sprite position
    """

    def update(self):
        self.rect.x = self.rect.x + self.move_x