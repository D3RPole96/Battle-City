from collections import defaultdict

import pygame
import Player
import Generator


class Game:
    def __init__(self, level):
        self.screen = pygame.display.set_mode([780, 780])
        self.surface = pygame.Surface((780, 780))
        self.surface.fill((0, 0, 0))
        self.surfacebox = self.screen.get_rect()
        self.clock = pygame.time.Clock()
        self.fps = 60

        generator = Generator.Generator(1)
        self.player = Player.Player()  # spawn player
        self.player.rect.x = 0  # go to x
        self.player.rect.y = 0  # go to y
        self.player_speed = 2 * (60 / self.fps)
        self.draw_list = pygame.sprite.Group()
        self.draw_list.add(self.player)
        for obstacle in generator.obstacles:
            self.draw_list.add(obstacle)

        self.start_cycle()

    def start_cycle(self):
        running = True
        while running:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    running = False

                if event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_UP or event.key == ord('w'):
                        self.player.control(0, -self.player_speed)
                    if event.key == pygame.K_DOWN or event.key == ord('s'):
                        self.player.control(0, self.player_speed)
                    if event.key == pygame.K_LEFT or event.key == ord('a'):
                        self.player.control(-self.player_speed, 0)
                    if event.key == pygame.K_RIGHT or event.key == ord('d'):
                        self.player.control(self.player_speed, 0)

                if event.type == pygame.KEYUP:
                    if event.key == pygame.K_UP or event.key == ord('w'):
                        self.player.control(0, self.player_speed)
                    if event.key == pygame.K_DOWN or event.key == ord('s'):
                        self.player.control(0, -self.player_speed)
                    if event.key == pygame.K_LEFT or event.key == ord('a'):
                        self.player.control(self.player_speed, 0)
                    if event.key == pygame.K_RIGHT or event.key == ord('d'):
                        self.player.control(-self.player_speed, 0)
                    if event.key == ord('q'):
                        running = False

            self.screen.blit(self.surface, self.surfacebox)
            self.draw_list.draw(self.screen)
            pygame.display.flip()
            self.clock.tick(self.fps)
            self.player.update()
            print(self.player.rect.x, self.player.rect.y, sep=' ')

    pygame.quit()


pygame.init()

game = Game(0)
