import os

import pygame
from Editor import Button

import GameSettings


class LevelEditor:
    def __init__(self, screen):
        self.fps = GameSettings.GameSettings.fps
        self.screen_width = GameSettings.GameSettings.screen_width + GameSettings.GameSettings.info_width
        self.screen_height = GameSettings.GameSettings.screen_height
        self.rows = 26
        self.columns = 26
        self.tile_size = 25
        self.tile_types = 7
        self.current_tile = 0

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
        for image in self.img_list:
            tile_button = Button.Button(self.columns * self.tile_size + (75 * button_col) + 40, 75 * button_row + 50, image, 1)
            self.button_list.append(tile_button)
            button_col += 1
            if button_col == 1:
                button_row += 1
                button_col = 0

    def draw_buttons(self):
        for button_count, button in enumerate(self.button_list):
            if button.draw(self.screen):
                self.current_tile = button_count

        pygame.draw.rect(self.screen, (255, 0, 0), self.button_list[self.current_tile], 3)

    def load_tiles_images(self):
        self.img_list = []

        img = pygame.image.load(os.path.join('sprites/Obstacles/Bricks', 'Brick15.png')).convert()
        img = pygame.transform.scale(img, (50, 50))
        img.set_colorkey((0, 0, 0))
        self.img_list.append(img)

        img = pygame.image.load(os.path.join('sprites/Obstacles/Concretes', 'Concrete.png')).convert()
        img = pygame.transform.scale(img, (50, 50))
        img.set_colorkey((0, 0, 0))
        self.img_list.append(img)

        img = pygame.image.load(os.path.join('sprites/Obstacles', 'Water.png')).convert()
        img = pygame.transform.scale(img, (50, 50))
        img.set_colorkey((0, 0, 0))
        self.img_list.append(img)

        img = pygame.image.load(os.path.join('sprites/Obstacles', 'Trees.png')).convert()
        img = pygame.transform.scale(img, (50, 50))
        img.set_colorkey((0, 0, 0))
        self.img_list.append(img)

        img = pygame.image.load(os.path.join('sprites/Obstacles', 'Ice.png')).convert()
        img = pygame.transform.scale(img, (50, 50))
        img.set_colorkey((0, 0, 0))
        self.img_list.append(img)

        img = pygame.image.load(os.path.join('sprites', 'Eagle.png')).convert()
        img = pygame.transform.scale(img, (50, 50))
        img.set_colorkey((0, 0, 0))
        self.img_list.append(img)

        img = pygame.image.load(os.path.join('sprites', 'SpawnerSprite.png')).convert()
        img = pygame.transform.scale(img, (50, 50))
        img.set_colorkey((0, 0, 0))
        self.img_list.append(img)

    def draw_grid(self):
        # vertical lines
        for c in range(self.columns + 1):
            pygame.draw.line(self.screen, (80, 80, 80), (c * self.tile_size, 0), (c * self.tile_size, self.screen_height))
        # horizontal lines
        for c in range(self.rows + 1):
            pygame.draw.line(self.screen, (80, 80, 80), (0, c * self.tile_size), (self.screen_width, c * self.tile_size))

    def start_cycle(self):
        running = True
        while running:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    running = False

                if event.type == pygame.KEYDOWN:
                    if event.key == pygame.MOUSEBUTTONDOWN:
                        self.player.set_negative_move_y()

            self.screen.blit(self.surface, self.surface_box)
            self.draw_grid()
            self.draw_rectangles()
            self.draw_buttons()
            pygame.display.flip()
            self.clock.tick(self.fps)

    pygame.quit()
