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
        # pg.display.flip()
        print(self.rect)


class Paddle(GameObject):
    def __init__(self, width, height, x, y, color, y_direction=20):
        self.y_direction = y_direction
        super(Paddle, self).__init__(width, height, x, y, color)
        pg.draw.line(self.surface, color, [0, 0], [0, self.height], 20)
        # pg.draw.ellipse(self.surface, color, (0, 0, self.width, self.height))

    def move_paddle_up(self):
        self.rect.y -= self.y_direction

    def move_paddle_down(self):
        self.rect.y += self.y_direction

    # def move_left_paddle(self, key_name_up, key_name_down):
    #     pass
