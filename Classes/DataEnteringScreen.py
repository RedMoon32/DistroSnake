import pygame


class DataEnteringScreen:
    def __init__(self, window_name, text, width=640, height=480):
        self.window_name = window_name
        self.text = text
        self.width = width
        self.height = height
        self.size = (self.width, self.height)

        pygame.init()
        pygame.display.set_caption(self.window_name)

    def run(self):
        screen = pygame.display.set_mode(self.size)
        font = pygame.font.Font(None, int(self.width/20))
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

            screen.fill((30, 30, 30))
            screen.blit(font.render(self.text, True, (255, 255, 255)), (self.width / 2.5, self.width / 6.5))
            txt_surface = font.render(text, True, pygame.Color('white'))
            input_box.w = max(self.width / 3, txt_surface.get_width() + int(self.width/64))
            screen.blit(txt_surface, (input_box.x + int(self.height/43), input_box.y + int(self.height/64)))
            pygame.draw.rect(screen, pygame.Color('white'), input_box, 2)

            pygame.display.flip()

# if __name__ == '__main__':
#     auth = NameEnteringScreen()
#     res = auth.run()
#     print(res)
