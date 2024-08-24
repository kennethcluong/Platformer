import pygame
from settings import *
from support import import_folder


class Player(pygame.sprite.Sprite):
    def __init__(self, position, groups, collision_sprites):
        super().__init__(groups)
        self.image = pygame.Surface((TILE_SIZE // 2, TILE_SIZE))
        self.image.fill(PLAYER_COLOR)
        self.rect = self.image.get_rect(topleft=position)

        # Dust Particles
        self.dust_frame_index = 0
        self.dust_animation_speed = 0.15
        # self.create_jump_particles = create_jump_particles

        # Player Movement
        self.direction = pygame.math.Vector2()
        self.speed = 8
        self.gravity = 0.8
        self.jump_speed = -16

        self.collision_sprites = collision_sprites
        # Player Status
        self.status = 'idle'
        self.on_floor = False
        self.facing_right = True
        self.on_ceiling = False
        self.on_left = False
        self.on_right = False

    def import_character_assets(self):
        character_path = '../graphics/character/'
        self.animations = {'idle': [], 'run': [], 'jump': [], 'fall': []}

        for animation in self.animations.keys():
            full_path = character_path + animation
            self.animations[animation] = import_folder(full_path)

    def import_dust_run_particles(self):
        self.dust_run_particles = import_folder('../graphics/character/dust_particles/run')

    # animate our character
    def animate(self):
        pass

    def get_input(self):
        # Dictionary of Key Presses
        keys = pygame.key.get_pressed()

        if keys[pygame.K_RIGHT]:
            self.direction.x = 1
            # self.facing_right = True
        elif keys[pygame.K_LEFT]:
            self.direction.x = -1
            # self.facing_right = False
        else:
            self.direction.x = 0

        if keys[pygame.K_UP] and self.on_floor:
            self.jump()
            # self.create_jump_particles(self.rect.midbottom)

    def horizontal_collisions(self):
        for sprite in self.collision_sprites.sprites():
            if sprite.rect.colliderect(self.rect):
                if self.direction.x < 0:
                    self.rect.left = sprite.rect.right
                    self.on_left = True
                if self.direction.x > 0:
                    self.rect.right = sprite.rect.left
                    self.on_right = True

    def vertical_collisions(self):
        for sprite in self.collision_sprites.sprites():
            if sprite.rect.colliderect(self.rect):
                if self.direction.y > 0:
                    self.rect.bottom = sprite.rect.top
                    self.direction.y = 0
                    self.on_floor = True
                elif self.direction.y < 0:
                    self.rect.top = sprite.rect.bottom
                    self.direction.y = 0
                    self.on_ceiling = True

        # player has left the floor
        if self.on_floor and self.direction.y < 0 or self.direction.y > 1:
            self.on_floor = False
        if self.on_ceiling and self.direction.y > 0.1:
            self.on_ceiling = False

    # def get_status(self):
    #     if self.direction.y < 0:
    #         self.status = 'jump'
    #     elif self.direction.y > 1:
    #         self.status = 'fall'
    #     else:
    #         if self.direction.x != 0:
    #             self.status = 'run'
    #         else:
    #             self.status = 'idle'

    def import_dust_run_particles(self):
        self.dust_run_particles = import_folder('../graphics/character/dust_particles/run')

    def apply_gravity(self):
        self.direction.y += self.gravity
        self.rect.y += self.direction.y

    def jump(self):
        self.direction.y = self.jump_speed

    def update(self):
        self.get_input()
        self.rect.x += self.direction.x * self.speed
        self.horizontal_collisions()
        self.apply_gravity()
        self.vertical_collisions()
        if self.rect.y > 1200:
            self.rect.x = 0
            self.rect.y = 0
