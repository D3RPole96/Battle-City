import pygame


class GameObjects:
    instance = None

    def __init__(self):
        self.interface_sprite_group = pygame.sprite.Group()
        self.front_sprite_group = pygame.sprite.Group()
        self.middle_sprite_group = pygame.sprite.Group()
        self.back_sprite_group = pygame.sprite.Group()

        self.dynamic_objects = []
        self.static_objects = []
        self.enemies = []
        self.bullets = []

    def set_player(self, player):
        self.dynamic_objects.append(player)
        self.middle_sprite_group.add(player)
        self.player = player

    def add_static_object(self, game_object, layer='middle'):
        if layer == 'interface':
            self.interface_sprite_group.add(game_object)
        if layer == 'front':
            self.front_sprite_group.add(game_object)
        if layer == 'middle':
            self.middle_sprite_group.add(game_object)
        if layer == 'back':
            self.back_sprite_group.add(game_object)
        self.static_objects.append(game_object)

    def add_bullet(self, bullet):
        self.middle_sprite_group.add(bullet)
        self.bullets.append(bullet)

    def get_all_objects(self):
        return self.dynamic_objects + self.static_objects + self.bullets

    def check_for_collision(self):
        for dynamic_object in self.dynamic_objects:
            for game_object in self.get_all_objects():
                if dynamic_object == game_object:
                    continue
                if dynamic_object.rect.colliderect(game_object.rect) and game_object.collision_type == 1:
                    dynamic_object.undo_move()
                if dynamic_object.rect.colliderect(game_object.rect) and game_object.collision_type == 2:
                    dynamic_object.collider_with_bullet(game_object)

        did_bullet_hit = False
        for bullet in self.bullets:
            hit_object = []
            for static_object in self.static_objects:
                if static_object.rect.colliderect(bullet.rect):
                    did_bullet_hit = static_object.collider_with_bullet(bullet) or did_bullet_hit
                    hit_object.append(static_object)
            if did_bullet_hit:
                for static_object in self.static_objects:
                    if static_object not in hit_object:
                        static_object.collider_with_bullet(bullet)
            if did_bullet_hit:
                bullet.destroy_bullet()
            did_bullet_hit = False

    def move_bullets(self):
        for bullet in self.bullets:
            bullet.move_bullet()
            bullet.is_bullet_behind_screen()
