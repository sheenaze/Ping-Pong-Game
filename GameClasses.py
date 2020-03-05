import pygame as pg
from pynput import keyboard
from enum import Enum
# import time
import random


class Board:
    def __init__(self, width, height, window_color):
        self.width = width
        self.height = height
        self.window_color = window_color
        self.window = pg.display.set_mode((width, height), 0, 32)
        self.rect = self.window.get_rect()
        pg.display.set_caption("PingPong by Mon")

    def draw_elements(self, *args):
        self.window.fill(self.window_color)
        for element in args:
            element.draw(self.window)
        pg.display.update()


class ObjectBase:
    def __init__(self, width, height, x, y, color):
        self.width = int(width)
        self.height = int(height)
        self.start_x = x
        self.start_y = y
        self.color = color
        self.surface = pg.Surface((self.width, self.height), pg.SRCALPHA, 32).convert_alpha()
        self.rect = self.surface.get_rect(x=self.start_x, y=self.start_y)

    def draw(self, window):
        window.blit(self.surface, self.rect)

    def reset_position(self):
        self.rect = self.surface.get_rect(x=self.start_x, y=self.start_y)


class FontNames(Enum):
    arial = 'arial'
    comic = 'comicsansms'
    calibri = 'calibri'
    cambria = 'cambria'
    times = 'times'


class TextWidget:
    def __init__(self, font_name, font_size, font_color, text):
        self.font_name = font_name
        self.font_size = font_size
        self.font_color = font_color
        self.text = text

        pg.font.init()
        font_path = pg.font.match_font(self.font_name)
        self.font = pg.font.Font(font_path, self.font_size)
        self.text_width, self.text_height = self.font.size(self.text)
        self.surface = self.font.render(self.text, True, self.font_color)
        self.rect = self.surface.get_rect()

    def set_text_rect(self, start_x, start_y):
        self.rect = self.surface.get_rect(x=start_x, y=start_y)

    def draw(self, window):
        window.blit(self.surface, self.rect)


class Ball(ObjectBase):
    def __init__(self, width, height, x, y, color, radius, x_direction=0, y_direction=0):
        super(Ball, self).__init__(width, height, x, y, color)
        self.radius = radius
        self.x_direction = x_direction
        self.y_direction = y_direction
        pg.draw.circle(self.surface, color, [self.radius, self.radius], self.radius)

    def bounce_x(self):
        self.x_direction *= -1

    def bounce_y(self):
        self.y_direction *= -1

    def move(self):
        self.rect.x += self.x_direction
        self.rect.y += self.y_direction

    def reset_movement_vector(self):
        self.x_direction = random.randint(1, 5)
        self.y_direction = random.randint(1, 5)


class Paddle(ObjectBase):
    def __init__(self, width, height, x, y, color, y_speed=100):
        super(Paddle, self).__init__(width, height, x, y, color)
        self.y_speed = y_speed
        pg.draw.line(self.surface, color, [0, 0], [0, self.height], 20)

    def move_paddle_up(self):
        if self.rect.y >= self.y_speed:
            self.rect.y -= self.y_speed
        else:
            self.rect.y -= self.rect.y

    def move_paddle_down(self, window_height):
        if window_height - (self.rect.y + self.rect[3]) >= self.y_speed:
            self.rect.y += self.y_speed
        else:
            self.rect.y += window_height - (self.rect.y + self.rect[3])


class Collisions(Enum):
    x_collision = 1
    y_collision = 2
    corner_collision = 3


class DetectCollisions:
    def __init__(self, object_rect):
        self.x_min = object_rect[0]
        self.y_min = object_rect[1]
        self.x_max = object_rect[0] + object_rect[2]
        self.y_max = object_rect[1] + object_rect[3]

    def included_object_collision(self, outside_object_rect):
        board_x_min = outside_object_rect[0]
        board_x_max = outside_object_rect[0] + outside_object_rect[2]
        board_y_min = outside_object_rect[1]
        board_y_max = outside_object_rect[1] + outside_object_rect[3]

        x_cond = self.x_min > board_x_min and self.x_max < board_x_max
        y_cond = self.y_min > board_y_min and self.y_max < board_y_max

        if not (x_cond or y_cond):
            return Collisions.corner_collision

        elif not x_cond:
            return Collisions.x_collision

        elif not y_cond:
            return Collisions.y_collision

    def excluded_object_collision(self, object_rect):

        object_x_min = object_rect[0]
        object_y_min = object_rect[1]
        object_x_max = object_rect[0] + object_rect[2]
        object_y_max = object_rect[1] + object_rect[3]

        x_cond = self.x_max < object_x_min or self.x_min > object_x_max
        y_cond = self.y_max < object_y_min or self.y_min > object_y_max

        return not (x_cond or y_cond)


