from tile import AnimatedTile
from random import randint
import pygame


class Enemy(AnimatedTile):
    def __init__(self, pos, size, path):
        super().__init__(pos, size, path)
        self.speed = (randint(2, 4))

    def move(self):
        self.rect.x += self.speed

    def reverse(self):
        self.speed *= -1

    def reverse_image(self):
        if self.speed < 0:
            self.image = pygame.transform.flip(self.image, True, False)

    def update(self, shift):
        self.rect.x += shift
        self.animate()
        self.move()
        self.reverse_image()
