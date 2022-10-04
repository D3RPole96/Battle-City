def change_for_fps(number):
    return number * (60.0 / GameSettings.fps)


def change_for_screen_width(number):
    return number * (780 / GameSettings.screen_width)


def change_for_screen_height(number):
    return number * (780 / GameSettings.screen_height)


class GameSettings:
    screen_width = 780
    screen_height = 780
    fps = 60
