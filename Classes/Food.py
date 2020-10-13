import random
import pygame

from Classes import consts


class Food:
    def __init__(self, screen_width = consts.WIDTH, screen_height = consts.HEIGHT):
        self.color = consts.RED
        self.size_x = 10
        self.size_y = 10
        self.pos = [random.randrange(1, screen_width / 10) * 10,
                    random.randrange(1, screen_height / 10) * 10]

    def draw(self, play_surface):
        pygame.draw.rect(
            play_surface, self.color, pygame.Rect(
                self.pos[0], self.pos[1],
                self.size_x, self.size_y))
