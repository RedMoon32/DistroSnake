import sys
import os
import pygame

from Classes import consts


class HostOrPlayerScreen:
    def __init__(self, width=consts.WIDTH, height=consts.HEIGHT):
        self.width = width
        self.height = height
        self.size = (self.width, self.height)
        pygame.init()
        pygame.display.set_caption('Host or player?')

    def run(self):
        screen = pygame.display.set_mode((self.width, self.height))
        smallfont = pygame.font.SysFont(consts.FONT, int(self.width / 19))

        quit_text = smallfont.render('Quit ', True, consts.WHITE)
        player_text = smallfont.render('Player ', True, consts.WHITE)
        host_text = smallfont.render(' Host ', True, consts.WHITE)

        position = 3 / 4
        player_pos = 1 / 6
        move_parameter = 1 / 12 * self.height
        _width = 1 / 10 * self.width
        _length = int(0.0076 * self.height * move_parameter)

        while True:
            mouse = pygame.mouse.get_pos()
            for ev in pygame.event.get():
                if ev.type == pygame.MOUSEBUTTONDOWN:
                    if position * self.width <= mouse[0] <= position * 6 / 5 * self.width \
                            and position * self.height <= mouse[1] <= position * self.height + move_parameter:
                        return pygame.quit()

                    elif player_pos * self.width <= mouse[0] <= 2 * player_pos * self.width \
                            and player_pos * self.height <= mouse[1] <= player_pos * self.height + move_parameter:
                        return True

                    elif player_pos * self.width + self.width / 2 <= mouse[
                        0] <= 2 * player_pos * self.width + self.width / 2 \
                            and player_pos * self.height <= mouse[1] <= player_pos * self.height + move_parameter:
                        return False
                if ev.type == pygame.QUIT:
                    sys.exit()

            pygame.draw.rect(screen,
                             consts.RED,
                             [position * self.width, position * self.height, _length, move_parameter])
            screen.blit(quit_text, (position * self.width + _width / 2, position * self.height))

            pygame.draw.rect(screen,
                             consts.LIGHT_GREY,
                             [self.width * player_pos, self.height * player_pos, _length,
                              move_parameter])
            screen.blit(player_text, (self.width * player_pos + _width / 2, self.height * player_pos))

            pygame.draw.rect(screen,
                             consts.LIGHT_GREY,
                             [self.width * player_pos + self.width / 2, self.height * player_pos, _length,
                              move_parameter])
            screen.blit(host_text, (self.width * player_pos + _width / 2 + self.width / 2, self.height * player_pos))

            pygame.display.flip()
