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
                block = self.obstacles_dictionary[quarter_blocks[quarter_index]]()
                block.rect.x = 30 * quarter_index
                block.rect.y = 30 * line_index
                layer = 'middle'
                if quarter_blocks[quarter_index] in 'WI':
                    layer = 'back'
                if quarter_blocks[quarter_index] == 'T':
                    layer = 'front'
                GameObjects.GameObjects.instance.add_static_object(block, layer)
