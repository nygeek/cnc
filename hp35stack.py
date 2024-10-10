""" Implementation of the hp35 stack for the CNC calculator
        print(f"self.stack: [{self.stack}]")
    new_shell.py.

    If I were properly ambitious I would make this class handle
    a stack of arbitrary type, but I will be lazy and make it
    handle only the cmath type complex.

Started 2024-08-30

Copyright (C) 2024 Marc Donner

$Id$

"""

class HP35Stack:
    """ Class to implement the HP35 Stack and sto/rcl register """

    def __init__(self, depth=4, _clamp=1e-10 ):
        _zero = complex(0.0, 0.0)
        self.stack = [_zero] * depth
        self.depth = depth
        self.clamp_threshold = _clamp
        self.labels = [0] * depth
        for j in range(4, depth):
            self.labels[j] = str(j)
        self.labels[0] = "X"
        self.labels[1] = "Y"
        self.labels[2] = "Z"
        self.labels[3] = "T"
        self.storcl = _zero
        self.count = 0


    def __str__(self):
        _result = "M: " + str(self.storcl) + "\n\n"
        for j in range(self.depth - 1, -1, -1):
            _result += self.labels[j] + ": " + str(self.stack[j]) + "\n"
        return _result


    def push(self, cn):
        """ push a number on to the stack """
        # this destroys the value at the top of the stack
        for j in range(self.depth - 1, 0, -1):
            self.stack[j] = self.stack[j-1]
        self.stack[0] = self.clamp(cn)
        return cn


    def clamp(self, z):
        """ clamp real and imag parts of z to within clamp of ints """
        r = complex(z).real
        i = complex(z).imag
        if abs(r-round(r)) < self.clamp_threshold:
            r = round(r)
        if abs(i-round(i)) < self.clamp_threshold:
            i = round(i)
        return complex(r, i)


    def pop(self):
        """ pop the bottom element (x) from the stack and return it """
        # this rolls the stack down, thus replicating t into z
        _result = self.stack[0]
        for j in range(0, self.depth - 1):
            self.stack[j] = self.stack[j+1]
        return _result


    def rolldown(self):
        """ perform the roll down function """
        _t = self.stack[0]
        for j in range(0, self.depth - 1):
            self.stack[j] = self.stack[j+1]
        self.stack[self.depth - 1] = _t


    def get_count(self):
        """ return the count """
        return self.count


    def increment_count(self):
        """ increment the count of stack interactions """
        self.count += 1
        return self.count


    def get_x(self):
        """ retrieve the x value from the stack """
        return self.stack[0]


    def set_x(self, new_x):
        """ retrieve the x value from the stack """
        self.stack[0] = new_x
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
    stack = HP35Stack(8)
    print(f"Stack:\n{stack}")
    _three = complex(3, 3)
    stack.push(_three)
    _two = complex(2, 2)
    stack.push(_two)
    _one = complex(1, 1)
    stack.push(_one)
    _zero = complex(-1, -1)
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
