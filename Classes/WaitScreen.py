import pygame

from Classes import consts


class WaitSreen:
    # TODO: как-то посылать сигнал о том, что хост начал игру
    def __init__(self, width=consts.WIDTH, height=consts.HEIGHT):
        self.width = width
        self.height = height

        pygame.init()
        pygame.display.set_caption('Waiting')

    def run(self):
        screen = pygame.display.set_mode((self.width, self.height))
        smallfont = pygame.font.SysFont('monaco', int(self.width / 19))

        host_text = smallfont.render(' Play (потом будет Waiting for others)', True, consts.WHITE)

        player_pos = 1 / 6
        move_parameter = 1 / 12 * self.height
        _width = 1 / 10 * self.width

        position = 3 / 4
        while True:
            mouse = pygame.mouse.get_pos()
            for ev in pygame.event.get():
                if ev.type == pygame.QUIT:
                    return False, True, pygame.quit()
                if ev.type == pygame.MOUSEBUTTONDOWN:
                    if self.width / 3 <= mouse[0] <= self.width / 3 + 3 * self.height * player_pos \
                            and self.height * player_pos <= mouse[1] <= self.height * player_pos + move_parameter:
                        return True, None, pygame.quit()

                    if position * self.width <= mouse[0] <= position * 6 / 5 * self.width \
                            and position * self.height <= mouse[1] <= position * self.height + move_parameter:
                        return False, False, pygame.quit()

            pygame.draw.rect(screen,
                             consts.LIGHT_GREY,
                             [self.width / 3, self.height * player_pos,
                              int(6 * move_parameter), move_parameter])
            screen.blit(host_text, (self.width / 3, self.height * player_pos))

            pygame.draw.rect(screen,
                             consts.RED,
                             [position * self.width, position * self.height, int(3.5 * move_parameter), move_parameter])

            quit_text = smallfont.render('Quit ', True, consts.WHITE)
            screen.blit(quit_text, (position * self.width + _width / 2, position * self.height))

            pygame.display.update()

# if __name__ == '__main__':
#     auth = WaitSreen()
#     res = auth.run()
#     print(res)
