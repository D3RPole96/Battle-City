import json
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
        with open(f'Levels/{level}.json', 'r') as json_file:
            json_file = json.load(json_file)
            world_data = json_file[0]
            spawners = json_file[1]

        self.objects_dictionary = get_objects_dictionary()
        self.enemy_spawners = []
        self.enemy_spawners_cells = []
        for y in range(26):
            for x in range(26):
                if world_data[y][x] == '.':
                    continue

                cell = GameObjects.GameObjects.instance.cells[y // 2][x // 2]
                subsell_index = y % 2 * 2 + x % 2

                current_object = world_data[y][x]

                if current_object == 'A':
                    obj = self.objects_dictionary[world_data[y][x]]()
                    obj.rect.x = 30 * x
                    obj.rect.y = 30 * y
                elif current_object.isdigit():
                    while len(self.enemy_spawners) <= int(current_object):
                        self.enemy_spawners.append(None)
                        self.enemy_spawners_cells.append(None)
                    self.enemy_spawners[int(current_object)] = EnemySpawner(30 * x + 5, 30 * y + 5)
                    self.enemy_spawners_cells[int(current_object)] = cell
                else:
                    obj = self.objects_dictionary[world_data[y][x]](cell, subsell_index)
                    obj.rect.x = 30 * x
                    obj.rect.y = 30 * y

                layer = 'middle'
                if current_object == 'T':
                    layer = 'front'
                if current_object in 'WI':
                    layer = 'back'

                if not current_object.isdigit():
                    GameObjects.GameObjects.instance.add_static_object(obj, layer)

        for i in range(len(spawners)):
            enemy_spawner_index = int(spawners[i].split(' ')[0])
            enemies = spawners[i].split(' ')[1::2]
            ticks = spawners[i].split(' ')[2::2]
            for j in range(len(enemies)):
                self.enemy_spawners[enemy_spawner_index].add_enemy(ticks[j],
                                                                   self.objects_dictionary[enemies[j]],
                                                                   self.enemy_spawners_cells[enemy_spawner_index])

        GameObjects.GameObjects.instance.set_enemy_spawners(self.enemy_spawners)
