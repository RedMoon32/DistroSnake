import os
import sys
from datetime import datetime

import pygame
import csv
import time

from Classes.DataEnteringScreen import DataEnteringScreen
from Classes.Food import Food
from Classes.Snake import Snake


class Game:
    def __init__(self, snakes, width=720, height=460, speed=25):
        self.snakes = snakes
        self.width = width
        self.height = height
        self.intend = self.width / 12
        self.time_interval = 3
        self.fps_controller = pygame.time.Clock()
        self.scores = [0 for _ in range(len(self.snakes))]
        self.status = "OK"
        self.speed = speed
        self.play_surface = pygame.display.set_mode((self.width, self.height))
        self.logger_file_path = "{}/{}".format(os.getcwd(), 'Logs/logs.csv')
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
        return change_to

    def refresh_screen(self):
        pygame.display.flip()
        alive = sum(1 for snake in self.snakes if snake.alive)
        Game(self.snakes, self.width, self.height).fps_controller.tick(alive * self.speed)

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

        s_font = pygame.font.SysFont('monaco', int(self.width / 25))
        self.blit_text(self.play_surface, results, (int(self.height/16), int(self.width/23)), s_font)

    def game_over(self):
        self.show_scores()
        res = [not snake.alive for snake in self.snakes]
        pygame.display.flip()
        if all(res):
            go_font = pygame.font.SysFont('monaco', int(self.width / 10))
            go_surf = go_font.render('Game is over', True, pygame.Color(255, 0, 0))
            go_rect = go_surf.get_rect()
            go_rect.midtop = (self.width / 2, self.height / 30)
            self.play_surface.blit(go_surf, go_rect)
            pygame.display.flip()
            self.status = "Finished"
            self.write_to_csv(self.logger_file_path)
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

    def write_to_csv(self, filename):
        snakes_data = [
            "{}. Direction: {}. Score: {}. ALive: {}. Died from self: {}. Died from wall: {}. Died from snake: {}"
                .format(snake.name, snake.direction, self.scores[i], snake.alive, snake.died_from_self,
                        snake.died_from_wall, snake.died_from_snake)
            for i, snake in enumerate(self.snakes)]
        writen = [
            {
                'Date and time': datetime.now().strftime("%m/%d/%Y, %H:%M:%S"),
                'game_status': self.status,
                'field_size': (self.width, self.height),
                'speed': self.speed,
                'snakes': snakes_data
            }]

        operation = 'a' if os.path.exists(filename) else 'w'
        csv_columns = ['Date and time', 'game_status', 'field_size', 'speed', 'snakes']

        exists = os.path.exists(os.path.dirname(filename))
        if not exists:
            os.makedirs(os.path.dirname(filename))

        with open(filename, operation) as f:
            writer = csv.DictWriter(f, fieldnames=csv_columns)
            if not exists:
                writer.writeheader()
            for data in writen:
                writer.writerow(data)

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
                    snake.draw_snake(self.play_surface)
                    food.draw(self.play_surface)
                    snake.check_for_boundaries(self.snakes, self.game_over, self.width, self.height)
                    self.show_scores()
                    self.refresh_screen()
            var = time.time() - timer
            if int(var % self.time_interval) == 0\
                    and var % self.time_interval < 0.055:
                self.write_to_csv(self.logger_file_path)

# # crazy test
# if __name__ == '__main__':
#     snakes = [Snake("dimon", width=720, height=460),
#               Snake("rinat", width=720, height=460)]
#     # Snake("sanya", width=720, height=460)]
#     game = Game(snakes, width=720, height=460).run()
