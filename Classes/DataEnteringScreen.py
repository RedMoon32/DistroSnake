import pygame

from Classes import consts


class DataEnteringScreen:
    def __init__(self, window_name, text, width=consts.WIDTH, height=consts.HEIGHT):
        self.window_name = window_name
        self.text = text
        self.width = width
        self.height = height
        self.size = (self.width, self.height)

        pygame.init()
        pygame.display.set_caption(self.window_name)

    def run(self):
        screen = pygame.display.set_mode(self.size)
        font = pygame.font.Font(None, int(self.width / 20))
        input_box = pygame.Rect(5 * self.width / 16, 5 * self.height / 16,
                                self.width, self.height / 15)
        active, text, done = False, '', False

        while not done:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    return True, pygame.quit()
                if event.type == pygame.MOUSEBUTTONDOWN:
                    active = not active if input_box.collidepoint(event.pos) else False
                if event.type == pygame.KEYDOWN and active:
                    if event.key == pygame.K_RETURN:
                        return False, text
                    elif event.key == pygame.K_BACKSPACE:
                        text = text[:-1]
                    else:
                        text += event.unicode

            screen.fill(consts.GREY)
            screen.blit(font.render(self.text, True, consts.WHITE), (self.width / 2.5, self.width / 6.5))
            txt_surface = font.render(text, True, consts.WHITE)
            input_box.w = max(self.width / 3, txt_surface.get_width() + int(self.width / 64))
            screen.blit(txt_surface, (input_box.x + int(self.height / 43), input_box.y + int(self.height / 64)))
            pygame.draw.rect(screen, consts.WHITE, input_box, 2)

            pygame.display.flip()

