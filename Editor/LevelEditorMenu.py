import pygame
import pygame_menu
from pygame_menu import Theme

from GameSettings import GameSettings
from LevelsHandler import LevelsHandler


class LevelEditorMenu:
    def __init__(self, level_editor_caller):
        self.screen_width = GameSettings.screen_width + GameSettings.info_width
        self.screen_height = GameSettings.screen_height
        self.screen = pygame.display.set_mode([self.screen_width, self.screen_height])

        mytheme = Theme(background_color=(0, 0, 0, 0),
                        title_background_color=(0, 0, 0, 255),
                        title_font_shadow=True,
                        widget_padding=25)

        menu = pygame_menu.Menu('Level picker', self.screen_width, self.screen_height,
                                theme=mytheme)
        levels = LevelsHandler.get_levels_list()
        for level in levels:
            level_name = level[:level.rfind('.')]
            menu.add.button(level_name, level_editor_caller, self.screen, level)
        menu.add.button('Exit', pygame_menu.events.EXIT)
        pygame.display.set_caption('Battle City')
        menu.mainloop(self.screen)