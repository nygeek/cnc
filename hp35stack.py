""" Implementation of the hp35 stack for the CNC calculator
    new_shell.py.

    If I were properly ambitious I would make this class handle
    a stack of arbitrary type, but I will be lazy and make it
    handle only the CNC class Complex

Started 2024-08-30

Copyright (C) 2024 Marc Donner

$Id$

"""

class HP35Stack:
    """ Class to implement the HP35 Stack and sto/rcl register """

    def __init__(self):
        _zero = complex(0.0, 0.0)
        self.stack = [_zero, _zero, _zero, _zero]
        self.storcl = _zero
        self.count = 0


    def __str__(self):
        _result = "M: " + str(self.storcl) + "\n\n"
        _result += "t: " + str(self.stack[3]) + "\n"
        _result += "z: " + str(self.stack[2]) + "\n"
        _result += "y: " + str(self.stack[1]) + "\n"
        _result += "x: " + str(self.stack[0])
        return _result


    def push(self, cn):
        """ push a number on to the stack """
        # this destroys the value in z (self.stack[3])
        self.stack[3] = self.stack[2]
        self.stack[2] = self.stack[1]
        self.stack[1] = self.stack[0]
        self.stack[0] = cn
        return cn


    def pop(self):
        """ pop the bottom element (x) from the stack and return it """
        # this rolls the stack down, thus replicating t into z
        _result = self.stack[0]
        self.stack[0] = self.stack[1]
        self.stack[1] = self.stack[2]
        self.stack[2] = self.stack[3]
        return _result


    def rolldown(self):
        """ perform the roll down function """
        _t = self.stack[0]
        self.stack[0] = self.stack[1]
        self.stack[1] = self.stack[2]
        self.stack[2] = self.stack[3]
        self.stack[3] = _t

    def get_count(self):
        """ return the count """
        return self.count

    def increment_count(self):
        self.count += 1
        return self.count

    def get_x(self):
        """ retrieve the x value from the stack """
        return self.stack[0]


    def get_y(self):
        """ retrieve the y value from the stack """
        return self.stack[1]


    def get_z(self):
        """ retrieve the x value from the stack """
        return self.stack[2]


    def get_t(self):
        """ retrieve the t value from the stack """
        return self.stack[3]


    def sto(self):
        """ sto function - copy x to M """
        self.storcl = self.stack[0]
        return self.stack[0]


    def rcl(self):
        """ rcl function - copy M to x (push the rest up) """
        self.push(self.storcl)


    def exch(self):
        """ exchange the values of x and y """
        x = self.stack[0]
        self.stack[0] = self.stack[1]
        self.stack[1] = x


def main():
    """ main """
    stack = HP35Stack()
    print(f"Stack:\n{stack}")
    _three = Complex(3, 3)
    stack.push(_three)
    _two = Complex(2, 2)
    stack.push(_two)
    _one = Complex(1, 1)
    stack.push(_one)
    _zero = Complex(-1, -1)
    stack.push(_zero)
    print(f"Stack:\n{stack}")
    qq = stack.get_x()
    print(f"x: {qq}")
    qq = stack.get_y()
    print(f"y: {qq}")
    qq = stack.get_z()
    print(f"z: {qq}")
    qq = stack.get_t()
    print(f"t: {qq}")
    qq = stack.pop()
    print(f"pop =>: {qq}")
    print(f"Stack:\n{stack}")
    stack.push(_two)
    stack.push(_one)
    stack.sto()
    stack.exch()
    stack.rcl()


if __name__ == '__main__':
    main()
