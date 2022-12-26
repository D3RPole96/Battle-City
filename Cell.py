import GameSettings


class Cell:
    def __init__(self, x, y):
        self.required_bullet_level = [0, 0, 0, 0]
        (self.top_cell, self.right_cell, self.bottom_cell, self.left_cell) = (None, None, None, None)
        self.x = x
        self.y = y

    def get_neighbours(self):
        return [self.top_cell, self.right_cell, self.bottom_cell, self.left_cell]

    def get_cell_coordinates_for_tank(self):
        return (abs(GameSettings.get_cell_side_size() - GameSettings.get_tank_side_size()) / 2 + self.x,
                self.y + abs(GameSettings.get_cell_side_size() - GameSettings.get_tank_side_size()) / 2)
