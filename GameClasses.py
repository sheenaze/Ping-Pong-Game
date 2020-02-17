import pygame as pg
import time


# pg.init()


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
        self.surface = pg.Surface((self.width, self.height), pg.SRCALPHA,  32).convert_alpha()
        self.rect = self.surface.get_rect(x = self.start_x, y = self.start_y)
        print(f'to jest Game Object self.rect: {self.rect}')

    def draw(self, window):
        window.blit(self.surface, self.rect)

class Ball(GameObject):
    def __init__(self, width, height, x, y, color, radius, x_direction = 0, y_direction = 0):
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
    def __init__(self, width, height, x, y, color, y_direction = 0):
        super(Paddle, self).__init__(width, height, x, y, color)
        pg.draw.line(self.surface, color, [0,0], [0, self.height], 20)
        # pg.draw.ellipse(self.surface, color, (0, 0, self.width, self.height))



width = 1000
height = 1000
window_color = (100, 100, 200)
object_color = (255,255,255)
x = int(width/2)
y = int(height/2)
radius = 10
# board = Board(width,height)
# print(type(board))
# board.changeWindowColor(window_color)

# object = GameObjects(int(width*0.02), int(height*0.02), object_color, x, y)

# surface = pg.display.set_mode((width, height))
# surface.fill(window_color)
# pg.display.update()

# ball = Ball(int(radius*2), int(2*radius) ,x, y, object_color,  radius)
# print(ball.rect)
# board.draw_elements(window_color, ball)
# circle = pg.draw.circle(surface, object_color, [x, y], 10)
# pg.display.flip()

# width, height, x, y, color, radius):

# print(circle)


# time.sleep(10)




# class Board:
#     def __init__(self, width, height):
#         self.surface = pg.display.set_mode((width, height))
#         pg.display.set_caption('PingPong by Mon')
#
#     def window_look(self, window_color = (0,0,0)):
#         self.surface.fill(window_color)
#         pg.display.update()
#
#     def draw_object(self, *args):
#         """
#         Rysuje okno gry
#
#         :param args: lista obiektów do narysowania
#         """
#         background = (230, 255, 255)
#         self.surface.fill(background)
#         for drawable in args:
#             drawable.draw_on(self.surface)
#
#         # dopiero w tym miejscu następuje fatyczne rysowanie
#         # w oknie gry, wcześniej tylko ustalaliśmy co i jak ma zostać narysowane
#         pg.display.update()
#
#     # def draw_object(self, *args):
#     #     for element in args:
#     #         element.draw_on(self.surface)
#     #     pg.display.flip()
#     # # def draw_object(self, *args):
#     #     for element in args:
#     #         element.draw_element(self.surface)
#     #     pg.display.update()
#
# class Drawable(object):
#     """
#     Klasa bazowa dla rysowanych obiektów
#     """
#
#     def __init__(self, width, height, x, y, color=(0, 255, 0)):
#         self.width = width
#         self.height = height
#         self.color = color
#         self.surface = pg.Surface([width, height], pg.SRCALPHA, 32).convert_alpha()
#         self.rect = self.surface.get_rect(x=x, y=y)
#
#     def draw_on(self, surface):
#         surface.blit(self.surface, self.rect)
#
# class Ball(Drawable):
#     """
#     Piłeczka, sama kontroluje swoją prędkość i kierunek poruszania się.
#     """
#     def __init__(self, width, height, x, y, color=(255, 0, 0), x_speed=3, y_speed=3):
#         super(Ball, self).__init__(width, height, x, y, color)
#         # pg.draw.ellipse(self.surface, self.color, [0, 0, self.width, self.height])
#         pg.draw.circle(self.surface, self.color,[0,0], 10, 10)
#
# # class Ball:
# #     def __init__(self, width, height, color, position, radius):
# #         self.x = position[0]
# #         self.y = position[1]
# #         self.surface = pg.Surface((width, height), pg.SRCALPHA).convert_alpha()
# #         self.rect = self.surface.get_rect(x = self.x, y = self.y)
# #         pg.draw.circle(self.surface, color, position, radius)
# #         # pg.display.update()
# #
# #     def draw_on(self, surface):
# #         surface.blit(self.surface, self.rect)
#
#
# width = 1000
# height = 1000
# x = int(width/2)+100
# y = int(height/2)
# object_color = (255, 255, 255)
# window_color = (10, 200, 100)
# radius = 10
#
# board = Board(width, height)
# board.window_look(window_color)
# # ball = Ball((width*0.02),(height*0.02), object_color, [x, y], radius)
# ball = Ball(20, 20, int(width/2), int(height/2), object_color)
#
# board.draw_object(ball)
# # pg.draw.circle(board.surface, object_color, [x, y], radius)
# # pg.display.update()
# # print(board.surface)
# time.sleep(10)
#

