import pygame as pg
from pynput import keyboard


def on_press(key):
    try:
        # return key.char
        print(f'alphanumeric key {key.char} pressed')
    except AttributeError:
        print(f'special key {key} pressed')


def on_release(key):
    print(f'{key} released')
    if key == keyboard.Key.esc:
        # Stop listener
        return False


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


class GameObject:
    def __init__(self, width, height, x, y, color):
        self.width = int(width)
        self.height = int(height)
        self.start_x = x
        self.start_y = y
        self.color = color
        self.surface = pg.Surface((self.width, self.height), pg.SRCALPHA, 32).convert_alpha()
        self.rect = self.surface.get_rect(x=self.start_x, y=self.start_y)
        print(f'to jest Game Object self.rect: {self.rect}')

    def draw(self, window):
        window.blit(self.surface, self.rect)


class Ball(GameObject):
    def __init__(self, width, height, x, y, color, radius, x_direction=0, y_direction=0):
        super(Ball, self).__init__(width, height, x, y, color)
        self.radius = radius
        circle = pg.draw.circle(self.surface, color, [self.radius, self.radius], self.radius)
        print(f'to jest circle: {circle}')
        self.x_direction = x_direction
        self.y_direction = y_direction

    def bounce_x(self):
        self.x_direction *= -1

    def bounce_y(self):
        self.y_direction *= -1

    def move(self):
        self.rect.x += self.x_direction
        self.rect.y += self.y_direction
        print(self.rect)

    def board_collision(self, rect_object):
        x_left = rect_object[0]
        x_right = rect_object[0] + rect_object[2]
        y_up = rect_object[1]
        y_bottom = rect_object[1]+rect_object[3]

        if self.rect.y <= y_up or self.rect.y+2*self.radius>= y_bottom:
            self.bounce_y()

        if self.rect.x <= x_left or self.rect.x+2*self.radius >= x_right:
            self.bounce_x()

    def paddle_collision(self, rect_object):
        pass


class Paddle(GameObject):
    def __init__(self, width, height, x, y, color, y_direction=100):
        super(Paddle, self).__init__(width, height, x, y, color)
        self.y_direction = y_direction
        pg.draw.line(self.surface, color, [0, 0], [0, self.height], 20)

        # pg.draw.ellipse(self.surface, color, (0, 0, self.width, self.height))

    def move_paddle_up(self):
        self.rect.y -= self.y_direction

    def move_paddle_down(self):
        self.rect.y += self.y_direction

    def get_paddle_line(self, *args):
        paddle_x = self.rect.x
        for arg in args:
            paddle_x += arg
        paddle_y_up = self.rect.y
        paddle_y_down = self.rect.y + self.height
        return [paddle_x, paddle_y_up,  paddle_y_down]

    # def move_left_paddle(self, key_name_up, key_name_down):
    #     pass
board = Board(500, 700, (100,100,100))
print(board)