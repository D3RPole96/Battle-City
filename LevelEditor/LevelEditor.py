import pygame

import GameSettings


class LevelEditor:
    def __init__(self, screen):
        self.fps = GameSettings.GameSettings.fps
        self.screen_width = GameSettings.GameSettings.screen_width + GameSettings.GameSettings.info_width
        self.screen_height = GameSettings.GameSettings.screen_height
        self.rows = 26
        self.columns = 26
        self.tile_size = 25

        self.screen = screen
        self.surface = pygame.Surface((self.screen_width, self.screen_height))
        self.surface.fill((0, 0, 0))
        self.surface_box = self.screen.get_rect()
        self.clock = pygame.time.Clock()

        self.draw_grid()

        self.start_cycle()

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
            pygame.display.flip()
            self.clock.tick(self.fps)

    pygame.quit()
