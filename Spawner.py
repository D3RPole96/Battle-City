from Cell import Cell


class EnemySpawner:
    def __init__(self, x, y):
        self.x = x
        self.y = y
        self.enemydict = {}

    def add_enemy(self, time, enemy_caller, cell):
        self.enemydict[int(time)] = (enemy_caller, cell)

    def try_spawn_enemy(self, tick):
        if tick in self.enemydict:
            enemy = self.enemydict[tick][0](self.enemydict[tick][1])
            enemy.rect.x = self.x
            enemy.rect.y = self.y
