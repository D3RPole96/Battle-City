import os
from math import sqrt

import pygame
import GameObjects


class Eagle(pygame.sprite.Sprite):
    def __init__(self):
        pygame.sprite.Sprite.__init__(self)

        img = pygame.image.load(os.path.join('sprites', 'Eagle.png')).convert()
        self.image = pygame.transform.scale(img, (60, 60))
        self.rect = self.image.get_rect()
        self.image.set_colorkey((0, 0, 0))

        self.collision_type = 1

        GameObjects.GameObjects.instance.set_eagle(self)

    def get_nearest_cell(self):
        nearest_cell = None
        shortest_distance = 1e18
        for cell in GameObjects.GameObjects.instance.get_all_cells_in_list():
            cell_coordinates = cell.get_cell_coordinates_for_tank()
            distance_to_cell = sqrt((cell_coordinates[0] - self.rect.x + 30) ** 2 + (cell_coordinates[1] - self.rect.y) ** 2)
            if distance_to_cell < shortest_distance:
                nearest_cell = cell
                shortest_distance = distance_to_cell

        return nearest_cell

    def collider_with_bullet(self, bullet):
        if True:
            self.destroy_eagle()

        return True

    def destroy_eagle(self):
        self.kill()
        # Game Over screen here
