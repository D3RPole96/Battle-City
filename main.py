from collections import defaultdict

import pygame
from pygame_menu import Theme

import Direction
import Player
import Tank
import Generator
import GameObjects
import GameSettings
import pygame_menu
import PickableBonuses.PickableShovelBonus
from Editor.LevelEditor import LevelEditor
from LevelsHandler import LevelsHandler

from Bonuses.ShovelBonus import ShovelBonus


class Menu:
    def __init__(self):
        self.screen_width = GameSettings.GameSettings.screen_width + GameSettings.GameSettings.info_width
        self.screen_height = GameSettings.GameSettings.screen_height
        self.screen = pygame.display.set_mode([self.screen_width, self.screen_height])

        mytheme = Theme(background_color=(0, 0, 0, 0),  # transparent background
                        title_background_color=(0, 0, 0, 255),
                        title_font_shadow=True,
                        widget_padding=25)

        menu = pygame_menu.Menu('Battle City', self.screen_width, self.screen_height,
                                theme=mytheme)
        #menu.add.text_input('Player name: ', default='Player')
        levels = LevelsHandler.get_levels_list()
        for level in levels:
            level_name = level[:level.rfind('.')]
            menu.add.button(level_name, Game, level_name, self.screen)

        menu.add.button('Level Editor', LevelEditor, self.screen)
        menu.add.button('Exit', pygame_menu.events.EXIT)
        pygame.display.set_caption('Battle City')
        menu.mainloop(self.screen)


class Game:
    def __init__(self, level, screen):
        self.fps = GameSettings.GameSettings.fps
        self.screen_width = GameSettings.GameSettings.screen_width + GameSettings.GameSettings.info_width
        self.screen_height = GameSettings.GameSettings.screen_height

        self.game_objects = GameObjects.GameObjects.instance = GameObjects.GameObjects()
        self.game_objects.available_bonuses = [PickableBonuses.PickableShovelBonus.PickableShovelBonus]

        self.screen = screen
        self.surface = pygame.Surface((self.screen_width, self.screen_height))
        self.surface.fill((0, 0, 0))
        self.surface_box = self.screen.get_rect()
        self.clock = pygame.time.Clock()

        self.generator = Generator.Generator(level)

        self.player = Player.Player()
        self.player.rect.x = 0
        self.player.rect.y = 0

        self.start_cycle()

    def start_cycle(self):
        running = True
        while running:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    running = False

                if event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_UP or event.key == ord('w'):
                        self.player.set_negative_move_y()
                    if event.key == pygame.K_DOWN or event.key == ord('s'):
                        self.player.set_positive_move_y()
                    if event.key == pygame.K_LEFT or event.key == ord('a'):
                        self.player.set_negative_move_x()
                    if event.key == pygame.K_RIGHT or event.key == ord('d'):
                        self.player.set_positive_move_x()
                    if event.key == pygame.K_SPACE:
                        self.player.shoot()

                if event.type == pygame.KEYUP:
                    if event.key == pygame.K_UP or event.key == ord('w') \
                            or event.key == pygame.K_DOWN or event.key == ord('s'):
                        self.player.unset_move_y()
                    if event.key == pygame.K_LEFT or event.key == ord('a') \
                            or event.key == pygame.K_RIGHT or event.key == ord('d'):
                        self.player.unset_move_x()
                    if event.key == ord('q'):
                        running = False

            self.screen.blit(self.surface, self.surface_box)
            self.game_objects.draw_sprite_groups(self.screen)
            pygame.display.flip()
            self.clock.tick(self.fps)
            self.player.update()

            self.game_objects.handle()

    pygame.quit()


if __name__ == "__main__":
    pygame.init()

    game = Menu()
