import random

import pygame


class HostInitializationScreen:
    def __init__(self, width=640, height=480):
        self.width = width
        self.height = height
        self.size = (self.width, self.height)
        self.host = self.host_init()

        pygame.init()
        pygame.display.set_caption('Host initialization')

    def run(self):
        screen = pygame.display.set_mode(self.size)
        font = pygame.font.Font(None, 32)
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


            # txt_surface = font.render(text, True, color)
            # input_box.w = max(self.width / 3, txt_surface.get_width() + 10)
            # screen.blit(txt_surface, (input_box.x + 5, input_box.y + 5))
            # pygame.draw.rect(screen, color, input_box, 2)

            pygame.display.flip()

    def host_init(self):
        return random.randint(10,20)

if __name__ == '__main__':
    auth = HostInitializationScreen()
    res = auth.run()
    print(res)
