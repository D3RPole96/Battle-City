from collections import defaultdict

import pygame
import Player
import Generator
import GameObjects
import GameSettings


class Game:
    def __init__(self, level):
        self.fps = GameSettings.GameSettings.fps
        self.screen_width = GameSettings.GameSettings.screen_width
        self.screen_height = GameSettings.GameSettings.screen_height

        self.game_objects = GameObjects.GameObjects.instance = GameObjects.GameObjects()

        self.screen = pygame.display.set_mode([self.screen_width, self.screen_height])
        self.surface = pygame.Surface((self.screen_width, self.screen_height))
        self.surface.fill((0, 0, 0))
        self.surface_box = self.screen.get_rect()
        self.clock = pygame.time.Clock()

        self.generator = Generator.Generator(level)

        self.player = Player.Player()
        self.player.rect.x = 0
        self.player.rect.y = 0
        self.player_speed = 2 * (60 / self.fps)

        self.start_cycle()

    def start_cycle(self):
        running = True
        while running:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    running = False

                if event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_UP or event.key == ord('w'):
                        self.player.control(self.player.move_x, -self.player_speed)
                    if event.key == pygame.K_DOWN or event.key == ord('s'):
                        self.player.control(self.player.move_x, self.player_speed)
                    if event.key == pygame.K_LEFT or event.key == ord('a'):
                        self.player.control(-self.player_speed, self.player.move_y)
                    if event.key == pygame.K_RIGHT or event.key == ord('d'):
                        self.player.control(self.player_speed, self.player.move_y)
                    if event.key == pygame.K_SPACE:
                        self.player.shoot()

                if event.type == pygame.KEYUP:
                    if event.key == pygame.K_UP or event.key == ord('w'):
                        self.player.control(self.player.move_x, 0)
                    if event.key == pygame.K_DOWN or event.key == ord('s'):
                        self.player.control(self.player.move_x, 0)
                    if event.key == pygame.K_LEFT or event.key == ord('a'):
                        self.player.control(0, self.player.move_y)
                    if event.key == pygame.K_RIGHT or event.key == ord('d'):
                        self.player.control(0, self.player.move_y)
                    if event.key == ord('q'):
                        running = False

            self.screen.blit(self.surface, self.surface_box)
            self.game_objects.back_sprite_group.draw(self.screen)
            self.game_objects.middle_sprite_group.draw(self.screen)
            self.game_objects.front_sprite_group.draw(self.screen)
            self.game_objects.interface_sprite_group.draw(self.screen)
            pygame.display.flip()
            self.clock.tick(self.fps)
            self.player.update()

            self.game_objects.check_for_collision()
            self.game_objects.move_bullets()

    pygame.quit()


pygame.init()

game = Game('test')
