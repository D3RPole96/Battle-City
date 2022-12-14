import os
import pygame

import Direction
import GameObjects


class Obstacle:
    def __init__(self, collision_type, x, y):
        self.collision_type = collision_type
        self.x = x
        self.y = y


def is_rectangles_overlap(rect1, rect2):
    left = max(rect1[0], rect2[0])
    top = max(rect1[1], rect2[1])
    right = min(rect1[2], rect2[2])
    bottom = min(rect1[3], rect2[3])

    width = right - left
    height = bottom - top

    return not (width < 0 or height < 0)


class Brick(pygame.sprite.Sprite):
    def __init__(self, cell, subcell_index):
        pygame.sprite.Sprite.__init__(self)
        self.images = []

        self.obstacle_state = [1, 1, 1, 1]

        self.collision_type = 1

        for i in range(1, 16):
            img = pygame.image.load(os.path.join('sprites/Obstacles/Bricks', f'Brick{i}.png')).convert()
            self.images.append(img)
        self.size = self.images[14].get_size()
        self.image = pygame.transform.scale(self.images[14], (30, 30))
        self.rect = self.image.get_rect()
        self.image.set_colorkey((0, 0, 0))

        self.cell = cell
        self.subcell_index = subcell_index
        self.cell.required_bullet_level[self.subcell_index] = 2

    def update_sprite(self):
        str = f"{self.obstacle_state[0]}{self.obstacle_state[1]}{self.obstacle_state[2]}{self.obstacle_state[3]}"

        if str == '0000':
            self.destroy_block()
        else:
            self.image = pygame.transform.scale(self.images[int(str, 2) - 1],
                                                (self.image.get_width(), self.image.get_width()))
            self.image.set_colorkey((0, 0, 0))

    def collider_with_bullet(self, bullet):
        if bullet.direction == Direction.Direction.up or bullet.direction == Direction.Direction.down:
            bullet_rect = [bullet.rect.x - 14, bullet.rect.y,
                           bullet.rect.x + bullet.rect.width + 14, bullet.rect.y + bullet.rect.height]
        else:
            bullet_rect = [bullet.rect.x, bullet.rect.y - 14,
                           bullet.rect.x + bullet.rect.width, bullet.rect.y + bullet.rect.height + 14]

        self.top_left_brick_rect = [self.rect.x, self.rect.y,
                                    self.rect.x + self.rect.width / 2, self.rect.y + self.rect.height / 2]

        self.top_right_brick_rect = [self.rect.x + self.rect.width / 2, self.rect.y,
                                     self.rect.x + self.rect.width, self.rect.y + self.rect.height / 2]

        self.bottom_left_brick_rect = [self.rect.x, self.rect.y + self.rect.height / 2,
                                       self.rect.x + self.rect.width / 2, self.rect.y + self.rect.height]

        self.bottom_right_brick_rect = [self.rect.x + + self.rect.width / 2, self.rect.y + self.rect.height / 2,
                                        self.rect.x + self.rect.width, self.rect.y + self.rect.height]

        did_bullet_hit = False

        if is_rectangles_overlap(self.top_left_brick_rect, bullet_rect):
            if self.obstacle_state[0] != 0:
                did_bullet_hit = True
            self.obstacle_state[0] = 0

        if is_rectangles_overlap(self.top_right_brick_rect, bullet_rect):
            if self.obstacle_state[1] != 0:
                did_bullet_hit = True
            self.obstacle_state[1] = 0

        if is_rectangles_overlap(self.bottom_left_brick_rect, bullet_rect):
            if self.obstacle_state[2] != 0:
                did_bullet_hit = True
            self.obstacle_state[2] = 0

        if is_rectangles_overlap(self.bottom_right_brick_rect, bullet_rect):
            if self.obstacle_state[3] != 0:
                did_bullet_hit = True
            self.obstacle_state[3] = 0

        self.update_sprite()

        return did_bullet_hit

    def destroy_block(self):
        self.cell.required_bullet_level[self.subcell_index] = 0
        GameObjects.GameObjects.instance.static_objects.remove(self)
        self.kill()


