import pygame
from settings import TILE_SIZE, TILE_COLOR


# Inheriting from Sprite class
class Tile(pygame.sprite.Sprite):
    def __init__(self, position, groups):
        super().__init__(groups)
        self.image = pygame.Surface((TILE_SIZE, TILE_SIZE))
        self.image.fill(TILE_COLOR)
        self.rect = self.image.get_rect(topleft=position)

    # def update(self, x_shift):
    #     self.rect.x += x_shift
