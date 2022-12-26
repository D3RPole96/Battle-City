import copy

import Obstacle
from Eagle import Eagle
from GameObjects import GameObjects
import GameSettings


class ShovelBonus:
    def __init__(self):
        self.bonus_time_left = GameSettings.change_for_fps(600)

        eagle_x = GameObjects.instance.eagle.rect.x
        eagle_y = GameObjects.instance.eagle.rect.y

        bricks_to_delete = []

        for obstacle in GameObjects.instance.static_objects:
            if (abs(obstacle.rect.x - eagle_x) <= 30 or obstacle.rect.x - eagle_x == 60) \
                    and abs(obstacle.rect.y - eagle_y) <= 30 and not isinstance(obstacle, Eagle):
                bricks_to_delete.append(obstacle)

        for brick_to_delete in bricks_to_delete:
            cell = brick_to_delete.cell
            subcell_index = brick_to_delete.subcell_index
            concrete = Obstacle.Concrete(cell, subcell_index)
            concrete.rect.x = brick_to_delete.rect.x
            concrete.rect.y = brick_to_delete.rect.y

            brick_to_delete.destroy_block()

            GameObjects.instance.add_static_object(concrete)

    def is_bonus_ended(self):
        if self.bonus_time_left == 0:
            eagle_x = GameObjects.instance.eagle.rect.x
            eagle_y = GameObjects.instance.eagle.rect.y
            concretes_to_delete = []

            for obstacle in GameObjects.instance.static_objects:
                if (abs(obstacle.rect.x - eagle_x) <= 30 or obstacle.rect.x - eagle_x == 60) \
                        and abs(obstacle.rect.y - eagle_y) <= 30 and not isinstance(obstacle, Eagle):
                    concretes_to_delete.append(obstacle)

            for concrete_to_delete in concretes_to_delete:
                cell = concrete_to_delete.cell
                subcell_index = concrete_to_delete.subcell_index
                brick = Obstacle.Brick(cell, subcell_index)
                brick.rect.x = concrete_to_delete.rect.x
                brick.rect.y = concrete_to_delete.rect.y

                concrete_to_delete.destroy_block()

                GameObjects.instance.add_static_object(brick)

            return True

        self.bonus_time_left -= 1
        return False
