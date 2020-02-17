import random
from GameClasses import *
import pygame.locals


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
        ball_suf_width = ball_radius * 2
        ball_suf_height = ball_radius * 2
        ball_x_speed = random.randint(1, 5)
        ball_y_speed = random.randint(1, 5)
        self.ball_x_start = self.x_mid
        self.ball_y_start = self.y_mid

        self.ball = Ball(ball_suf_width, ball_suf_height, self.ball_x_start, self.ball_y_start, ball_color, ball_radius,
                         ball_x_speed, ball_y_speed)

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

    def move(self, key):
        try:
            if key.char == 'w' and self.left_paddle.rect.y > 0:
                self.left_paddle.move_paddle_up()
            elif key.char == 's' and self.left_paddle.rect.y < self.window.height - self.paddle_length:
                self.left_paddle.move_paddle_down()
        except Exception:
            print(False)

    def run(self):
        self.listener = keyboard.Listener(
            on_press=self.move)
        self.listener.start()
        while not self.handle_events():

            if self.ball.rect.y >= self.window.height - self.ball.radius * 2 or self.ball.rect.y <= 0:
                self.ball.bounce_y()

            if self.ball.rect.x >= self.window.width - self.ball.radius * 2 or self.ball.rect.x <= 0:
                self.ball.bounce_x()

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
