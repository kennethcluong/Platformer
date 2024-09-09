# System functionality
from os import walk
import pygame
import pytmx


def import_folder(path):
    image_surfaces = []

    for _, __, image_files in walk(path):
        for image in image_files:
            full_path = path + '/' + image
            image_surface = pygame.image.load(full_path).convert_alpha()
            image_surfaces.append(image_surface)

    return image_surfaces


class TiledMap:
    def __init__(self, filename):
        tile_map = pytmx.load_pygame(filename, pixelalpha=True)
        self.width = tile_map.width * tile_map.tilewidth
        self.height = tile_map.height * tile_map.tileheight
        self.tmx_data = tile_map

    def render(self, display_surface):
        tiles = self.tmx_data.get_tile_image_by_gid
        for layer in self.tmx_data.visible_layers:
            if isinstance(layer, pytmx.TiledTileLayer):
                for x, y, gid in layer:
                    tile = tiles(gid)
                    if tile:
                        display_surface.blit(tile, (x * self.tmx_data.tilewidth, y * self.tmx_data.tileheight))

    def make_map(self):
        return self.render(pygame.Surface((self.width, self.height)))


class Spritesheet:
    def init(self, image):
        self.spread_sheet = image

    def get_frame(self, width, height, color):
        image = pygame.Surface((width, height)).convert_alpha()
        image.blit(self.spread_sheet, (0, 0))
        image = pygame.transform.scale(image, (width, height))
        image.set_colorkey(color)

        return image

