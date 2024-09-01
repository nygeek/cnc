""" Implementation of the hp35 stack for the CNC calculator
    new_shell.py.

    If I were properly ambitious I would make this class handle
    a stack of arbitrary type, but I will be lazy and make it
    handle only the CNC class Complex

Started 2024-08-30

Copyright (C) 2024 Marc Donner

"""

# Complex class
import cnc
from debug import Debug

class HP35Stack:
    """ Class to implement the HP35 Stack and sto/rcl register """

    def __init__(self, debug):
        _old = debug.inc()
        _zero = cnc.Complex(0.0, 0.0, debug)
        self.stack = [_zero, _zero, _zero, _zero]
        self.storcl = _zero
        debug.reset(_old)


    def __str__(self):
        _result = "M: " + str(self.storcl) + "\n\n"
        _result += "t: " + str(self.stack[3]) + "\n"
        _result += "z: " + str(self.stack[2]) + "\n"
        _result += "y: " + str(self.stack[1]) + "\n"
        _result += "x: " + str(self.stack[0])
        return _result


    def push(self, cn, debug):
        """ push a number on to the stack """
        # this destroys the value in self.stack[3]
        if debug.get():
            print(f"{debug.indent()}push({cn})")
        self.stack[3] = self.stack[2]
        self.stack[2] = self.stack[1]
        self.stack[1] = self.stack[0]
        self.stack[0] = cn


    def pop(self, debug):
        """ pop the bottom element (x) from the stack and return it """
        # this rolls the stack down, thus replicating t into z
        _result = self.stack[0]
        self.stack[0] = self.stack[1]
        self.stack[1] = self.stack[2]
        self.stack[2] = self.stack[3]
        if debug.get():
            print(f"{debug.indent()}pop()")
            print(f"{debug.indent()}pop => {_result}")
        return _result


    def rolldown(self, debug):
        """ perform the roll down function """
        if debug.get():
            print(f"{debug.indent()}rolldown()")
        _t = self.stack[0]
        self.stack[0] = self.stack[1]
        self.stack[1] = self.stack[2]
        self.stack[2] = self.stack[3]
        self.stack[3] = _t

    def get_x(self, debug):
        """ retrieve the x value from the stack """
        if debug.get():
            print(f"{debug.indent()}get_x()")
            print(f"{debug.indent()}get_x => {self.stack[0]}")
        return self.stack[0]


    def get_y(self, debug):
        """ retrieve the y value from the stack """
        if debug.get():
            print(f"{debug.indent()}get_y()")
            print(f"{debug.indent()}get_y => {self.stack[1]}")
        return self.stack[1]


    def get_z(self, debug):
        """ retrieve the x value from the stack """
        if debug.get():
            print(f"{debug.indent()}get_z()")
            print(f"{debug.indent()}get_z => {self.stack[2]}")
        return self.stack[2]


    def get_t(self, debug):
        """ retrieve the t value from the stack """
        if debug.get():
            print(f"{debug.indent()}get_t()")
            print(f"{debug.indent()}get_t => {self.stack[3]}")
        return self.stack[3]


    def sto(self, debug):
        """ sto function - copy x to M """
        self.storcl = self.stack[0]
        if debug.get():
            print(f"{debug.indent()}sto()")
            print(self)
        return self.stack[0]


    def rcl(self, debug):
        """ rcl function - copy M to x (push the rest up) """
        self.push(self.storcl, debug.inc())
        debug.dec()
        if debug.get():
            print(f"{debug.indent()}rcl()")
            print(self)


    def exch(self, debug):
        """ exchange the values of x and y """
        x = self.stack[0]
        self.stack[0] = self.stack[1]
        self.stack[1] = x
        if debug.get():
            print(f"{debug.indent()}exch()")
            print(self)


def main():
    """ main """
    debug = Debug(True)
    print(f"debug.get(): {debug.get()}")
    stack = HP35Stack(debug)
    print(f"Stack:\n{stack}")
    _three = cnc.Complex(3, 3, debug)
    stack.push(_three, debug)
    _two = cnc.Complex(2, 2, debug)
    stack.push(_two, debug)
    _one = cnc.Complex(1, 1, debug)
    stack.push(_one, debug)
    _zero = cnc.Complex(-1, -1, debug)
    stack.push(_zero, debug)
    print(f"Stack:\n{stack}")
    qq = stack.get_x(debug)
    print(f"x: {qq}")
    qq = stack.get_y(debug)
    print(f"y: {qq}")
    qq = stack.get_z(debug)
    print(f"z: {qq}")
    qq = stack.get_t(debug)
    print(f"t: {qq}")
    qq = stack.pop(debug)
    print(f"pop =>: {qq}")
    print(f"Stack:\n{stack}")
    stack.push(_two, debug)
    stack.push(_one, debug)
    stack.sto(debug)
    stack.exch(debug)
    stack.rcl(debug)


if __name__ == '__main__':
    main()
