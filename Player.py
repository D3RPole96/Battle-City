import Tank
import GameSettings


class Player(Tank.Tank):
    def __init__(self):
        super().__init__()

        self.bullet_level = 2
        self.armor_level = 1
        self.tank_speed = GameSettings.change_for_fps(2)
        self.is_tank_player = True
