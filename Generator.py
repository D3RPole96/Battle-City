import os

import Eagle
import Obstacle
import GameObjects
import Enemy


def get_objects_dictionary():
    objects_dict = {'B': Obstacle.Brick, 'C': Obstacle.Concrete, 'W': Obstacle.Water,
                    'T': Obstacle.Trees, 'I': Obstacle.Ice, 'E': Enemy.Enemy, 'A': Eagle.Eagle}

    return objects_dict


class Generator:
    def __init__(self, level):
        self.path = os.path.join('Levels', f'{level}.txt')
        self.objects_dictionary = get_objects_dictionary()
        f = open(self.path, "r")
        lines = f.read().split('\n')
        for line_index in range(len(lines)):
            quarter_objects = lines[line_index].split(' ')
            for quarter_index in range(len(quarter_objects)):
                if quarter_objects[quarter_index] == '.':
                    continue

                cell = GameObjects.GameObjects.instance.cells[line_index // 2][quarter_index // 2]
                subsell_index = line_index % 2 * 2 + quarter_index % 2

                current_object = quarter_objects[quarter_index]

                if current_object == 'A':
                    obj = self.objects_dictionary[quarter_objects[quarter_index]]()
                    obj.rect.x = 30 * quarter_index
                    obj.rect.y = 30 * line_index
                elif current_object == 'E':
                    obj = self.objects_dictionary[quarter_objects[quarter_index]](1, 2, 2, cell)
                    obj.rect.x = 30 * quarter_index + 5
                    obj.rect.y = 30 * line_index + 5
                else:
                    obj = self.objects_dictionary[quarter_objects[quarter_index]](cell, subsell_index)
                    obj.rect.x = 30 * quarter_index
                    obj.rect.y = 30 * line_index

                layer = 'middle'
                if current_object in 'WI':
                    layer = 'back'
                if current_object == 'T':
                    layer = 'front'

                if current_object != 'E':
                    GameObjects.GameObjects.instance.add_static_object(obj, layer)

                cell.required_bullet_level[subsell_index] = \
                    2 if current_object == 'B' \
                    else (4 if current_object == 'C'
                          else (255 if current_object == 'W' else 0))
