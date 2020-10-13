import sys

import pygame

from Classes import consts
from Communication.receive import render_players


class HostScreen:
    def __init__(self, window_name, host, width=consts.WIDTH, height=consts.HEIGHT):
        self.window_name = window_name
        self.host = host
        self.width = width
        self.height = height
        self.size = (self.width, self.height)

        pygame.init()
        pygame.display.set_caption(self.window_name)

    def run(self, game_name):
        screen = pygame.display.set_mode(self.size)
        smallfont = pygame.font.SysFont(consts.FONT, int(self.width / 19))
        _width = 1 / 10 * self.width

        position = 5 / 16
        move_parameter = 1 / 11 * self.height

        while True:
            screen.fill((0, 0, 0))
            mouse = pygame.mouse.get_pos()
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    sys.exit()
                if event.type == pygame.MOUSEBUTTONDOWN:
                    if position * self.width <= mouse[0] <= 1.5 * position * self.width \
                            and position * self.height <= mouse[1] <= position * self.height + move_parameter:
                        return True, pygame.quit()

            game_text = smallfont.render('Yout host is: {}'.format(self.host), True, consts.WHITE)
            screen.blit(game_text, (position * self.width, position * self.height / 2))

            pygame.draw.rect(screen,
                             consts.BLUE,
                             [position * self.width, position * self.height, int(5 * move_parameter), move_parameter])

            quit_text = smallfont.render('Start game! ', True, consts.WHITE)
            screen.blit(quit_text, (position * self.width + _width / 2, position * self.height))

            render_players(game_name, smallfont, self, screen)

            pygame.display.update()

# if __name__ == '__main__':
#     auth = HostScreen('Host data', '<сюда хост>', 720, 460).run()
#     res = auth.run()
#     print(res)
