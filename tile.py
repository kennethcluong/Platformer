import pygame
from settings import TILE_SIZE
from support import import_folder


class Tile(pygame.sprite.Sprite):
    def __init__(self, position):
        super().__init__()
        image = pygame.transform.scale(pygame.image.load('../graphics/terrain_tiles.png'), (TILE_SIZE, TILE_SIZE))
        self.image = image
        self.rect = self.image.get_rect(topleft=position)

    def update(self, x_shift):
        self.rect.x += x_shift


class AnimatedTile(Tile):
    def __init__(self, pos, path):
        super().__init__(pos)
        self.frames = import_folder(path)

    def animate(self):
        pass

    def update(self, x_shift):
        pass


class Mushroom(AnimatedTile):
    def __init__(self, pos, size, player):
        super().__init__(pos, size)
        self.jump_power = -20
        self.jump_power_up = False
        self.jump_power_up_duration = 5000
        self.player = player
        self.jump_power_up_timer = 0
        
    def activate_power_up(self):
        self.jump_power_up = True
        self.jump_power_up_timer = pygame.time.get_ticks() + self.jump_power_up_duration

    def update_jump_power(self):
        if self.jump_power_up and pygame.time.get_ticks() < self.jump_power_up_timer:
            self.player.jump_speed = self.jump_power
        else:
            self.player.jump_speed = -16
