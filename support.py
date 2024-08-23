# System functionality
from os import walk
import pygame


def import_folder(path):
    image_surfaces = []

    for _, __, image_files in walk(path):
        for image in image_files:
            full_path = path + '/' + image
            image_surface = pygame.image.load(full_path).convert_alpha()
            image_surfaces.append(image_surface)

    return image_surfaces


class Spritesheet:
    def init(self, image):
        self.spread_sheet = image

    def get_frame(self, width, height, color):
        image = pygame.Surface((width, height)).convert_alpha()
        image.blit(self.spread_sheet, (0, 0))
        image = pygame.transform.scale(image, (width, height))
        image.set_colorkey(color)

        return image

