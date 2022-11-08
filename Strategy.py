import GameObjects
from random import choice


def do_stupid_move(tank, current_cell):
    available_cells = []
    cell_neighbours = current_cell.get_neighbours()

    for cell in cell_neighbours:
        if cell is None:
            continue
        if tank.bullet_level >= max(cell.required_bullet_level):
            available_cells.append(cell)

    return choice(available_cells)
