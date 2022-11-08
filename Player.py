import Tank
import GameSettings


class Player(Tank.Tank):
    def __init__(self):
        super().__init__(2, 1, 2, True)
