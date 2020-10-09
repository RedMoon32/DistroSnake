import sys
import time
import pygame

from Classes.Food import Food


class Game:
    def __init__(self, snakes, width=720, height=460):
        self.snakes = snakes
        self.width = width
        self.height = height
        self.intend = 60

        self.fps_controller = pygame.time.Clock()
        self.score = 0

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
                    sys.exit()
        return change_to

    def refresh_screen(self):
        pygame.display.flip()
        Game(self.snakes, self.width, self.height).fps_controller.tick(25)

    def show_score(self, choice=1):
        s_font = pygame.font.SysFont('monaco', 24)
        s_surf = s_font.render(
            '{0}. Score: {1}'.format(self.snakes.name, self.score), True, pygame.Color(0, 0, 0))
        s_rect = s_surf.get_rect()
        if choice == 1:
            s_rect.midtop = (self.width / 9, self.height / 23)
        else:
            s_rect.midtop = (self.width / 2, self.height / 4)
        self.play_surface.blit(s_surf, s_rect)

    def game_over(self):
        go_font = pygame.font.SysFont('monaco', int(self.width / 10))
        go_surf = go_font.render('Game over', True, pygame.Color(255, 0, 0))
        go_rect = go_surf.get_rect()
        go_rect.midtop = (self.width / 2, self.height / 30)
        self.play_surface.blit(go_surf, go_rect)
        self.show_score(0)
        pygame.display.flip()
        time.sleep(1)
        pygame.quit()
        sys.exit()


    def run(self):
        food = Food(self.width, self.height)
        while True:
            self.snakes.change_to = self.event_loop(self.snakes.change_to)
            self.snakes.validate_direction_and_change()
            self.snakes.change_head_position()
            self.score, food.pos = self.snakes.body_mechanism(
                self.score, food.pos, self.width, self.height)
            self.snakes.draw_snake(self.play_surface)
            food.draw(self.play_surface)
            self.snakes.check_for_boundaries(self.game_over, self.width, self.height)
            self.show_score()
            self.refresh_screen()
