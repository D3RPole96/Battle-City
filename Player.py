from math import sqrt

import Tank
import GameSettings
import GameObjects


class Player(Tank.Tank):
    def __init__(self):
        super().__init__(1, 2, 2, True)
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
