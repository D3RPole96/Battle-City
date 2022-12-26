import json
import os
import random

import pygame
from Editor import Button
from Editor.LevelEditorMenu import LevelEditorMenu

import GameSettings
from LevelsHandler import LevelsHandler


class LevelEditor:
    def __init__(self, screen, load_file=None):
        self.fps = GameSettings.GameSettings.fps
        self.file_name = None
        self.screen_width = GameSettings.GameSettings.screen_width + GameSettings.GameSettings.info_width
        self.screen_height = GameSettings.GameSettings.screen_height
        self.rows = 26
        self.columns = 26
        self.tile_size = 25
        self.tile_types = 7
        self.current_tile = 0
        self.keys = ['B', 'C', 'W', 'T', 'I', 'A', 'S']
        self.spawners_strategies = ['H 240 S 900', 'S 340 F 670', 'H 490 F 840']

        if load_file is None:
            self.world_data = []
            for row in range(self.rows):
                r = ['.'] * self.columns
                self.world_data.append(r)
            self.spawners = []
        else:
            with open(f'Levels/{load_file}', 'r') as json_file:
                self.file_name = load_file
                load_file_json = json.load(json_file)

            json_world_data = load_file_json[0]
            for y in range(len(json_world_data)):
                row = json_world_data[y]
                for x in range(len(row)):
                    if json_world_data[y][x].isdigit():
                        json_world_data[y][x] = 'S'
            self.world_data = json_world_data

            json_spawners = []
            for i in range(len(json_spawners)):
                json_spawners[i] = json_spawners[json_spawners[i].find(' ') + 1:]

            self.spawners = json_spawners

        self.init_file_buttons()

        self.screen = screen
        self.surface = pygame.Surface((self.screen_width, self.screen_height))
        self.surface.fill((0, 0, 0))
        self.surface_box = self.screen.get_rect()
        self.clock = pygame.time.Clock()

        self.load_tiles_images()
        self.make_buttons_list()
        self.draw_grid()

        self.start_cycle()

    def draw_rectangles(self):
        pygame.draw.rect(self.screen, (116, 116, 116), (0, self.rows * self.tile_size, self.screen_width, self.screen_height))
        pygame.draw.rect(self.screen, (116, 116, 116), (self.columns * self.tile_size, 0, self.screen_width, self.screen_height))

    def make_buttons_list(self):
        self.button_list = []
        button_col = 0
        button_row = 0
        for key in self.keys:
            tile_button = Button.Button(self.columns * self.tile_size + (75 * button_col) + 40, 75 * button_row + 50, self.img_dict[key], 1)
            self.button_list.append(tile_button)
            button_col += 1
            if button_col == 1:
                button_row += 1
                button_col = 0

    def init_file_buttons(self):
        save_img = pygame.image.load(os.path.join('sprites', 'SaveButton.png')).convert_alpha()
        save_img = pygame.transform.scale(save_img, (80, 80))

        load_img = pygame.image.load(os.path.join('sprites', 'LoadButton.png')).convert_alpha()
        load_img = pygame.transform.scale(load_img, (80, 80))

        self.save_button = Button.Button(self.screen_width / 2 - 80, self.screen_height - 100, save_img, 1)
        self.load_button = Button.Button(self.screen_width / 2 + 80, self.screen_height - 100, load_img, 1)

    def draw_buttons(self):
        for button_count, button in enumerate(self.button_list):
            if button.draw(self.screen):
                self.current_tile = button_count

        pygame.draw.rect(self.screen, (255, 0, 0), self.button_list[self.current_tile], 3)

    def draw_save_button(self):
        if self.save_button.draw(self.screen):
            world_data_to_json = []
            spawners = 0
            for y in range(len(self.world_data)):
                row = self.world_data[y]
                world_data_to_json.append([])
                for x in range(len(row)):
                    world_data_to_json[y].append(row[x])
                    if world_data_to_json[y][x] == 'S':
                        world_data_to_json[y][x] = str(spawners)
                        spawners += 1

            spawners_to_json = []
            for i in range(len(self.spawners)):
                spawner_str = str(self.spawners[i])
                spawners_to_json.append(str(i) + ' ' + spawner_str)
            list_to_json = [world_data_to_json, spawners_to_json]
            if self.file_name is None:
                new_level_name_number = 1
                for level_name in LevelsHandler.get_levels_list():
                    if 'User level' in level_name:
                        new_level_name_number += 1
                self.file_name = f'User level {new_level_name_number}.json'
            with open(f'Levels/{self.file_name}', 'w') as json_file:
                json.dump(list_to_json, json_file)

    def draw_load_button(self):
        if self.load_button.draw(self.screen):
            LevelEditorMenu(LevelEditor)

    def load_tiles_images(self):
        self.img_dict = {}

        img = pygame.image.load(os.path.join('sprites/Obstacles/Bricks', 'Brick15.png')).convert()
        img = pygame.transform.scale(img, (50, 50))
        img.set_colorkey((0, 0, 0))
        self.img_dict['B'] = img

        img = pygame.image.load(os.path.join('sprites/Obstacles/Concretes', 'Concrete.png')).convert()
        img = pygame.transform.scale(img, (50, 50))
        img.set_colorkey((0, 0, 0))
        self.img_dict['C'] = img

        img = pygame.image.load(os.path.join('sprites/Obstacles', 'Water.png')).convert()
        img = pygame.transform.scale(img, (50, 50))
        img.set_colorkey((0, 0, 0))
        self.img_dict['W'] = img

        img = pygame.image.load(os.path.join('sprites/Obstacles', 'Trees.png')).convert()
        img = pygame.transform.scale(img, (50, 50))
        img.set_colorkey((0, 0, 0))
        self.img_dict['T'] = img

        img = pygame.image.load(os.path.join('sprites/Obstacles', 'Ice.png')).convert()
        img = pygame.transform.scale(img, (50, 50))
        img.set_colorkey((0, 0, 0))
        self.img_dict['I'] = img

        img = pygame.image.load(os.path.join('sprites', 'Eagle.png')).convert()
        img = pygame.transform.scale(img, (50, 50))
        img.set_colorkey((0, 0, 0))
        self.img_dict['A'] = img

        img = pygame.image.load(os.path.join('sprites', 'SpawnerSprite.png')).convert()
        img = pygame.transform.scale(img, (50, 50))
        img.set_colorkey((0, 0, 0))
        self.img_dict['S'] = img

    def draw_grid(self):
        # vertical lines
        for c in range(self.columns + 1):
            pygame.draw.line(self.screen, (80, 80, 80), (c * self.tile_size, 0), (c * self.tile_size, self.screen_height))
        # horizontal lines
        for c in range(self.rows + 1):
            pygame.draw.line(self.screen, (80, 80, 80), (0, c * self.tile_size), (self.screen_width, c * self.tile_size))

    def draw_world(self):
        for y in range(len(self.world_data)):
            row = self.world_data[y]
            for x in range(len(row)):
                tile = row[x]
                if tile != '.':
                    img = self.img_dict[tile]
                    if tile not in 'AS':
                        img = pygame.transform.scale(img, (self.tile_size, self.tile_size))
                    else:
                        img = pygame.transform.scale(img, (self.tile_size * 2, self.tile_size * 2))
                    self.screen.blit(img, (x * self.tile_size, y * self.tile_size))

    def start_cycle(self):
        running = True
        while running:
            pos = pygame.mouse.get_pos()
            x = pos[0] // self.tile_size
            y = pos[1] // self.tile_size

            if pos[0] < self.columns * self.tile_size and pos[1] < self.rows * self.tile_size:
                if pygame.mouse.get_pressed()[0] == 1:
                    if self.world_data[y][x] != self.keys[self.current_tile]:
                        if self.world_data[y][x] == 'S':
                            self.spawners.pop()
                        self.world_data[y][x] = self.keys[self.current_tile]
                        if self.world_data[y][x] == 'S':
                            self.spawners.append(self.spawners_strategies[random.randint(0, len(self.spawners_strategies) - 1)])
                if pygame.mouse.get_pressed()[2] == 1:
                    self.world_data[y][x] = '.'

            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    running = False

            self.screen.blit(self.surface, self.surface_box)
            self.draw_world()
            self.draw_grid()
            self.draw_rectangles()

            self.draw_buttons()
            self.draw_save_button()
            self.draw_load_button()

            pygame.display.flip()
            self.clock.tick(self.fps)

    pygame.quit()
