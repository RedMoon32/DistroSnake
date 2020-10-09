import random
import pygame


class Snake:
    def printing(self):
        print(self.head_pos)

    def __init__(self, name, width=720, height=460):
        self.name = name
        self.width = width
        self.height = height
        self.intend = 60
        # TODO: рандомить вдали от остальных змей
        self.head_pos = self.randomize_head_position(self.width, self.height, self.intend)  # [x, y]
        self.body = self.randomize_body_position(self.head_pos)
        self.color = self.randomize_color()
        self.direction = self.randomize_init_direction(self.body)
        self.change_to = self.direction

    def randomize_head_position(self, width, height, intend):
        width /= 10
        height /= 10
        intend /= 10
        return [random.randint(intend, width - intend)*10, random.randint(intend, height - intend)*10]

    def randomize_body_position(self, head_pos):
        s_w = head_pos[0]
        s_h = head_pos[1]
        to_right = [[s_w, s_h], [s_w - 10, s_h], [s_w - 20, s_h]]
        to_left = [[s_w, s_h], [s_w + 10, s_h], [s_w + 20, s_h]]
        to_up = [[s_w, s_h], [s_w, s_h + 10], [s_w, s_h + 20]]
        to_down = [[s_w, s_h], [s_w, s_h - 10], [s_w, s_h - 20]]
        moves = [to_right, to_left, to_up, to_down]
        return random.choice(moves)

    def randomize_color(self):
        r = random.randint(20, 245)
        g = random.randint(20, 245)
        b = random.randint(20, 245)
        return [r, g, b]

    def randomize_init_direction(self, body):
        if body[0][0] < self.width / 7 and body[0][1] < self.height / 7:
            if body[0][0] < body[1][0]:
                return random.choice(["DOWN"])
            elif body[0][0] > body[1][0] or body[0][1] > body[1][1]:
                return random.choice(["DOWN", "RIGHT"])
            elif body[0][1] < body[1][1]:
                return random.choice(["RIGHT"])
        elif body[0][0] < self.width / 7 and self.height / 7 < body[0][1] < 6 * self.height / 7:
            if body[0][0] < body[1][0]:
                return random.choice(["UP", "DOWN"])
            elif body[0][0] > body[1][0]:
                return random.choice(["UP", "DOWN", "RIGHT"])
            elif body[0][1] < body[1][1]:
                return random.choice(["UP", "RIGHT"])
            else:
                return random.choice(["DOWN", "RIGHT"])
        elif body[0][0] < self.width / 7 and 6 * self.height / 7 < body[0][1] < self.height:
            if body[0][0] < body[1][0]:
                return random.choice(["UP"])
            elif body[0][0] > body[1][0] or body[0][1] < body[1][1]:
                return random.choice(["UP", "RIGHT"])
            elif body[0][1] > body[1][1]:
                return random.choice(["RIGHT"])
        elif body[0][1] < self.height / 7 and self.width / 7 < body[0][0] < 6 * self.width / 7:
            if body[0][0] < body[1][0]:
                return random.choice(["DOWN", "LEFT"])
            elif body[0][0] > body[1][0]:
                return random.choice(["DOWN", "RIGHT"])
            elif body[0][1] < body[1][1]:
                return random.choice(["LEFT", "RIGHT"])
            else:
                return random.choice(["LEFT", "RIGHT", "DOWN"])
        elif self.height / 7 <= body[0][1] <= 6 * self.height / 7 \
                and self.width / 7 <= body[0][0] <= 6 * self.width / 7:
            if body[0][0] < body[1][0]:
                return random.choice(["UP", "LEFT", "DOWN"])
            elif body[0][0] > body[1][0]:
                return random.choice(["UP", "RIGHT", "DOWN"])
            elif body[0][1] < body[1][1]:
                return random.choice(["UP", "LEFT", "RIGHT"])
            else:
                return random.choice(["DOWN", "LEFT", "RIGHT"])
        elif 6 * self.height / 7 < body[0][1] < self.height \
                and self.width / 7 < body[0][0] < 6 * self.width / 7:
            if body[0][0] < body[1][0]:
                return random.choice(["LEFT", "UP"])
            elif body[0][0] > body[1][0]:
                return random.choice(["UP", "RIGHT"])
            elif body[0][1] < body[1][1]:
                return random.choice(["LEFT", "RIGHT", "UP"])
            else:
                return random.choice(["LEFT", "RIGHT"])
        elif body[0][1] < self.height / 7 \
                and 6 * self.width / 7 < body[0][0] < self.width:
            if body[0][0] < body[1][0] or body[0][1] > body[1][1]:
                return random.choice(["LEFT", "DOWN"])
            elif body[0][0] > body[1][0]:
                return random.choice(["DOWN"])
            elif body[0][1] < body[1][1]:
                return random.choice(["LEFT"])
        elif 6 * self.width / 7 < body[0][0] < self.width \
                and 6 * self.height / 7 > body[0][1] > self.height / 7:
            if body[0][0] < body[1][0]:
                return random.choice(["LEFT", "DOWN", "UP"])
            elif body[0][0] > body[1][0]:
                return random.choice(["DOWN", "UP"])
            elif body[0][1] < body[1][1]:
                return random.choice(["LEFT", "UP"])
            else:
                return random.choice(["LEFT", "DOWN"])
        else:
            if body[0][0] < body[1][0]:
                return random.choice(["LEFT", "UP"])
            elif body[0][0] > body[1][0]:
                return random.choice(["UP"])
            elif body[0][1] < body[1][1]:
                return random.choice(["LEFT", "UP"])
            else:
                return random.choice(["LEFT"])

    def validate_direction_and_change(self):
        if any((self.change_to == "RIGHT" and not self.direction == "LEFT",
                self.change_to == "LEFT" and not self.direction == "RIGHT",
                self.change_to == "UP" and not self.direction == "DOWN",
                self.change_to == "DOWN" and not self.direction == "UP")):
            self.direction = self.change_to

    def change_head_position(self):
        if self.direction == "RIGHT":
            self.head_pos[0] += 10
        elif self.direction == "LEFT":
            self.head_pos[0] -= 10
        elif self.direction == "UP":
            self.head_pos[1] -= 10
        elif self.direction == "DOWN":
            self.head_pos[1] += 10

    def body_mechanism(self, score, food_pos, screen_width, screen_height):
        self.body.insert(0, list(self.head_pos))
        if (self.head_pos[0] == food_pos[0] and
                self.head_pos[1] == food_pos[1]):
            food_pos = [random.randrange(1, screen_width / 10) * 10,
                        random.randrange(1, screen_height / 10) * 10]
            score += 1
        else:
            self.body.pop()
        return score, food_pos

    def draw_snake(self, play_surface):
        play_surface.fill(pygame.Color(255, 255, 255))
        for pos in self.body:
            pygame.draw.rect(
                play_surface, self.color, pygame.Rect(
                    pos[0], pos[1], 10, 10))

    def check_for_boundaries(self, game_over, screen_width, screen_height):
        if any((
                self.head_pos[0] > screen_width - 10
                or self.head_pos[0] < 0,
                self.head_pos[1] > screen_height - 10
                or self.head_pos[1] < 0
        )):
            game_over()
        for block in self.body[1:]:
            if (block[0] == self.head_pos[0] and
                    block[1] == self.head_pos[1]):
                game_over()