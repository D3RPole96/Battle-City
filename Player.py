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
        self.image = pygame.transform.scale(self.images[0], (50, 50))
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
        self.rect.x += self.move_x
        if self.move_x == 0:
            self.rect.y += self.move_y

        self.rect.x = min(780 - self.image.get_size()[0], self.rect.x)
        self.rect.x = max(0, self.rect.x)
        self.rect.y = min(780 - self.image.get_size()[1], self.rect.y)
        self.rect.y = max(0, self.rect.y)
