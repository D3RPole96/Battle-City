import GameSettings
import Tank
import GameObjects
import Strategy
import random


class Enemy(Tank.Tank):
    def __init__(self, bullet_level, armor_level, speed, spawn_cell):
        super().__init__(bullet_level, armor_level, speed, False)
        GameObjects.GameObjects.instance.enemies.append(self)
        self.target = (None, None)
        self.target_cell = None
        self.current_cell = spawn_cell

        self.strategy = Strategy.do_stupid_move
        self.ticks = 0
        self.ticks_before_chasing_player = GameSettings.change_for_fps(480)
        self.ticks_before_moving_to_eagle = GameSettings.change_for_fps(960)

    def handle_enemy(self):
        if self.target_cell is None:
            self.target_cell = self.strategy(self, self.current_cell)
            self.target = self.target_cell.get_cell_coordinates_for_tank()

        move_x = self.target[0] - self.rect.x
        move_y = self.target[1] - self.rect.y

        self.unset_move_x()
        self.unset_move_y()

        if move_x > 0 and abs(move_x) > abs(move_y):
            self.set_positive_move_x()
        if move_x < 0 and abs(move_x) > abs(move_y):
            self.set_negative_move_x()
        if move_y > 0 and abs(move_x) < abs(move_y):
            self.set_positive_move_y()
        if move_y < 0 and abs(move_x) < abs(move_y):
            self.set_negative_move_y()

        if random.randint(1, 100) == 1:
            self.shoot()

        if abs(move_x) < self.tank_speed and abs(move_y) < self.tank_speed:
            self.current_cell = self.target_cell
            self.target_cell = None
            self.target = (None, None)

        self.ticks += 1

        if self.ticks == self.ticks_before_chasing_player:
            self.strategy = Strategy.chase_player
        if self.ticks == self.ticks_before_moving_to_eagle:
            self.strategy = Strategy.move_to_eagle
