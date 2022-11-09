import math

import GameObjects
from random import choice


def do_stupid_move(tank, current_cell):
    return choice(get_available_neighbours(tank, current_cell))


def chase_player(tank, current_cell):
    return move_to_object_cell(tank, current_cell, GameObjects.GameObjects.instance.player)


def move_to_eagle(tank, current_cell):
    return move_to_object_cell(tank, current_cell, GameObjects.GameObjects.instance.eagle)


def get_available_neighbours(tank, cell):
    available_cells = []
    cell_neighbours = cell.get_neighbours()

    for cell in cell_neighbours:
        if cell is None:
            continue
        if tank.bullet_level >= max(cell.required_bullet_level):
            available_cells.append(cell)

    return available_cells


def move_to_object_cell(tank, current_cell, obj):
    obj_cell = obj.get_nearest_cell()

    path = dijkstra(tank, current_cell, obj_cell)

    next_cell = path[obj_cell]

    while next_cell is not None and path[next_cell] != current_cell:
        next_cell = path[next_cell]

    if next_cell is None:
        return move_to_object_direction(tank, current_cell, obj)

    return next_cell


def move_to_object_direction(tank, current_cell, obj):
    angle = math.atan2(-(obj.rect.y - tank.rect.y), obj.rect.x - tank.rect.x)

    if abs(angle) <= math.pi / 4:
        return current_cell.right_cell
    if math.pi / 4 < angle < 3 * math.pi / 4:
        return current_cell.top_cell
    if -3 * math.pi / 4 < angle < -math.pi / 4:
        return current_cell.bottom_cell
    if abs(angle) >= 3 * math.pi / 4:
        return current_cell.left_cell


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
