from cmd import Cmd
from enum import Enum
import re
import time
import turtle
import copy
from queue import LifoQueue
import cubelet

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

