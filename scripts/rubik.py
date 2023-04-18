from cmd import Cmd
import cubelet
import cube

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
