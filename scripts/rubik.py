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


class Cube:
    def __init__(self, bottom_left_back, side_len):
        print("Callinc init")
        # create cube as dictionary of tuples representing 3d coordinates
        self.cube = {}
        self.coords = {}
        self.prev_cube = {}
        self.stack = LifoQueue(maxsize=1000)
        self.side_len = side_len
        self.speed = 1

        self.tut = turtle.Screen()
        self.tut.bgcolor("black")
        self.trtl = turtle.Turtle()  # making a turtle object of Turtle class for drawing
        self.front_face = Colour.BLUE

        self.reset_cube()
        self.command_dispatch_dict = {"F": self.cw_rotate_blue_layer,
                                      "B": self.cw_rotate_green_layer,
                                      "R": self.cw_rotate_red_layer,
                                      "L": self.cw_rotate_orange_layer,
                                      "U": self.cw_rotate_yellow_layer,
                                      "D": self.cw_rotate_white_layer,
                                      "F'": self.ccw_rotate_blue_layer,
                                      "B'": self.ccw_rotate_green_layer,
                                      "R'": self.ccw_rotate_red_layer,
                                      "L'": self.ccw_rotate_orange_layer,
                                      "U'": self.ccw_rotate_yellow_layer,
                                      "D'": self.ccw_rotate_white_layer}

        self.green_front = {"F": self.cw_rotate_green_layer,
                            "B": self.cw_rotate_blue_layer,
                            "R": self.cw_rotate_orange_layer,
                            "L": self.cw_rotate_red_layer,
                            "F'": self.ccw_rotate_green_layer,
                            "B'": self.ccw_rotate_blue_layer,
                            "R'": self.ccw_rotate_orange_layer,
                            "L'": self.ccw_rotate_red_layer}

        self.blue_front = {"F": self.cw_rotate_blue_layer,
                           "B": self.cw_rotate_green_layer,
                           "R": self.cw_rotate_red_layer,
                           "L": self.cw_rotate_orange_layer,
                           "F'": self.ccw_rotate_blue_layer,
                           "B'": self.ccw_rotate_green_layer,
                           "R'": self.ccw_rotate_red_layer,
                           "L'": self.ccw_rotate_orange_layer}

        self.orange_front = {"F": self.cw_rotate_orange_layer,
                             "B": self.cw_rotate_red_layer,
                             "R": self.cw_rotate_blue_layer,
                             "L": self.cw_rotate_green_layer,
                             "F'": self.ccw_rotate_orange_layer,
                             "B'": self.ccw_rotate_red_layer,
                             "R'": self.ccw_rotate_blue_layer,
                             "L'": self.ccw_rotate_green_layer}

        self.red_front = {"F": self.cw_rotate_red_layer,
                          "B": self.cw_rotate_orange_layer,
                          "R": self.cw_rotate_green_layer,
                          "L": self.cw_rotate_blue_layer,
                          "F'": self.ccw_rotate_red_layer,
                          "B'": self.ccw_rotate_orange_layer,
                          "R'": self.ccw_rotate_green_layer,
                          "L'": self.ccw_rotate_blue_layer}

    def two_layer_start(self):
        self.reset_cube()
        cubelet = self.get_cubelet((0, 2, 2))
        cubelet.rotate_up()
        cubelet.rotate_right()

        cubelet = self.get_cubelet((1, 2, 2))
        cubelet.rotate_right()
        cubelet.rotate_right()
        cubelet.rotate_down()

        cubelet = self.get_cubelet((0, 2, 1))
        cubelet.rotate_right()
        cubelet.rotate_right()
        cubelet.rotate_ccw()

        cubelet = self.get_cubelet((0, 2, 0))
        cubelet.rotate_cw()
        cubelet.rotate_right()

        cubelet = self.get_cubelet((2, 2, 0))
        cubelet.rotate_cw()
        cubelet.rotate_down()

        self.draw()

    def mark_top_layer(self):
        for coord, cubelet in self.cube.items():
            if (coord[1] == 2):
                cubelet.mark = True
        self.draw()

    def unmark_all(self):
        for coord, cubelet in self.cube.items():
            cubelet.mark = False
        self.draw()

    def set_alg_front_face(self, front):
        self.front_face = enum_colour_converter.get(front, Colour.BLUE)
        print(f"Front colour is: {enum_colour_converter.get(self.front_face, 'undefined')}")

        colour_update = {
            Colour.GREEN: self.green_front,
            Colour.BLUE: self.blue_front,
            Colour.ORANGE: self.orange_front,
            Colour.RED: self.red_front
        }
        self.command_dispatch_dict.update(colour_update[self.front_face])

    def reset_cube(self):
        spacing = 5
        for x in reversed(range(3)):
            for y in range(3):
                for z in range(3):
                    x_pos = x * self.side_len + x * spacing
                    y_pos = y * self.side_len + y * spacing
                    z_pos = z * self.side_len + z * spacing
                    self.cube[(x, y, z)] = Cubelet(self.side_len, self.trtl)
                    self.coords[(x, y, z)] = (x_pos, y_pos, z_pos)

    def find_rotate_count(self, token):
        result = re.findall(r'\d+', token)
        return int(result[0]) if result else 1

    def do_alg(self, alg):
        alg_split = alg.split(' ')

        for token in alg_split:
            rotate_count = self.find_rotate_count(token)
            token = token.replace(str(rotate_count), "")
            for i in range(rotate_count):
                self.stack.put((token, self.front_face))
                print(f"rotating {token}")
                self.command_dispatch_dict.get(token, self.do_nothing)()
                if self.speed:
                    self.draw(self.speed)

    def rewind_alg(self, steps=1):
        for i in range(steps):
            if self.stack.empty():
                return

            pov_token = self.stack.get()
            self.set_alg_front_face(enum_colour_converter[pov_token[1]])
            token = pov_token[0]
            print(f"rewinding {token} {enum_colour_converter[pov_token[1]]} pov")
            if token.endswith("'"):
                token = token[:-1]
            else:
                token += "'"

            self.command_dispatch_dict.get(token, self.do_nothing)()
        self.draw()

    def do_nothing(self):
        print("Alg Command Not Recognised.")

    def cw_rotate_yellow_layer(self):
        self.rotate_y_layer_left(2)

    def ccw_rotate_yellow_layer(self):
        self.rotate_y_layer_right(2)

    def cw_rotate_white_layer(self):
        self.rotate_y_layer_right(0)

    def ccw_rotate_white_layer(self):
        self.rotate_y_layer_left(0)

    def cw_rotate_red_layer(self):
        self.rotate_x_layer_up(2)

    def ccw_rotate_red_layer(self):
        self.rotate_x_layer_down(2)

    def cw_rotate_orange_layer(self):
        self.rotate_x_layer_down(0)

    def ccw_rotate_orange_layer(self):
        self.rotate_x_layer_up(0)

    def cw_rotate_blue_layer(self):
        self.rotate_z_layer_cw(2)

    def ccw_rotate_blue_layer(self):
        self.rotate_z_layer_ccw(2)

    def cw_rotate_green_layer(self):
        self.rotate_z_layer_ccw(0)

    def ccw_rotate_green_layer(self):
        self.rotate_z_layer_cw(0)

    def rotate_x_layer_up(self, layer):
        for coord, cubelet in self.cube.items():
            if (coord[0] == layer):
                cubelet.rotate_up()

        temp_cubelet = self.get_cubelet((layer, 2, 2))
        self.copy_cubelet((layer, 2, 2), (layer, 0, 2))
        self.copy_cubelet((layer, 0, 2), (layer, 0, 0))
        self.copy_cubelet((layer, 0, 0), (layer, 2, 0))
        self.set_cubelet((layer, 2, 0), temp_cubelet)

        temp_cubelet = self.get_cubelet((layer, 2, 1))
        self.copy_cubelet((layer, 2, 1), (layer, 1, 2))
        self.copy_cubelet((layer, 1, 2), (layer, 0, 1))
        self.copy_cubelet((layer, 0, 1), (layer, 1, 0))
        self.set_cubelet((layer, 1, 0), temp_cubelet)

    def rotate_x_layer_down(self, layer):
        for i in range(3):
            self.rotate_x_layer_up(layer)

    def rotate_y_layer_left(self, layer):
        for coord, cubelet in self.cube.items():
            if (coord[1] == layer):
                cubelet.rotate_left()

        temp_cubelet = self.get_cubelet((0, layer, 0))
        self.copy_cubelet((0, layer, 0), (0, layer, 2))
        self.copy_cubelet((0, layer, 2), (2, layer, 2))
        self.copy_cubelet((2, layer, 2), (2, layer, 0))
        self.set_cubelet((2, layer, 0), temp_cubelet)
        temp_cubelet = self.get_cubelet((1, layer, 0))
        self.copy_cubelet((1, layer, 0), (0, layer, 1))
        self.copy_cubelet((0, layer, 1), (1, layer, 2))
        self.copy_cubelet((1, layer, 2), (2, layer, 1))
        self.set_cubelet((2, layer, 1), temp_cubelet)

    def rotate_y_layer_right(self, layer):
        for i in range(3):
            self.rotate_y_layer_left(layer)

    def rotate_z_layer_cw(self, layer):
        for coord, cubelet in self.cube.items():
            if (coord[2] == layer):
                cubelet.rotate_cw()

        temp_cubelet = self.get_cubelet((0, 2, layer))
        self.copy_cubelet(((0, 2, layer)), (0, 0, layer))
        self.copy_cubelet((0, 0, layer), (2, 0, layer))
        self.copy_cubelet((2, 0, layer), (2, 2, layer))
        self.set_cubelet((2, 2, layer), temp_cubelet)

        temp_cubelet = self.get_cubelet((0, 1, layer))
        self.copy_cubelet((0, 1, layer), (1, 0, layer))
        self.copy_cubelet((1, 0, layer), (2, 1, layer))
        self.copy_cubelet((2, 1, layer), (1, 2, layer))
        self.set_cubelet((1, 2, layer), temp_cubelet)

    def rotate_z_layer_ccw(self, layer):
        for i in range(3):
            self.rotate_z_layer_cw(layer)

    def copy_cubelet(self, destination, start):
        self.set_cubelet(destination, self.get_cubelet(start))

    def get_cubelet(self, coord):
        return self.cube[coord]

    def set_cubelet(self, coord, cubelet):
        self.cube[coord] = cubelet

    def mark_cubelet(self, coord):
        self.get_cubelet(coord).mark = True
        self.draw()

    def unmark_cubelet(self, coord):
        self.get_cubelet(coord).mark = False
        self.draw()

    def draw(self, *args):
        # Forming the window screen
        turtle.tracer(0, 0)
        for z in range(3):
            for y in range(3):
                for x in reversed(range(3)):
                    # print(f"drawing: {(x, y, z)}")
                    # if not self.cube[(x, y, z)].is_same_orientation(self.prev_cube.get((x, y, z), NonCubelet())):
                    coords = self.coords[(x, y, z)]
                    moved_coords = (coords[0], coords[1], coords[2])
                    self.cube[(x, y, z)].draw(moved_coords)

                    # self.prev_cube[(x, y, z)] = self.cube[(x, y, z)].copy()

        for y in reversed(range(3)):
            for x in range(3):
                # for x in reversed(range(3)):
                for z in reversed(range(3)):
                    # print(f"drawing: {(x, y, z)}")
                    # if not self.cube[(x, y, z)].is_same_orientation(self.prev_cube.get((x, y, z), NonCubelet())):
                    coords = self.coords[(x, y, z)]
                    reverse_coords = (-coords[0] - 50, coords[1] - 200, coords[2])
                    self.cube[(x, y, z)].reverse_draw(reverse_coords)

                    self.prev_cube[(x, y, z)] = self.cube[(x, y, z)].copy()

        turtle.update()

        for sleep_time in args:
            time.sleep(sleep_time)

    # cube.do_alg("F U R U' R' F'")
    #


