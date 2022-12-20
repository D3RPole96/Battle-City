import random

import pygame

import Cell
import Obstacle
import GameSettings
from Spawner import EnemySpawner


class GameObjects:
    instance = None

    def __init__(self):
        self.interface_sprite_group = pygame.sprite.Group()
        self.front_sprite_group = pygame.sprite.Group()
        self.middle_sprite_group = pygame.sprite.Group()
        self.back_sprite_group = pygame.sprite.Group()

        self.cells = self.init_cells_list()

        self.dynamic_objects = []
        self.static_objects = []
        self.enemies = []
        self.bullets = []
        self.enemy_spawners = []
        self.player = None
        self.eagle = None
        self.ticks = 0

        self.available_bonuses = []
        self.pickable_bonuses = []
        self.bonuses = []

    def draw_sprite_groups(self, screen):
        self.back_sprite_group.draw(screen)
        self.middle_sprite_group.draw(screen)
        self.front_sprite_group.draw(screen)

        pygame.draw.rect(screen, (116, 116, 116), pygame.Rect(GameSettings.GameSettings.screen_width,
                                                              0,
                                                              GameSettings.GameSettings.screen_width +
                                                              GameSettings.GameSettings.info_width,
                                                              GameSettings.GameSettings.screen_height))
        self.interface_sprite_group.draw(screen)

    def handle(self):
        self.handle_pickable_bonuses()
        self.handle_bonuses()
        self.handle_spawners()
        self.handle_enemies()
        self.check_dynamic_objects_for_collision()
        self.check_bullets_for_collision()
        self.move_bullets()
        self.ticks += 1

        if self.ticks % GameSettings.change_for_fps(900) == 0:
            self.spawn_pickable_bonus()

    def spawn_pickable_bonus(self):
        pickable_bonus = random.choice(self.available_bonuses)()
        pickable_bonus.rect.x = random.randint(0, GameSettings.GameSettings.screen_width - 60)
        pickable_bonus.rect.y = random.randint(0, GameSettings.GameSettings.screen_height - 60)
        pickable_bonus.rect.x = 0
        pickable_bonus.rect.y = 0
        self.front_sprite_group.add(pickable_bonus)
        self.pickable_bonuses.append(pickable_bonus)


    def set_enemy_spawners(self, enemy_spawners):
        self.enemy_spawners = enemy_spawners

    def init_cells_list(self):
        cells = []

        for i in range(13):
            line = []
            for j in range(13):
                cell = Cell.Cell(j * GameSettings.get_cell_side_size(), i * GameSettings.get_cell_side_size())
                line.append(cell)
            cells.append(line)

        for i in range(13):
            for j in range(13):
                if i != 0:
                    cells[i][j].top_cell = cells[i - 1][j]
                if j != 12:
                    cells[i][j].right_cell = cells[i][j + 1]
                if i != 12:
                    cells[i][j].bottom_cell = cells[i + 1][j]
                if j != 0:
                    cells[i][j].left_cell = cells[i][j - 1]

        return cells

    def get_all_cells_in_list(self):
        cells = []
        for line in self.cells:
            for cell in line:
                cells.append(cell)

        return cells

    def add_tank(self, tank):
        self.dynamic_objects.append(tank)
        self.middle_sprite_group.add(tank)

    def set_player(self, player):
        self.player = player

    def set_eagle(self, eagle):
        self.eagle = eagle

    def handle_pickable_bonuses(self):
        picked_bonuses = []
        for pickable_bonus in self.pickable_bonuses:
            if self.player.rect.colliderect(pickable_bonus.rect):
                picked_bonuses.append(pickable_bonus)
                self.bonuses.append(pickable_bonus.bonus_caller())

            pickable_bonus.remaining_time -= 1
            if pickable_bonus.remaining_time == 0:
                picked_bonuses.append(pickable_bonus)

        for picked_bonus in picked_bonuses:
            self.pickable_bonuses.remove(picked_bonus)
            picked_bonus.kill()

    def handle_bonuses(self):
        ended_bonuses = []
        for bonus in self.bonuses:
            if bonus.is_bonus_ended():
                ended_bonuses.append(bonus)

        for ended_bonus in ended_bonuses:
            self.bonuses.remove(ended_bonus)

    def handle_enemies(self):
        for enemy in self.enemies:
            enemy.handle_enemy()
            enemy.update()

    def handle_spawners(self):
        for spawner in self.enemy_spawners:
            spawner.try_spawn_enemy(self.ticks)

    def add_static_object(self, game_object, layer='middle'):
        if layer == 'interface':
            self.interface_sprite_group.add(game_object)
        if layer == 'front':
            self.front_sprite_group.add(game_object)
        if layer == 'middle':
            self.middle_sprite_group.add(game_object)
        if layer == 'back':
            self.back_sprite_group.add(game_object)
        self.static_objects.append(game_object)

    def add_bullet(self, bullet):
        self.middle_sprite_group.add(bullet)
        self.bullets.append(bullet)

    def get_all_objects(self):
        return self.dynamic_objects + self.static_objects + self.bullets

    def check_dynamic_objects_for_collision(self):
        for dynamic_object in self.dynamic_objects:
            for game_object in self.get_all_objects():
                if dynamic_object == game_object:
                    continue
                if dynamic_object.rect.colliderect(game_object.rect) and game_object.collision_type == 1:
                    dynamic_object.undo_move()
                if dynamic_object.rect.colliderect(game_object.rect) and game_object.collision_type == 2:
                    dynamic_object.collider_with_bullet(game_object)

    def check_bullets_for_collision(self):
        did_bullet_hit = False
        for bullet in self.bullets:
            hit_object = []
            for static_object in self.static_objects:
                if static_object.rect.colliderect(bullet.rect):
                    did_bullet_hit = static_object.collider_with_bullet(bullet) or did_bullet_hit
                    hit_object.append(static_object)
            if did_bullet_hit:
                for static_object in self.static_objects:
                    if static_object not in hit_object and static_object != self.eagle:
                        static_object.collider_with_bullet(bullet)
            if did_bullet_hit:
                bullet.destroy_bullet()
            did_bullet_hit = False

    def is_player_on_ice(self):
        for ice_object in list(filter(lambda static_object:
                                      isinstance(static_object, Obstacle.Ice), self.static_objects)):
            if ice_object.collider_with_player():
                return True

        return False

    def move_bullets(self):
        for bullet in self.bullets:
            bullet.move_bullet()
            bullet.is_bullet_behind_screen()
