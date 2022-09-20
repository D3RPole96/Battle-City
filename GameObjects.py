import pygame


class GameObjects:
    instance = None

    def __init__(self):
        self.dynamic_objects = []
        self.static_objects = []
        self.enemies = []
        self.bullets = []

    def set_player(self, player):
        self.dynamic_objects.append(player)
        self.player = player

    def add_static_object(self, game_object):
        self.static_objects.append(game_object)

    def get_all_objects(self):
        return self.dynamic_objects + self.static_objects

    def check_for_collision(self):
        for dynamic_object in self.dynamic_objects:
            for game_object in self.get_all_objects():
                if dynamic_object == game_object:
                    continue
                if dynamic_object.rect.colliderect(game_object.rect) and game_object.collision_type == 1:
                    dynamic_object.undo_move()
