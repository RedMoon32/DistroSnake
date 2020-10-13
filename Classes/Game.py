import sys
import pygame
import time

from Classes import consts
from Classes.Food import Food
from Classes.Snake import Snake


class Game:
    def __init__(self, snakes, width=consts.WIDTH, height=consts.HEIGHT, speed=consts.SPEED):
        self.snakes = snakes
        self.width = width
        self.height = height
        self.intend = self.width / 12
        self.time_interval = consts.SAVE_TIME_INTERVAL_SEC
        self.fps_controller = pygame.time.Clock()
        self.scores = [0 for _ in range(len(self.snakes))]
        self.status = consts.STATUS_OK
        self.speed = speed
        self.play_surface = pygame.display.set_mode((self.width, self.height))

        pygame.display.set_caption('Snake Game')
        pygame.init()

    def event_loop(self, change_to):
        for event in pygame.event.get():
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_RIGHT or event.key == ord('d'):
                    change_to = "RIGHT"
                elif event.key == pygame.K_LEFT or event.key == ord('a'):
                    change_to = "LEFT"
                elif event.key == pygame.K_UP or event.key == ord('w'):
                    change_to = "UP"
                elif event.key == pygame.K_DOWN or event.key == ord('s'):
                    change_to = "DOWN"
                elif event.key == pygame.K_ESCAPE:
                    pygame.quit()
                    # sys.exit()
            if event.type == pygame.QUIT:
                return sys.exit()
        return change_to

    def refresh_screen(self):
        pygame.display.flip()
        alive = 1
        self.fps_controller.tick(alive * self.speed)

    def blit_text(self, surface, text, pos, font):
        words = [word.split(' ') for word in text.splitlines()]
        space = font.size(' ')[0]
        max_width, max_height = surface.get_size()
        x, y = pos
        for i, line in enumerate(words):
            for word in line:
                word_surface = font.render(word, 0, self.snakes[i].color)
                word_width, word_height = word_surface.get_size()
                if x + word_width >= max_width:
                    x = pos[0]
                    y += word_height
                surface.blit(word_surface, (x, y))
                x += word_width + space
            x = pos[0]  # Reset the x.
            y += word_height  # Start on new row.

    def show_scores(self):
        results = ''
        for i, snake in enumerate(self.snakes):
            results += '{0}. Score: {1}\n'.format(snake.name, self.scores[i])

        s_font = pygame.font.SysFont(consts.FONT, int(self.width / 25))
        self.blit_text(self.play_surface, results, (int(self.height / 16), int(self.width / 23)), s_font)

    def game_over(self):
        self.show_scores()
        res = [not snake.alive for snake in self.snakes]
        pygame.display.flip()
        if all(res):
            go_font = pygame.font.SysFont(consts.FONT, int(self.width / 10))
            go_surf = go_font.render('Game is over', True, pygame.Color(255, 0, 0))
            go_rect = go_surf.get_rect()
            go_rect.midtop = (self.width / 2, self.height / 30)
            self.play_surface.blit(go_surf, go_rect)
            pygame.display.flip()
            self.status = consts.STATUS_FINISHED
            time.sleep(2)
            pygame.quit()
            # sys.exit()

            # Кнопка для выхода, которую я не хз как делать
            # done = False
            # smallfont = pygame.font.SysFont('Corbel', 35)
            # text = smallfont.render('quit', True, (255, 255, 255))
            # _width = self.width / 10
            # _height = self.height / 12
            # while not done:
            #     mouse = pygame.mouse.get_pos()
            #     print(mouse)
            #     for ev in pygame.event.get():
            #         if ev.type == pygame.MOUSEBUTTONDOWN:
            #             if self.width / 2 <= mouse[0] <= \
            #                     self.width / 2 + 140 and \
            #                     self.height / 2 <= mouse[1] <= \
            #                     self.height / 2 + _height:
            #                 pygame.quit()
            #
            #     if self.width / 2 <= mouse[0] <= self.width / 2 + 140 \
            #             and self.height / 2 <= mouse[1] <= self.height / 2 + _height:
            #         pygame.draw.rect(self.play_surface, (255, 0, 0), [self.width / 2, self.height / 2, 140, _height])
            #     self.play_surface.blit(text, (self.width / 2 + 50, self.height / 2))
            #
            #     # updates the frames of the game
            #     pygame.display.update()

    def draw_snakes(self, snakes, play_surface):
        play_surface.fill(consts.WHITE)
        for snake in snakes:
            for pos in snake.body:
                pygame.draw.rect(
                    play_surface, snake.color, pygame.Rect(
                        pos[0], pos[1], 10, 10))

    def to_dict(self):
        return {"snakes": [snake.to_dict() for snake in self.snakes],
                "width": self.width, "height": self.height, "speed": self.speed}

    @staticmethod
    def from_dict(data):
        return Game([Snake.from_dict(s) for s in data["snakes"]],
                    data["width"], data["height"], data["speed"])

    def run(self):
        timer = time.time()
        food = Food(self.width, self.height)
        while True:
            for i, snake in enumerate(self.snakes):
                if snake.alive:
                    snake.change_to = self.event_loop(snake.change_to)
                    snake.validate_direction_and_change()
                    snake.change_head_position()
                    self.scores[i], food.pos = snake.body_mechanism(
                        self.scores[i], food.pos, self.width, self.height)
                    snake.check_for_boundaries(self.snakes, self.game_over, self.width, self.height)
                # print(self.to_dict())
                # print(self.from_dict(self.to_dict()))
            self.draw_snakes(self.snakes, self.play_surface)
            food.draw(self.play_surface)
            self.show_scores()
            self.refresh_screen()

# # crazy test
# if __name__ == '__main__':
#     snakes = [Snake("dimon", width=720, height=460),
#               Snake("rinat", width=720, height=460)]
#     # Snake("sanya", width=720, height=460)]
#     game = Game(snakes, width=720, height=460).run()
