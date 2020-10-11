import pygame


class HostOrPlayerScreen:
    def __init__(self, width=640, height=480):
        self.width = width
        self.height = height
        self.size = (self.width, self.height)

        pygame.init()
        pygame.display.set_caption('Host or player?')

    def run(self):
        screen = pygame.display.set_mode((self.width, self.height))
        smallfont = pygame.font.SysFont('monaco', 35)

        quit_text = smallfont.render('Quit ', True, (255, 255, 255))
        player_text = smallfont.render('Player ', True, (255, 255, 255))
        host_text = smallfont.render(' Host ', True, (255, 255, 255))

        position = 3 / 4
        player_pos = 1 / 6
        move_parameter = 1 / 12 * self.height
        _width = 1 / 10 * self.width

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

                    elif player_pos * self.width + self.width/2 <= mouse[0] <= 2 * player_pos * self.width + self.width/2 \
                            and player_pos * self.height <= mouse[1] <= player_pos * self.height + move_parameter:
                        return False

            pygame.draw.rect(screen,
                             (255, 0, 0),
                             [position * self.width, position * self.height, int(3.5 * move_parameter), move_parameter])
            screen.blit(quit_text, (position * self.width + _width/2, position * self.height))

            pygame.draw.rect(screen,
                             (100, 100, 100),
                             [self.width * player_pos, self.height * player_pos, int(3.5 * move_parameter),
                              move_parameter])
            screen.blit(player_text, (self.width * player_pos + _width/2, self.height * player_pos))

            pygame.draw.rect(screen,
                             (100, 100, 100),
                             [self.width * player_pos + self.width/2, self.height * player_pos, int(3.5 * move_parameter),
                              move_parameter])
            screen.blit(host_text, (self.width * player_pos + _width / 2 + self.width/2, self.height * player_pos))

            pygame.display.update()


# if __name__ == '__main__':
#     auth = HostOrPlayerScreen()
#     res = auth.run()
#     print(res)
