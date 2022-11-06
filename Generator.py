import os
import Obstacle
import GameObjects


def get_obstacles_dictionary():
    obstacles_dict = {'B': Obstacle.Brick, 'C': Obstacle.Concrete, 'W': Obstacle.Water,
                      'T': Obstacle.Trees, 'I': Obstacle.Ice}

    return obstacles_dict


class Generator:
    def __init__(self, level):
        self.path = os.path.join('Levels', f'{level}.txt')
        self.obstacles_dictionary = get_obstacles_dictionary()
        f = open(self.path, "r")
        lines = f.read().split('\n')
        for line_index in range(len(lines)):
            quarter_blocks = lines[line_index].split(' ')
            for quarter_index in range(len(quarter_blocks)):
                if quarter_blocks[quarter_index] == '.':
                    continue

                cell = GameObjects.GameObjects.instance.cells[line_index // 2][quarter_index // 2]
                subsell_index = line_index % 2 * 2 + quarter_index % 2

                block = self.obstacles_dictionary[quarter_blocks[quarter_index]](cell, subsell_index)
                block.rect.x = 30 * quarter_index
                block.rect.y = 30 * line_index

                current_obstacle = quarter_blocks[quarter_index]

                layer = 'middle'
                if current_obstacle in 'WI':
                    layer = 'back'
                if current_obstacle == 'T':
                    layer = 'front'
                GameObjects.GameObjects.instance.add_static_object(block, layer)

                cell.required_bullet_level[subsell_index] = \
                    2 if current_obstacle == 'B' \
                    else (4 if current_obstacle == 'C'
                          else (255 if current_obstacle == 'W' else 0))
