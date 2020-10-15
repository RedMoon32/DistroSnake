import random
import pygame

from Classes import consts


class Food:
    def __init__(self, x, y):
        self.color = consts.RED
        self.size_x = 10
        self.size_y = 10
        self.pos = [x, y]

    def draw(self, play_surface):
        pygame.draw.rect(
            play_surface,
            self.color,
            pygame.Rect(self.pos[0], self.pos[1], self.size_x, self.size_y),
        )
