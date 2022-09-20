import os
import Obstacle
import GameObjects


class Generator:
    def __init__(self, level):
        self.path = os.path.join('Levels', f'{level}.txt')
        self.obstacles_dictionary = self.get_obstacles_dictionary()
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
                GameObjects.GameObjects.instance.add_static_object(block)

    def get_obstacles_dictionary(self):
        dict = {}
        dict['B'] = Obstacle.Brick

        return dict
