import pygame
from settings import *
from tile import Tile
from player import Player


class Level:
    def __init__(self):
        # level setup
        self.display_surface = pygame.display.get_surface()
        # sprite group setup
        self.visible_sprites = CameraGroup()
        self.active_sprites = pygame.sprite.Group()
        self.collision_sprites = pygame.sprite.Group()
        self.setup_level()

    def setup_level(self):
        for i, row in enumerate(LEVEL_MAP):
            for j, col in enumerate(row):
                x = j * TILE_SIZE
                y = i * TILE_SIZE
                if col == 'X':
                    Tile((x, y), [self.visible_sprites, self.collision_sprites])
                if col == 'P':
                    self.player = Player((x, y), [self.visible_sprites, self.active_sprites], self.collision_sprites)

    def run(self):
        # run the entire game (level)
        self.active_sprites.update()
        self.visible_sprites.custom_draw(self.player)


class CameraGroup(pygame.sprite.Group):
    def __init__(self):
        super().__init__()
        self.display_surface = pygame.display.get_surface()
        self.offset = pygame.math.Vector2(100, 300)

        # center camera setup
        # self.half_width = self.display_surface.get_size()[0] // 2
        # self.half_height = self.display_surface.get_size()[1] // 2
        # camera
        camera_left = CAMERA_BORDERS['left']
        camera_top = CAMERA_BORDERS['top']
        camera_width = self.display_surface.get_size()[0] - (camera_left + CAMERA_BORDERS['right'])
        camera_height = self.display_surface.get_size()[1] - (camera_top + CAMERA_BORDERS['bottom'])

        self.camera_rect = pygame.Rect(camera_left, camera_top, camera_width, camera_height)

    def custom_draw(self, player):
        # get the player offset
        # self.offset.x = player.rect.centerx - self.half_width
        # self.offset.y = player.rect.centery - self.half_height
        # getting the camera position
        if player.rect.left < self.camera_rect.left:
            self.camera_rect.left = player.rect.left
        if player.rect.right > self.camera_rect.right:
            self.camera_rect.right = player.rect.right
        if player.rect.top < self.camera_rect.top:
            self.camera_rect.top = player.rect.top
        if player.rect.bottom > self.camera_rect.bottom:
            self.camera_rect.bottom = player.rect.bottom
        # camera offset
        self.offset = pygame.math.Vector2(
            self.camera_rect.left - CAMERA_BORDERS['left'],
            self.camera_rect.top - CAMERA_BORDERS['top']
        )

        for sprite in self.sprites():
            offset_position = sprite.rect.topleft - self.offset
            self.display_surface.blit(sprite.image, offset_position)
