from cmd import Cmd
from enum import Enum
from itertools import cycle
import re
import time
import turtle
import copy
from queue import LifoQueue

class Colour(Enum):
    RED = 1
    GREEN = 2
    BLUE = 3
    WHITE = 4
    YELLOW = 5
    ORANGE = 6
    BLACK = 7


enum_colour_converter = {
    Colour.GREEN: "green",
    Colour.WHITE: "white",
    Colour.RED: "red",
    Colour.ORANGE: "orange",
    Colour.BLUE: "blue",
    Colour.YELLOW: "yellow",
    Colour.BLACK: "black",
    "green": Colour.GREEN,
    "white": Colour.WHITE,
    "red": Colour.RED,
    "orange": Colour.ORANGE,
    "blue": Colour.BLUE,
    "yellow": Colour.YELLOW,
    "black": Colour.BLACK,
    "GREEN": Colour.GREEN,
    "WHITE": Colour.WHITE,
    "RED": Colour.RED,
    "ORANGE": Colour.ORANGE,
    "BLUE": Colour.BLUE,
    "YELLOW": Colour.YELLOW,
    "BLACK": Colour.BLACK}


# import turtle  # importing the module
# trtl = turtle.Turtle()  # making a turtle object of Turtle class for drawing
# screen = turtle.Screen()  # making a canvas for drawing
# screen.setup(400, 300)  # choosing the screen size
# screen.bgcolor('black')  # making canvas black
# trtl.pencolor('red')  # making colour of the pen red
# trtl.pensize(5)  # choosing the size of pen nib
# trtl.speed(1)  # choosing the speed of drawing
# trtl.shape('turtle')  # choosing the shape of pen nib
# trtl.forward(150)  # drawing a line of 200 pixels
# trtl.right(90)  # asking turtle to turn 90 degrees
# trtl.forward(150)  # drawing a line of 200 pixels
# trtl.penup()  # preparing for moving pen without drawing
# trtl.setpos(-140, -120)  # making the new position of the turtle
# trtl.pendown()  # bringing the pen down for drawing again
# trtl.pencolor('green')  # choosin the pen colour as green
# trtl.write('Vivax Solutions', font=("Arial", 20, "bold"))  # chosing the font
# trtl.penup()
# trtl.ht()  # hiding the turtle from the screen