class LocalListener:
    def __init__(self, function_name):
        self.listener = keyboard.Listener(
            on_press=function_name)

    def listen(self):
        self.listener.start()


class GameActions:
    def __init__(self, scene, ball, paddle_left, paddle_right):
        self.scene = scene
        self.ball = ball
        self.paddle_left = paddle_left
        self.paddle_right = paddle_right
        self.paddle_listener = LocalListener(self.paddles_movement)
        self.paddle_listener.listen()
        self.counter_left = 0
        self.counter_right = 0

    def ball_movement(self):
        self.ball.move()
        ball_collisions = DetectCollisions(self.ball.rect)

        ball_window_collision = ball_collisions.included_object_collision(self.scene.rect)
        ball_paddle_left_collision = ball_collisions.excluded_object_collision(self.paddle_left.rect)
        ball_paddle_right_collision = ball_collisions.excluded_object_collision(self.paddle_right.rect)

        if ball_paddle_left_collision or ball_paddle_right_collision:
            self.ball.bounce_x()
        elif ball_window_collision == Collisions.y_collision:
            self.ball.bounce_y()

    def paddles_movement(self, key):
        try:
            if key == keyboard.Key.up and self.paddle_right.rect.y > 0:
                self.paddle_right.move_paddle_up()  #
            elif key == keyboard.Key.down and self.paddle_right.rect.y + self.paddle_right.height < self.scene.height:
                self.paddle_right.move_paddle_down(self.scene.height)
            elif key.char == 'w' and self.paddle_left.rect.y > 0:
                self.paddle_left.move_paddle_up()
            elif key.char == 's' and self.paddle_left.rect.y + self.paddle_left.height < self.scene.height:
                self.paddle_left.move_paddle_down(self.scene.height)
        except Exception:
            print(False)

    def reset_all_positions(self):
        self.ball.reset_position()
        self.paddle_left.reset_position()
        self.paddle_right.reset_position()
        self.ball.reset_movement_vector()

    def count_points(self):
        if self.ball.rect.x > self.scene.rect[0] + self.scene.rect[2]:
            self.counter_left += 1
            self.reset_all_positions()
        elif self.ball.rect.x < self.scene.rect[0]:
            self.counter_right += 1
            self.reset_all_positions()
        return f'{self.counter_left}:{self.counter_right}'


class CurrentGameObjectsFactory:
    def __init__(self, window_width, window_height, paddles_color, ball_radius, ball_color, text_color):
        self.window_width = window_width
        self.window_height = window_height
        self.x_mid = int(window_width / 2)
        self.y_mid = int(window_height / 2)
        self.paddles_color = paddles_color
        self.ball_color = ball_color
        self.ball_radius = ball_radius
        self.paddle_length = 110
        self.paddle_width = 20
        self.text_color = text_color

    def get_ball(self):
        # parameters for a ball
        ball_surf_width = self.ball_radius * 2
        ball_surf_height = self.ball_radius * 2
        ball_x_speed = random.randint(1, 5)
        ball_y_speed = random.randint(1, 5)
        #
        ball_x_start = self.x_mid
        ball_y_start = self.y_mid
        #
        return Ball(ball_surf_width, ball_surf_height, ball_x_start, ball_y_start, self.ball_color,
                    self.ball_radius, ball_x_speed, ball_y_speed)

    def get_left_paddle(self):
        left_pad_x_start = 30
        left_pad_y_start = self.y_mid - int(self.paddle_length / 2)

        return Paddle(self.paddle_width, self.paddle_length, left_pad_x_start, left_pad_y_start, self.paddles_color)

    def get_right_paddle(self):
        right_pad_x_start = self.window_width - 30 - self.paddle_width
        right_pad_y_start = self.y_mid - int(self.paddle_length / 2)
        #
        return Paddle(self.paddle_width, self.paddle_length, right_pad_x_start, right_pad_y_start, self.paddles_color)

    def result_display(self, result_text):
        text = TextWidget(FontNames.arial.value, int(self.window_height * 0.06), self.text_color, result_text)
        x_start = self.x_mid - int(text.text_width / 2)
        y_start = int(self.window_height * 0.01)
        text.set_text_rect(x_start, y_start)
        return text
