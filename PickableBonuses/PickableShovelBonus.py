import os

import pygame

import GameSettings
from Bonuses.ShovelBonus import ShovelBonus


class PickableShovelBonus(pygame.sprite.Sprite):
    def __init__(self):
        pygame.sprite.Sprite.__init__(self)
        img = pygame.image.load(os.path.join('sprites/Bonuses', f'shovel.png')).convert()

        self.image = pygame.transform.scale(img, (60, 60))
        self.rect = self.image.get_rect()
        #self.image.set_colorkey((0, 0, 0))
        self.remaining_time = GameSettings.change_for_fps(600)

        self.bonus_caller = ShovelBonus
