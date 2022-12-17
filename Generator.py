import os

import Eagle
import Obstacle
import GameObjects
import Enemy
import EnemyTanks.HeavyTank
import EnemyTanks.FastTank
import EnemyTanks.FastShootingTank
from Spawner import EnemySpawner


def get_objects_dictionary():
    objects_dict = {'B': Obstacle.Brick, 'C': Obstacle.Concrete, 'W': Obstacle.Water,
                    'T': Obstacle.Trees, 'I': Obstacle.Ice, 'H': EnemyTanks.HeavyTank.HeavyTank,
                    'F': EnemyTanks.FastTank.FastTank, 'S': EnemyTanks.FastShootingTank.FastShootingTank,
                    'A': Eagle.Eagle}

    return objects_dict


class Generator:
    def __init__(self, level):
        self.path = os.path.join('Levels', f'{level}.txt')
        self.objects_dictionary = get_objects_dictionary()
        self.enemy_spawners = []
        self.enemy_spawners_cells = []
        f = open(self.path, "r")
        lines = f.read().split('\n')
        for line_index in range(26):
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
                elif current_object.isdigit():
                    while len(self.enemy_spawners) <= int(current_object):
                        self.enemy_spawners.append(None)
                        self.enemy_spawners_cells.append(None)
                    # enemy_caller = lambda: self.objects_dictionary[quarter_objects[quarter_index]](cell)
                    self.enemy_spawners[int(current_object)] = EnemySpawner(30 * quarter_index + 5, 30 * line_index + 5)
                    self.enemy_spawners_cells[int(current_object)] = cell
                else:
                    obj = self.objects_dictionary[quarter_objects[quarter_index]](cell, subsell_index)
                    obj.rect.x = 30 * quarter_index
                    obj.rect.y = 30 * line_index

                layer = 'middle'
                if current_object == 'T':
                    layer = 'front'
                if current_object in 'WI':
                    layer = 'back'

                if not current_object.isdigit():
                    GameObjects.GameObjects.instance.add_static_object(obj, layer)

                cell.required_bullet_level[subsell_index] = \
                    2 if current_object == 'B' \
                        else (4 if current_object == 'C'
                              else (255 if current_object == 'W' else 0))

        for line_index in range(26, len(lines)):
            enemy_spawner_index = int(lines[line_index].split(' ')[0])
            enemies = lines[line_index].split(' ')[1::2]
            ticks = lines[line_index].split(' ')[2::2]
            for i in range(len(enemies)):
                self.enemy_spawners[enemy_spawner_index].add_enemy(ticks[i],
                                                                   self.objects_dictionary[enemies[i]],
                                                                   self.enemy_spawners_cells[enemy_spawner_index])

        GameObjects.GameObjects.instance.set_enemy_spawners(self.enemy_spawners)
