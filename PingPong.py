import pygame as pg
from GameClasses import *

class PingPong:
    def __init__(self, width, height, window_color):
        pg.init()
        self.window = Board(width, height)




if __name__ == "__main__":
    game = PingPong(800, 400, (10, 100, 200))
    time.sleep(10)
    # game.run()