import random
from GameClasses import *
import pygame.locals
from pynput import keyboard


class PingPong:
    def __init__(self, window_width, window_height, window_color, paddles_color, ball_radius, ball_color):
        pg.init()

        self.listener = keyboard.Listener()
        # window parameters
        self.window = Board(window_width, window_height, window_color)
        self.x_mid = int(width / 2)
        self.y_mid = int(height / 2)
        self.fps_clock = pygame.time.Clock()

        # parameters for a ball
        ball_surf_width = ball_radius * 2
        ball_surf_height = ball_radius * 2
        ball_x_speed = random.randint(1, 5)
        ball_y_speed = random.randint(1, 5)
        self.ball_x_start = self.x_mid
        self.ball_y_start = self.y_mid

        self.ball = Ball(ball_surf_width, ball_surf_height, self.ball_x_start, self.ball_y_start, ball_color,
                         ball_radius, ball_x_speed, ball_y_speed)

        # parameters for paddles
        self.paddle_length = 110
        self.paddle_width = 20
        # the left one
        self.left_pad_x_start = 30
        self.left_pad_y_start = self.y_mid - int(self.paddle_length / 2)

        self.left_paddle = Paddle(self.paddle_width, self.paddle_length, self.left_pad_x_start, self.left_pad_y_start,
                                  paddles_color)

        # the right one
        self.right_pad_x_start = self.window.width - 40
        self.right_pad_y_start = self.y_mid - int(self.paddle_length / 2)

        self.right_paddle = Paddle(self.paddle_width, self.paddle_length, self.right_pad_x_start,
                                   self.right_pad_y_start, paddles_color)

    def move_paddles(self, key):
        try:
            if key == keyboard.Key.up and self.right_paddle.rect.y > 0:
                self.right_paddle.move_paddle_up()
            elif key == keyboard.Key.down and self.right_paddle.rect.y < self.window.height - self.paddle_length:
                self.right_paddle.move_paddle_down()
            elif key.char == 'w' and self.left_paddle.rect.y > 0:
                self.left_paddle.move_paddle_up()
            elif key.char == 's' and self.left_paddle.rect.y < self.window.height - self.paddle_length:
                self.left_paddle.move_paddle_down()

        except Exception:
            print(False)

    def get_paddle_position(self, paddle, *args):
        paddle_x = paddle.rect.x
        for arg in args:
            paddle_x += arg
        paddle_y_up = paddle.rect.y
        paddle_y_down = paddle.rect.y + self.paddle_length
        return [paddle_x, paddle_y_down, paddle_y_up]

    def board_collisions(self):
        if self.ball.rect.y >= self.window.height - self.ball.radius * 2 or self.ball.rect.y <= 0:
            self.ball.bounce_y()

    def left_paddle_collisions(self):
        left_paddle_position = self.get_paddle_position(self.left_paddle, self.paddle_width, -self.ball.radius)
        if (self.ball.rect.x <= left_paddle_position[0] and left_paddle_position[2] <= self.ball.rect.y <=
                left_paddle_position[1]):
            self.ball.bounce_x()

    def right_paddle_collisions(self):
        right_paddle_position = self.get_paddle_position(self.right_paddle, -self.paddle_width)
        if self.ball.rect.x >= right_paddle_position[0] and right_paddle_position[2] <= self.ball.rect.y <= \
                right_paddle_position[1]:
            self.ball.bounce_x()


    def run(self):
        self.listener = keyboard.Listener(
            on_press=self.move_paddles)
        self.listener.start()

        while not self.handle_events():
            self.board_collisions()
            self.left_paddle_collisions()
            self.right_paddle_collisions()

            # if (self.ball.rect.x <= left_paddle_position[0] and left_paddle_position[2] <= self.ball.rect.y <=
            #     left_paddle_position[1]) or (
            #         self.ball.rect.x >= right_paddle_position[0] and right_paddle_position[2] <= self.ball.rect.y <=
            #         right_paddle_position[1]):
            #     self.ball.bounce_x()

            self.ball.move()
            self.window.draw_elements(
                self.ball,
                self.left_paddle,
                self.right_paddle
            )
            self.fps_clock.tick(70)


    def handle_events(self):
        for event in pg.event.get():
            if event.type == pygame.locals.QUIT:
                self.listener.stop()
                pg.quit()
                return True


if __name__ == "__main__":
    color = (10, 200, 100)
    width = 1000
    height = 1000
    x = int(width / 2)
    y = int(height / 2)
    object_color = (255, 255, 255)
    radius = 10

    game = PingPong(width, height, color, object_color, radius, object_color)
    game.run()
    # game.windowLook((10, 100, 200))
    # time.sleep(10)
    pg.quit()
    # game.run()
