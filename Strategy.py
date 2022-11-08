import GameObjects
from random import choice


def do_stupid_move(tank, current_cell):
    return choice(get_available_neighbours(tank, current_cell))


def get_available_neighbours(tank, cell):
    available_cells = []
    cell_neighbours = cell.get_neighbours()

    for cell in cell_neighbours:
        if cell is None:
            continue
        if tank.bullet_level >= max(cell.required_bullet_level):
            available_cells.append(cell)

    return available_cells


def chase_player(tank, current_cell):
    player_cell = GameObjects.GameObjects.instance.player.get_nearest_cell()

    path = dijkstra(tank, current_cell, player_cell)

    next_cell = path[player_cell]

    while next_cell is not None and path[next_cell] != current_cell:
        next_cell = path[next_cell]

    if next_cell is None:
        return do_stupid_move(tank, current_cell)
    return next_cell


def dijkstra(tank, start_cell, end_cell):
    cells = GameObjects.GameObjects.instance.get_all_cells_in_list()

    dist = {}
    prev = {}
    queue = []
    for cell in cells:
        dist[cell] = 1e18
        prev[cell] = None
        queue.append(cell)
    dist[start_cell] = 0

    while len(queue) > 0:
        min_dist = 1e18
        current_cell = None

        for cell in queue:
            if dist[cell] < min_dist:
                min_dist = dist[cell]
                current_cell = cell

        if current_cell is None:
            break

        queue.remove(current_cell)

        for neighbour in get_available_neighbours(tank, current_cell):
            if neighbour not in queue:
                continue
            alt = dist[current_cell] + max(neighbour.required_bullet_level) + 1
            if alt < dist[neighbour]:
                dist[neighbour] = alt
                prev[neighbour] = current_cell

    return prev
