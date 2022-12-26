import os


class LevelsHandler:
    @staticmethod
    def get_levels_list():
        return os.listdir('Levels')