class MyPrompt(Cmd):
    def __init__(self):
        self.cube = None
        super(MyPrompt, self).__init__()
        self.cube = Cube((0, 0, 0), 100)
        self.cube.draw()

    def do_alg(self, i):
        '''enter one or more setps separated by space eg: alg F U R U' R' F'''
        self.cube.do_alg(i)
        self.cube.draw()

    def do_fururf(self, i):
        '''shortcut to enter alg F U R U' R' F' just type fururf'''
        self.cube.do_alg("F U R U' R' F'")
        self.cube.draw()

    def do_rururuur(self, i):
        '''shortcut to enter alg R U R' U R U2 R' just type rururuur'''
        self.cube.do_alg("R U R' U R U2 R'")
        self.cube.draw()

    def do_top_corner_alg(self, i):
        '''shortcut to enter alg L' U R U' L U R' R U R' U R U2 R' just type top_corner_alg'''
        self.cube.do_alg("L' U R U' L U R' R U R' U R U2 R'")
        self.cube.draw()

    def do_top_edge_cw_swap(self, i):
        '''shortcut to enter alg L' U R U' L U R' R U R' U R U2 R' just type top_edge_cw_swap'''
        self.cube.do_alg("F2 U R' L F2 L' R U F2")
        self.cube.draw()

    def do_top_edge_ccw_swap(self, i):
        '''shortcut to enter alg F2 U' R' L F2 L' R U' F2 just type top_edge_ccw_swap'''
        self.cube.do_alg("F2 U' R' L F2 L' R U' F2")
        self.cube.draw()

    def do_speed(self, i):
        '''set display pause time after each alg rotation set speed 0 stops draw pause on each step '''
        self.cube.speed = int(i)

    def do_two_layer_start(self, i):
        '''set sets up cube with only top layer to solve'''
        self.cube.two_layer_start()

    def do_mark_top_layer(self, i):
        '''mark top layer cubelets (by making them smaller) so movement can be followed in subsequent steps'''
        self.cube.mark_top_layer()

    def get_coord_from_ip(self, i):
        result = None
        if len(i) == 3:
            result = (int(i[0]), int(i[1]), int(i[2]))
        if len(i) == 5:
            result = (int(i[0]), int(i[2]), int(i[4]))
        return result

    def do_mark(self, i):
        '''mark single cubelet (makes it smaller) to by coordinates x,y,z eg mark 1,2,3 or mark 123 so movement can be followed in subsequent steps'''
        self.cube.mark_cubelet(self.get_coord_from_ip(i))

    def do_unmark(self, i):
        '''unmark mark single cubelet to by coordinates x,y,z eg unmark 1,2,3 or unmark 123'''
        self.cube.unmark_cubelet(self.get_coord_from_ip(i))

    def do_unmark_all(self, i):
        '''unmark all cubelet to by coordinates x,y, z show movement after alg steps coming up'''
        self.cube.unmark_all()

    def do_set_alg_front(self, i):
        '''set fromt of cube from an alg POV eg set_alg_front GREEN'''
        self.cube.set_alg_front_face(i)

    def do_rw(self, i):
        '''rewind alg commands - rw does one step rw 4 does 4 etc'''
        i = int(i) if i else 1
        print(f"Calling rewind with:{i}")
        self.cube.rewind_alg(i)

    def do_exit(self, i):
        '''exit the application.'''
        print("Bye")
        return True

    def help_add(self):
        print("Add a new entry to the system.")


MyPrompt().cmdloop()
