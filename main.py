import pygame
import Player
pygame.init()

fps = 60

screen = pygame.display.set_mode([800, 800])
surface = pygame.Surface((800, 800))
surface.fill((0, 0, 0))
surfacebox = screen.get_rect()
clock = pygame.time.Clock()

player = Player.Player()   # spawn player
player.rect.x = 0   # go to x
player.rect.y = 0   # go to y
player_list = pygame.sprite.Group()
player_list.add(player)

running = True
while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_UP or event.key == ord('w'):
                print('up')
            if event.key == pygame.K_DOWN or event.key == ord('s'):
                print('down')
            if event.key == pygame.K_LEFT or event.key == ord('a'):
                print('left')
            if event.key == pygame.K_RIGHT or event.key == ord('d'):
                print('right')

        if event.type == pygame.KEYUP:
            if event.key == pygame.K_UP or event.key == ord('w'):
                print('up stop')
            if event.key == pygame.K_DOWN or event.key == ord('s'):
                print('down stop')
            if event.key == pygame.K_LEFT or event.key == ord('a'):
                print('left stop')
            if event.key == pygame.K_RIGHT or event.key == ord('d'):
                print('right stop')
            if event.key == ord('q'):
                running = False

    screen.blit(surface, surfacebox)
    player_list.draw(screen)
    pygame.display.flip()
    clock.tick(fps)

pygame.quit()