class Cubelet:
    def __init__(self, side_len, trtl):
        self.side_len = side_len
        self.reset_colours()
        self.mark = False
        self.trtl = trtl

    def dump(self):
        print(f"self.front_colour: {self.front_colour}")
        print(f"self.right_colour: {self.right_colour}")
        print(f"self.left_colour: {self.left_colour}")
        print(f"self.back_colour: {self.back_colour}")
        print(f"self.bottom_colour: {self.bottom_colour}")
        print(f"self.top_colour: {self.top_colour}")
        print(f"self.side_len: {self.side_len}")

    def is_same_orientation(self, other):
        result = False
        # print("self...")
        # self.dump()
        # print("other...")
        # other.dump()

        if self.front_colour == other.front_colour and \
                self.right_colour == other.right_colour and \
                self.left_colour == other.left_colour and \
                self.back_colour == other.back_colour and \
                self.bottom_colour == other.bottom_colour and \
                self.top_colour == other.top_colour:
            result = True
        # print(f"result: {result}")
        return result

    def reset_colours(self):
        self.front_colour = Colour.BLUE
        self.right_colour = Colour.RED
        self.left_colour = Colour.ORANGE
        self.back_colour = Colour.GREEN
        self.bottom_colour = Colour.WHITE
        self.top_colour = Colour.YELLOW

    def copy(self):
        result = Cubelet(self.side_len, self.trtl)
        result.mark = self.mark
        result.front_colour = self.front_colour
        result.right_colour = self.right_colour
        result.left_colour = self.left_colour
        result.back_colour = self.back_colour
        result.bottom_colour = self.bottom_colour
        result.top_colour = self.top_colour
        return result

    def rotate_up(self):
        temp_front_colour = self.front_colour
        self.front_colour = self.bottom_colour
        self.bottom_colour = self.back_colour
        self.back_colour = self.top_colour
        self.top_colour = temp_front_colour

    def rotate_right(self):
        temp_front_colour = self.front_colour
        self.front_colour = self.left_colour
        self.left_colour = self.back_colour
        self.back_colour = self.right_colour
        self.right_colour = temp_front_colour

    def rotate_left(self):
        temp_front_colour = self.front_colour
        self.front_colour = self.right_colour
        self.right_colour = self.back_colour
        self.back_colour = self.left_colour
        self.left_colour = temp_front_colour

    def rotate_down(self):
        temp_front_colour = self.front_colour
        self.front_colour = self.top_colour
        self.top_colour = self.back_colour
        self.back_colour = self.bottom_colour
        self.bottom_colour = temp_front_colour

    def rotate_cw(self):
        temp_top_colour = self.top_colour
        self.top_colour = self.left_colour
        self.left_colour = self.bottom_colour
        self.bottom_colour = self.right_colour
        self.right_colour = temp_top_colour

    def rotate_ccw(self):
        temp_top_colour = self.top_colour
        self.top_colour = self.right_colour
        self.right_colour = self.bottom_colour
        self.bottom_colour = self.left_colour
        self.left_colour = temp_top_colour

    def enum_to_turtle_colour(self, cube_colour):
        return enum_colour_converter[cube_colour]

    #
    # if cube_colour == Colour.GREEN:
    #     return "green" if not self.mark else "OLIVE"
    # if cube_colour == Colour.WHITE:
    #     return "white" if not self.mark else "IVORY1"
    # if cube_colour == Colour.RED:
    #     return "red" if not self.mark else "INDIANRED"
    # if cube_colour == Colour.ORANGE:
    #     return "orange" if not self.mark else "ORANGERED1"
    # if cube_colour == Colour.BLUE:
    #     return "blue" if not self.mark else "ROYALBLUE"
    # if cube_colour == Colour.YELLOW:
    #     return "yellow" if not self.mark else "YELLOW3"

    def draw(self, coords):

        x = coords[0]
        y = coords[1]
        z = coords[2]

        x += z / 2
        y -= z / 2

        tmp_side_len = self.side_len
        if self.mark:
            black_cubelet = BlackCubelet(self.side_len, self.trtl)
            black_cubelet.draw_sides(x, y)
            self.side_len -= 5

        self.draw_sides(x, y)

        self.side_len = tmp_side_len

    def reverse_draw(self, coords):

        x = coords[0]
        y = coords[1]
        z = coords[2]

        x -= z / 2
        y -= z / 2

        tmp_side_len = self.side_len
        if self.mark:
            black_cubelet = BlackCubelet(self.side_len, self.trtl)
            black_cubelet.draw_reverse_sides(x, y)
            self.side_len -= 5

        self.draw_reverse_sides(x, y)

        self.side_len = tmp_side_len

    def draw_filled_square(self, x, y, side_len, colour):
        self.trtl.pendown()
        self.trtl.fillcolor(colour)
        self.trtl.begin_fill()
        # forming front square face
        self.trtl.setpos(x, y)
        self.trtl.setpos(x + side_len, y)
        self.trtl.setpos(x + side_len, y + side_len)
        self.trtl.setpos(x, y + side_len)
        self.trtl.setpos(x, y)
        self.trtl.end_fill()
        self.trtl.penup()

    def draw_filled_side(self, x, y, side_len, colour):
        self.trtl.pendown()
        self.trtl.fillcolor(colour)
        self.trtl.begin_fill()
        self.trtl.setpos(x, y)
        self.trtl.setpos(x + side_len / 2, y - side_len / 2)
        self.trtl.setpos(x + side_len / 2, y + side_len / 2)
        self.trtl.setpos(x, y + side_len)
        self.trtl.setpos(x, y)
        self.trtl.end_fill()
        self.trtl.penup()

    def draw_reverse_filled_side(self, x, y, side_len, colour):
        self.trtl.pendown()
        self.trtl.fillcolor(colour)
        self.trtl.begin_fill()
        self.trtl.setpos(x, y)
        self.trtl.setpos(x - side_len / 2, y - side_len / 2)
        self.trtl.setpos(x - side_len / 2, y + side_len / 2)
        self.trtl.setpos(x, y + side_len)
        self.trtl.setpos(x, y)
        self.trtl.end_fill()
        self.trtl.penup()

    def draw_filled_upper(self, x, y, side_len, colour):
        self.trtl.pendown()
        self.trtl.fillcolor(colour)
        self.trtl.begin_fill()
        self.trtl.setpos(x, y)
        self.trtl.setpos(x + side_len / 2, y - side_len / 2)
        self.trtl.setpos(x + side_len / 2 + side_len, y - side_len / 2)
        self.trtl.setpos(x + side_len, y)
        self.trtl.setpos(x, y)
        self.trtl.end_fill()
        self.trtl.penup()

    def draw_reverse_filled_upper(self, x, y, side_len, colour):
        self.trtl.pendown()
        self.trtl.fillcolor(colour)
        self.trtl.begin_fill()
        self.trtl.setpos(x, y)
        self.trtl.setpos(x - side_len / 2, y - side_len / 2)
        self.trtl.setpos(x + side_len / 2, y - side_len / 2)
        self.trtl.setpos(x + side_len, y)
        self.trtl.setpos(x, y)
        self.trtl.end_fill()
        self.trtl.penup()

    def draw_sides(self, x, y):
        self.draw_filled_square(x, y, self.side_len, self.enum_to_turtle_colour(self.back_colour))
        self.draw_filled_upper(x, y, self.side_len, self.enum_to_turtle_colour(self.bottom_colour))
        self.draw_filled_side(x + self.side_len, y, self.side_len, self.enum_to_turtle_colour(self.right_colour))
        self.draw_filled_side(x, y, self.side_len, self.enum_to_turtle_colour(self.left_colour))
        self.draw_filled_square(x + self.side_len / 2, y - self.side_len / 2, self.side_len,
                                self.enum_to_turtle_colour(self.front_colour))
        self.draw_filled_upper(x, y + self.side_len, self.side_len, self.enum_to_turtle_colour(self.top_colour))

    #     self.draw_filled_upper(x, y + self.side_len, self.side_len, self.enum_to_turtle_colour(Colour.BLACK))

    def draw_reverse_sides(self, x, y):
        # self.draw_filled_square(x - self.side_len / 2, y - self.side_len / 2, self.side_len,
        #                         self.enum_to_turtle_colour(self.front_colour))
        # self.draw_reverse_filled_side(x + self.side_len, y, self.side_len, self.enum_to_turtle_colour(self.left_colour))
        self.draw_reverse_filled_side(x, y, self.side_len, self.enum_to_turtle_colour(self.right_colour))

        self.draw_reverse_filled_upper(x, y, self.side_len, self.enum_to_turtle_colour(self.bottom_colour))
        self.draw_filled_square(x, y, self.side_len, self.enum_to_turtle_colour(self.back_colour))


class NonCubelet(Cubelet):
    def __init__(self):
        self.side_len = 0
        self.front_colour = Colour.BLACK
        self.right_colour = Colour.BLACK
        self.left_colour = Colour.BLACK
        self.back_colour = Colour.BLACK
        self.bottom_colour = Colour.BLACK
        self.top_colour = Colour.BLACK
        self.mark = False


class BlackCubelet(Cubelet):
    def __init__(self, side_len, trtl):
        super(BlackCubelet, self).__init__(side_len, trtl)
        self.front_colour = Colour.BLACK
        self.right_colour = Colour.BLACK
        self.left_colour = Colour.BLACK
        self.back_colour = Colour.BLACK
        self.bottom_colour = Colour.BLACK
        self.top_colour = Colour.BLACK

