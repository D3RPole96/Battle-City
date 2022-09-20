from collections import defaultdict

import pygame
import Player
import Generator
import GameObjects


class Game:
    def __init__(self, level):
        self.game_objects = GameObjects.GameObjects.instance = GameObjects.GameObjects()

        self.screen = pygame.display.set_mode([780, 780])
        self.surface = pygame.Surface((780, 780))
        self.surface.fill((0, 0, 0))
        self.surfacebox = self.screen.get_rect()
        self.clock = pygame.time.Clock()
        self.fps = 60

        self.generator = Generator.Generator(1)

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

            self.screen.blit(self.surface, self.surfacebox)
            self.game_objects.sprite_group.draw(self.screen)
            pygame.display.flip()
            self.clock.tick(self.fps)
            self.player.update()
            self.game_objects.check_for_collision()
            print(self.player.rect.x, self.player.rect.y, sep=' ')

    pygame.quit()


pygame.init()

game = Game(0)
