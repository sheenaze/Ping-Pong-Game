import random

import pygame as pg
from GameClasses import *
import pygame.locals

window_color = (10,200,100)
width = 1000
height = 1000
x = int(width/2)
y = int(height/2)
object_color = (255, 255, 255)
radius = 10

class PingPong:
    def __init__(self, window_width = width, window_height = height, window_color = window_color, paddles_color = object_color, ball_radius = radius, ball_color = object_color):
        pg.init()

        self.window = Board(window_width, window_height)
        self.window.changeWindowColor(window_color)
        self.x = int(width / 2)
        self.y = int(height / 2)
        self.fps_clock = pygame.time.Clock()
        x_direction = random.randint(1, 5)
        y_direction = random.randint(1, 5)
        paddle_length = 110
        paddle_width = 20
        self.ball = Ball(ball_radius*2, ball_radius*2, self.x, self.y, object_color, ball_radius, x_direction=x_direction, y_direction=y_direction)
        self.paddle_left = Paddle(paddle_width, paddle_length, 10, self.y, object_color)

    def run(self):
        while not self.handle_events():
            if self.ball.rect.y >= self.window.height - self.ball.radius*2 or self.ball.rect.y <= 0:
                self.ball.bounce_y()

            if self.ball.rect.x >= self.window.width - self.ball.radius*2  or self.ball.rect.x <= 0:
                self.ball.bounce_x()

            self.ball.move()
            self.window.draw_elements(
                self.ball,
                self.paddle_left
                                      )
            self.fps_clock.tick(70)

    def handle_events(self):
        for event in pg.event.get():
            if event.type == pygame.locals.QUIT:
                pygame.quit()
                return True




if __name__ == "__main__":
    game = PingPong()
    game.run()
    # game.windowLook((10, 100, 200))
    time.sleep(10)
    pg.quit()
    # game.run()