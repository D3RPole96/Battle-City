import pygame
import Player
pygame.init()

fps = 60

screen = pygame.display.set_mode([780, 780])
surface = pygame.Surface((780, 780))
surface.fill((0, 0, 0))
surfacebox = screen.get_rect()
clock = pygame.time.Clock()

player = Player.Player()   # spawn player
player.rect.x = 0   # go to x
player.rect.y = 0   # go to y
player_speed = 2
player_list = pygame.sprite.Group()
player_list.add(player)

running = True
while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_UP or event.key == ord('w'):
                player.control(0, -player_speed)
            if event.key == pygame.K_DOWN or event.key == ord('s'):
                player.control(0, player_speed)
            if event.key == pygame.K_LEFT or event.key == ord('a'):
                player.control(-player_speed, 0)
            if event.key == pygame.K_RIGHT or event.key == ord('d'):
                player.control(player_speed, 0)

        if event.type == pygame.KEYUP:
            if event.key == pygame.K_UP or event.key == ord('w'):
                player.control(0, player_speed)
            if event.key == pygame.K_DOWN or event.key == ord('s'):
                player.control(0, -player_speed)
            if event.key == pygame.K_LEFT or event.key == ord('a'):
                player.control(player_speed, 0)
            if event.key == pygame.K_RIGHT or event.key == ord('d'):
                player.control(-player_speed, 0)
            if event.key == ord('q'):
                running = False

    screen.blit(surface, surfacebox)
    player_list.draw(screen)
    pygame.display.flip()
    clock.tick(fps)
    player.update()
    print(player.rect.x, player.rect.y, sep=' ')

pygame.quit()