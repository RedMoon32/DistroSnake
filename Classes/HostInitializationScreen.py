import random

import pygame

from Classes import consts


class HostInitializationScreen:
    def __init__(self, width=consts.WIDTH, height=consts.HEIGHT):
        self.width = width
        self.height = height
        self.size = (self.width, self.height)
        self.host = self.host_init()

        pygame.init()
        pygame.display.set_caption('Host initialization')

    def run(self):
        screen = pygame.display.set_mode(self.size)
        font = pygame.font.Font(None, int(2 * self.width / 45))
        input_box = pygame.Rect(5 * self.width / 16, 5 * self.height / 16,
                                self.width, self.height / 15)
        active, text, done = False, '', False

        while not done:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    done = True
                if event.type == pygame.MOUSEBUTTONDOWN:
                    active = not active if input_box.collidepoint(event.pos) else False
                if event.type == pygame.KEYDOWN and active:
                    if event.key == pygame.K_RETURN:
                        return text
                    elif event.key == pygame.K_BACKSPACE:
                        text = text[:-1]
                    else:
                        text += event.unicode

            # screen.fill((30, 30, 30))
            screen.blit(font.render('Yout host is {}.'.format(self.host), True, (255, 255, 255)),
                        (self.height / 2, self.width / 10))

            screen.blit(font.render('Players: ', True, (255, 255, 255)),
                        (self.height / 1.7, self.width / 6))

            pygame.display.flip()

    def host_init(self):
        return random.randint(10, 20)
