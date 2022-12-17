import os
from math import sqrt

import pygame

import Direction
import Tank
import GameSettings
import GameObjects


class Player(Tank.Tank):
    def __init__(self):
        super().__init__(1, 2, 2, True)

        for i in Direction.Direction:
            img = pygame.image.load(os.path.join('sprites/Tanks', f'green-tank-{i.name}.png')).convert()
            self.images.append(img)

        tank_side_size = GameSettings.get_tank_side_size()
        self.size = self.images[0].get_size()
        self.image = pygame.transform.scale(self.images[0], (GameSettings.change_for_screen_width(tank_side_size),
                                                             GameSettings.change_for_screen_height(tank_side_size)))
        self.rect = self.image.get_rect()
        self.image.set_colorkey((0, 0, 0))

        self.reload_time = GameSettings.change_for_fps(30)

        GameObjects.GameObjects.instance.add_tank(self)

        GameObjects.GameObjects.instance.set_player(self)

    def get_nearest_cell(self):
        nearest_cell = None
        shortest_distance = 1e18
        for cell in GameObjects.GameObjects.instance.get_all_cells_in_list():
            cell_coordinates = cell.get_cell_coordinates_for_tank()
            distance_to_cell = sqrt((cell_coordinates[0] - self.rect.x)**2 + (cell_coordinates[1] - self.rect.y)**2)
            if distance_to_cell < shortest_distance:
                nearest_cell = cell
                shortest_distance = distance_to_cell

        return nearest_cell
