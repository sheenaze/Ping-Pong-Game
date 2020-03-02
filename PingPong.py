
from GameClasses import *
import pygame.locals
from pynput import keyboard




class PingPong:
    def __init__(self, window_width, window_height, window_color, paddles_color, ball_radius, ball_color):
        pg.init()

        self.window = Board(window_width, window_height, window_color)
        self.game_objects = GameObjects(window_width, window_height, paddles_color, ball_radius, ball_color)

        self.ball = self.game_objects.get_ball()
        self.left_paddle = self.game_objects.get_left_paddle()
        self.right_paddle = self.game_objects.get_right_paddle()

        self.fps_clock = pygame.time.Clock()
    def run(self):

        while not self.handle_events():
            self.ball.move()

            self.window.draw_elements(
                self.ball,
                self.left_paddle,
                self.right_paddle
            )
            self.fps_clock.tick(100)

    def handle_events(self):
        for event in pg.event.get():
            if event.type == pygame.locals.QUIT:
                # self.listener.stop()
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
