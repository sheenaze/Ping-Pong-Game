import pygame as pg
import time
# pg.init()

BLACK = (0,0,0)
WHITE = (255,255,255)


# size = (500, 700)
# screen = pygame.display.set_mode(size, pygame.RESIZABLE)
# print(pygame.display.Info())
# # screen = pygame.display.mode_ok(size)
# pygame.display.set_caption("PingPong")
#
#
#
# carryOn = True
#
# # The clock will be used to control how fast the screen updates
# clock = pygame.time.Clock()
#
# # -------- Main Program Loop -----------
# while carryOn:
#     # --- Main event loop
#     for event in pygame.event.get():  # User did something
#         if event.type == pygame.QUIT:  # If user clicked close
#             carryOn = False  # Flag that we are done so we exit this loop

class Board:
    def __init__(self, width, height):
        self.window = pg.display.set_mode((width, height), pg.RESIZABLE)

    def changeWindowColor(self, window_color):
        self.window.fill(window_color)
        pg.display.update()

    # pg.display.set_caption('PingPong by Mon')

    # def draw(self, *args):
    #     background = (100, 100, 100)
    #     self.window.fill(background)
    #     for drawable in args:
    #         drawable.draw_on(self.window)
    #
    #     pg.display.update()


board = Board(500,700)
board.changeWindowColor((100, 100, 200))
time.sleep(10)