import itertools
import sys
import pygame
import time

from Classes import consts
from Classes.Food import Food
from Classes.Snake import Snake
from Communication.receive import update_game_var, get_key, get_game, set_key

import random

RAND = random.randint(1000, 9999)

last = None


class Game:
    def __init__(self, snakes=[], width=consts.WIDTH, height=consts.HEIGHT,
                 speed=consts.SPEED, food=None, scores=None, host_addr="ABVD"):
        self.snakes = snakes
        self.width = width
        self.height = height
        self.food = Food(food[0], food[1]) if food is not None else Food(self.width / 2, self.height / 2)
        self.intend = self.width / 12
        self.time_interval = consts.SAVE_TIME_INTERVAL_SEC
        self.fps_controller = pygame.time.Clock()
        self.scores = [0 for _ in range(len(self.snakes))] if not scores else scores
        self.status = consts.STATUS_OK
        self.speed = speed
        self.play_surface = pygame.display.set_mode((self.width, self.height))
        self.host_addr = host_addr
        pygame.display.set_caption('Snake Game')
        pygame.init()

    # @staticmethod
    def get_key(self, change_to=None):

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
                    exit()
            if event.type == pygame.QUIT:
                return sys.exit()
        return change_to

    def refresh_screen(self):
        alive = 1
        self.fps_controller.tick(max(1, alive * self.speed))

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

    def draw_snakes(self, snakes, play_surface):
        play_surface.fill(consts.WHITE)
        for snake in snakes:
            for ind, pos in enumerate(snake.body):
                pygame.draw.rect(play_surface, snake.color,
                                 pygame.Rect(pos[0], pos[1], 10, 10)) if ind > 0 else pygame.draw.rect(play_surface,
                                                                                                       consts.BLACK,
                                                                                                       pygame.Rect(
                                                                                                           pos[0],
                                                                                                           pos[1], 10,
                                                                                                           10))

    def to_dict(self):
        return {"snakes": [snake.to_dict() for snake in self.snakes],
                "width": self.width, "height": self.height, "speed": self.speed,
                "food_pos": self.food.pos, "scores": self.scores}

    @staticmethod
    def from_dict(data):
        return Game([Snake.from_dict(s) for s in data["snakes"]],
                    data["width"], data["height"], data["speed"],
                    data["food_pos"], data["scores"])

    def calculate(self):
        for i, snake in enumerate(self.snakes):
            if snake.alive:
                snake.change_to = get_key(snake.name)  # self.event_loop(snake.change_to)
                snake.validate_direction_and_change()
                snake.change_head_position()
                self.scores[i], self.food.pos = snake.body_mechanism(
                    self.scores[i], self.food.pos, self.width, self.height)
                snake.check_for_boundaries(self.snakes, self.game_over, self.width, self.height)

    def run(self):
        while True:
            self.calculate()
            self.render()
            update_game_var(self.host_addr, "state", self.to_dict())
            self.refresh_screen()

    def render(self):
        key = self.get_key()
        self.draw_snakes(self.snakes, self.play_surface)
        self.food.draw(self.play_surface)
        self.show_scores()
        pygame.display.flip()
        self.refresh_screen()
        return key

    @staticmethod
    def game_calculate_once(host_addr, player_name):
        global last

        availability = host_addr + "_AVAILABLE_" + str(RAND)
        prev_state = get_game(host_addr)
        if prev_state is None:
            prev_state = last

        pre_calc_game = Game.from_dict(prev_state["state"])

        if player_name in [snake.name for snake in pre_calc_game.snakes if snake.alive] and not get_key(availability):
            set_key(availability, True, px=1500)
            pre_calc_game.calculate()
            prev_state["state"] = pre_calc_game.to_dict()
            set_key(host_addr, prev_state)
            set_key(availability, False)

        last = prev_state

        return pre_calc_game.render()

# # crazy test
# if __name__ == '__main__':
#     snakes = [Snake("dimon", width=720, height=460),
#               Snake("rinat", width=720, height=460)]
#     # Snake("sanya", width=720, height=460)]
#     game = Game(snakes, width=720, height=460).run()
