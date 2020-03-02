import pygame as pg
from pynput import keyboard
import time
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


class Object:
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


class Ball(Object):
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


class Paddle(Object):
    def __init__(self, width, height, x, y, color, y_direction=100):
        super(Paddle, self).__init__(width, height, x, y, color)
        self.y_direction = y_direction
        pg.draw.line(self.surface, color, [0, 0], [0, self.height], 20)

    def move_paddle_up(self):
        self.rect.y -= self.y_direction

    def move_paddle_down(self):
        self.rect.y += self.y_direction


class DetectCollisions:
    def __init__(self, object_rect):
        self.x_min = object_rect[0]
        self.y_min = object_rect[1]
        self.x_max = object_rect[0] + object_rect[2]
        self.y_max = object_rect[1] + object_rect[3]

    def object_included_collision(self, outside_object_rect):
        board_x_min = outside_object_rect[0]
        board_x_max = outside_object_rect[0] + outside_object_rect[2]
        board_y_min = outside_object_rect[1]
        board_y_max = outside_object_rect[1] + outside_object_rect[3]

        if not (self.x_min > board_x_min and self.x_max < board_x_max and self.y_min > board_y_min and
                self.y_max < board_y_max):
            return 'XY_collision'
        elif not (self.x_min > board_x_min and self.x_max < board_x_max):
            return 'X_collision'
        elif not (self.y_min > board_y_min and self.y_max < board_y_max):
            return 'Y_collision'

    def object_excluded_collision(self, object_rect):

        object_x_min = object_rect[0]
        object_y_min = object_rect[1]
        object_x_max = object_rect[0] + object_rect[2]
        object_y_max = object_rect[1] + object_rect[3]

        return not (self.x_max < object_x_min or self.x_min > object_x_max or self.y_max < object_y_min or
                    self.y_min > object_y_max)


class LocalListener:
    def __init__(self, function_name):
        self.listener = keyboard.Listener(
            on_press=function_name
        )

    def listen(self):
        self.listener.start()


class GameActions:
    def __init__(self, scene, ball, paddle_left, paddle_right):
        self.scene = scene
        self.ball = ball
        self.paddle_left = paddle_left
        self.paddle_right = paddle_right

    def ball_movement(self):
        self.ball.move()
        # print(self.ball.rect[0])
        ball_collsions = DetectCollisions(self.ball.rect)
        if ball_collsions.object_included_collision(self.scene.rect) == 'X_collision':
            self.ball.bounce_x()
        elif ball_collsions.object_included_collision(self.scene.rect) == 'Y_collision':
            self.ball.bounce_y()
        elif ball_collsions.object_included_collision(self.scene.rect) == 'XY_collision':
            self.ball.bounce_y()
            self.ball.bounce_x()


class CurrentGameObjects:
    def __init__(self, window_width, window_height, paddles_color, ball_radius, ball_color):
        self.window_width = window_width
        self.x_mid = int(window_width / 2)
        self.y_mid = int(window_height / 2)
        self.paddles_color = paddles_color
        self.ball_color = ball_color
        self.ball_radius = ball_radius
        self.paddle_length = 110
        self.paddle_width = 20

    def get_ball(self):
        # parameters for a ball
        ball_surf_width = self.ball_radius * 2
        ball_surf_height = self.ball_radius * 2
        ball_x_speed = 5#random.randint(1, 5)
        ball_y_speed = 5#random.randint(1, 5)
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