class Concrete(pygame.sprite.Sprite):
    def __init__(self, cell, subcell_index):
        pygame.sprite.Sprite.__init__(self)
        self.images = []

        self.collision_type = 1

        self.block_health = 2

        image = pygame.image.load(os.path.join('sprites/Obstacles/Concretes', f'Concrete.png')).convert()
        self.size = image.get_size()
        self.image = pygame.transform.scale(image, (30, 30))
        self.rect = self.image.get_rect()

        self.image.set_colorkey((0, 0, 0))

        self.cell = cell
        self.subcell_index = subcell_index
        self.cell.required_bullet_level[self.subcell_index] = 4

    def collider_with_bullet(self, bullet):
        bullet_rect = [bullet.rect.x, bullet.rect.y,
                       bullet.rect.x + bullet.rect.width, bullet.rect.y + bullet.rect.height]
        concrete_rect = [self.rect.x, self.rect.y,
                         self.rect.x + self.rect.width, self.rect.y + self.rect.height]
        if is_rectangles_overlap(concrete_rect, bullet_rect):
            if bullet.level == 4:
                self.block_health -= 1
                if self.block_health == 0:
                    self.destroy_block()
            return True

        return False

    def destroy_block(self):
        self.cell.required_bullet_level[self.subcell_index] = 0
        GameObjects.GameObjects.instance.static_objects.remove(self)
        self.kill()


class Water(pygame.sprite.Sprite):
    def __init__(self, cell, subcell_index):
        pygame.sprite.Sprite.__init__(self)
        self.images = []

        self.collision_type = 1

        image = pygame.image.load(os.path.join('sprites/Obstacles', f'Water.png')).convert()
        self.size = image.get_size()
        self.image = pygame.transform.scale(image, (30, 30))
        self.rect = self.image.get_rect()

        self.image.set_colorkey((0, 0, 0))

        self.cell = cell
        self.subcell_index = subcell_index
        self.cell.required_bullet_level[self.subcell_index] = 255

    def collider_with_bullet(self, bullet):
        return False


class Trees(pygame.sprite.Sprite):
    def __init__(self, cell, subcell_index):
        pygame.sprite.Sprite.__init__(self)
        self.images = []

        self.collision_type = 0

        image = pygame.image.load(os.path.join('sprites/Obstacles', f'Trees.png')).convert()
        self.size = image.get_size()
        self.image = pygame.transform.scale(image, (30, 30))
        self.rect = self.image.get_rect()

        self.image.set_colorkey((0, 0, 0))

        self.cell = cell
        self.subcell_index = subcell_index

    def collider_with_bullet(self, bullet):
        return False


class Ice(pygame.sprite.Sprite):
    def __init__(self, cell, subcell_index):
        pygame.sprite.Sprite.__init__(self)
        self.images = []

        self.collision_type = 0

        image = pygame.image.load(os.path.join('sprites/Obstacles', f'Ice.png')).convert()
        self.size = image.get_size()
        self.image = pygame.transform.scale(image, (30, 30))
        self.rect = self.image.get_rect()

        self.image.set_colorkey((0, 0, 0))

        self.cell = cell
        self.subcell_index = subcell_index

    def collider_with_bullet(self, bullet):
        return False

    def collider_with_player(self):
        player = GameObjects.GameObjects.instance.player
        if player is None:
            return False

        player_rect = [player.rect.x, player.rect.y,
                       player.rect.x + player.rect.width, player.rect.y + player.rect.height]
        ice_rect = [self.rect.x, self.rect.y,
                    self.rect.x + self.rect.width, self.rect.y + self.rect.height]

        return is_rectangles_overlap(player_rect, ice_rect)
