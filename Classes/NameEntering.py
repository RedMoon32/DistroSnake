import pygame


class NameEntering:
    def __init__(self, width = 640, height = 480):
        self.width = 640
        self.height = 480
        self.size = (self.width, self.height)

        pygame.init()

    def run(self):
        screen = pygame.display.set_mode(self.size)
        font = pygame.font.Font(None, 32)
        input_box = pygame.Rect(5 * self.width / 16, 5 * self.height / 16,
                            self.width / 15, self.height / 15)
        color_inactive = pygame.Color('lightskyblue3')
        color_active = pygame.Color('dodgerblue2')
        color = color_inactive
        active, text, done = False, '', False

        while not done:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    done = True
                if event.type == pygame.MOUSEBUTTONDOWN:
                    active = not active if input_box.collidepoint(event.pos) else False
                    color = color_active if active else color_inactive
                if event.type == pygame.KEYDOWN and active:
                    if event.key == pygame.K_RETURN:
                        return text
                    elif event.key == pygame.K_BACKSPACE:
                        text = text[:-1]
                    else:
                        text += event.unicode

            screen.fill((30, 30, 30))

            screen.blit(font.render('Enter name', True, (255, 255, 255)), (self.width / 2.7, self.width / 6))
            txt_surface = font.render(text, True, color)
            input_box.w = max(200, txt_surface.get_width() + 10)
            screen.blit(txt_surface, (input_box.x + 5, input_box.y + 5))
            pygame.draw.rect(screen, color, input_box, 2)
            pygame.display.flip()

# if __name__ == '__main__':
#     auth = Authorization()
#     res = auth.main()
#     print(res)
