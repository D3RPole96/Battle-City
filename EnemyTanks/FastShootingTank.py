import os

import pygame

from Direction import Direction
from Enemy import Enemy
import GameSettings
from GameObjects import GameObjects


class FastShootingTank(Enemy):
    def __init__(self, cell):
        super().__init__(2, 2, 2, cell)

        for i in Direction:
            img = pygame.image.load(os.path.join('sprites/Tanks/FastShootingTank', f'fast-shooting-tank-{i.name}.png')).convert()
            self.images.append(img)

        tank_side_size = GameSettings.get_tank_side_size()
        self.size = self.images[0].get_size()
        self.image = pygame.transform.scale(self.images[0], (GameSettings.change_for_screen_width(tank_side_size),
                                                             GameSettings.change_for_screen_height(tank_side_size)))
        self.rect = self.image.get_rect()
        self.image.set_colorkey((0, 0, 0))

        self.reload_time = GameSettings.change_for_fps(15)

        GameObjects.instance.add_tank(self)
